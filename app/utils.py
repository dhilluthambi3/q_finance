import time
import uuid
import json
from functools import wraps
from typing import Callable, Any
from flask import request, make_response, Response


def request_id_middleware():
    if not request.headers.get("X-Request-Id"):
        request.environ["HTTP_X_REQUEST_ID"] = str(uuid.uuid4())


class TTLCache:
    def __init__(self, ttl_seconds: int = 60):
        self.ttl = ttl_seconds
        self.store = {}

    def get(self, key: str):
        now = time.time()
        if key in self.store:
            value, exp = self.store[key]
            if exp > now:
                return value
            else:
                del self.store[key]
        return None

    def set(self, key: str, value: Any):
        self.store[key] = (value, time.time() + self.ttl)


def _normalize_to_tuple(resp: Any):
    """
    Normalize any Flask return into (body:str, status:int, headers:dict).
    Ensures we ONLY cache strings (JSON) and always return a proper Response.
    """
    if isinstance(resp, Response):
        return resp.get_data(as_text=True), resp.status_code, dict(resp.headers)

    if isinstance(resp, tuple):
        if len(resp) == 3:
            body, status, headers = resp
        elif len(resp) == 2:
            body, status = resp
            headers = {}
        else:
            body, status, headers = resp, 200, {}
        if isinstance(body, Response):
            body = body.get_data(as_text=True)
        if not isinstance(body, str):
            body = json.dumps(body)
        return body, int(status), dict(headers)

    # Plain dict/list/primitive
    if isinstance(resp, (dict, list)):
        return json.dumps(resp), 200, {}
    return str(resp), 200, {}


def cached(ttl: int = 60):
    """Cache GET endpoints via Redis (if configured) or in-process TTL fallback."""

    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from .extensions import redis_client

            cache_key = f"cache:{fn.__name__}:{request.full_path}"
            client = redis_client.client

            # Redis path
            if client:
                hit = client.get(cache_key)
                if hit:
                    r = make_response(hit, 200)
                    if not r.headers.get("Content-Type"):
                        r.headers["Content-Type"] = "application/json"
                    r.headers["X-Cache"] = "HIT"
                    return r

                resp = fn(*args, **kwargs)
                body, status, headers = _normalize_to_tuple(resp)
                client.setex(cache_key, ttl, body)
                r = make_response(body, status)
                # copy headers except content-length
                for k, v in headers.items():
                    if str(k).lower() == "content-length":
                        continue
                    r.headers[k] = v
                if not r.headers.get("Content-Type"):
                    r.headers["Content-Type"] = "application/json"
                r.headers["X-Cache"] = "MISS"
                return r

            # Local TTL fallback
            if not hasattr(wrapper, "_local_cache"):
                wrapper._local_cache = TTLCache(ttl)

            hit = wrapper._local_cache.get(cache_key)
            if hit:
                r = make_response(hit, 200)
                if not r.headers.get("Content-Type"):
                    r.headers["Content-Type"] = "application/json"
                r.headers["X-Cache"] = "HIT"
                return r

            resp = fn(*args, **kwargs)
            body, status, headers = _normalize_to_tuple(resp)
            wrapper._local_cache.set(cache_key, body)
            r = make_response(body, status)
            for k, v in headers.items():
                if str(k).lower() == "content-length":
                    continue
                r.headers[k] = v
            if not r.headers.get("Content-Type"):
                r.headers["Content-Type"] = "application/json"
            r.headers["X-Cache"] = "MISS"
            return r

        return wrapper

    return decorator

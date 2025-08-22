from flask import Blueprint, jsonify, request
from app.services.job_service import JobService

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.route("/", methods=["GET"])
def list_jobs():
    jobs = JobService.list_jobs()
    return jsonify(jobs), 200


@jobs_bp.route("/<job_id>", methods=["GET"])
def get_job(job_id):
    job = JobService.get_job(job_id)
    if job:
        return jsonify(job), 200
    else:
        return jsonify({"error": "Job not found"}), 404


@jobs_bp.route("/", methods=["POST"])
def create_job():
    data = request.json
    job = JobService.create_job(data)
    return jsonify(job), 201

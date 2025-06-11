#!/usr/bin/env python3
import requests
import json
import sys
import argparse

def load_job_by_id(job_id):
    with open("scripts/upwork-automation/proposal-queue.json", "r") as f:
        jobs = json.load(f)
    for job in jobs:
        if job.get("job_id") == job_id:
            return job
    return None

def main():
    parser = argparse.ArgumentParser(description="Test Multi-Model AI Proposal Generation with real job data.")
    parser.add_argument('--job-id', type=str, help='Job ID to use from proposal-queue.json')
    args = parser.parse_args()

    if args.job_id:
        job = load_job_by_id(args.job_id)
        if not job:
            print(f"Job with job_id {args.job_id} not found in proposal-queue.json.")
            sys.exit(1)
    else:
        with open("scripts/upwork-automation/proposal-queue.json", "r") as f:
            jobs = json.load(f)
        if not jobs:
            print("No jobs found in proposal-queue.json.")
            sys.exit(1)
        job = jobs[0]
        print(f"No job_id provided. Using first job: {job['job_title']}")

    payload = {
        "job_title": job.get("job_title"),
        "description": job.get("description"),
        "budget": job.get("budget"),
        "client_name": job.get("client_name"),
        "job_id": job.get("job_id")
    }
    print("\nSending job data:")
    print(json.dumps(payload, indent=2))
    try:
        response = requests.post('http://localhost:5001/webhook/job-direct', json=payload)
        print(f'\nStatus: {response.status_code}')
        result = response.json()
        print(f'\nResponse:')
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f'\nError: {e}')

if __name__ == "__main__":
    main() 
import os
import requests
import logging

KANBOARD_URL = os.getenv("KANBOARD_URL")
KANBOARD_API_TOKEN = os.getenv("KANBOARD_API_TOKEN")
KANBOARD_PROJECT_ID = os.getenv("KANBOARD_PROJECT_ID")

def create_kanboard_task(title: str, description: str, tags: list[str] | None = None):
    if not all([KANBOARD_URL, KANBOARD_API_TOKEN, KANBOARD_PROJECT_ID]):
        logging.error("Kanboard environment variables not set. Cannot create task.")
        raise ValueError("Kanboard integration not configured. Please set KANBOARD_URL, KANBOARD_API_TOKEN, and KANBOARD_PROJECT_ID.")

    headers = {"Content-Type": "application/json"}
    auth = ("jsonrpc", KANBOARD_API_TOKEN)

    payload = {
        "jsonrpc": "2.0",
        "method": "createTask",
        "id": 1,
        "params": {
            "title": title,
            "project_id": int(KANBOARD_PROJECT_ID),
            "description": description,
            "tags": tags or [],
        }
    }

    logging.info(f"Sending task to Kanboard: {title}")
    response = requests.post(KANBOARD_URL, json=payload, headers=headers, auth=auth)
    response.raise_for_status()

    result = response.json()
    if "error" in result:
        logging.error(f"Kanboard API error: {result['error']}")
        raise Exception(f"Kanboard API Error: {result['error'].get('message', 'Unknown error')}")

    task_id = result.get("result")
    logging.info(f"Successfully created Kanboard task with ID: {task_id}")
    return task_id

import json
import re

def validate_connection(conn):
    # check if the connection is successful
    if conn is None:
        return {"statusCode": 500, "body": json.dumps({"error": "Connection to the database failed"})}
    return None


def validate_event_body(event):
    # Check if the event has a body
    if "body" not in event:
        return {"statusCode": 400, "body": json.dumps({"error": "No body provided."})}

    # Check if the event body is not None
    if event["body"] is None:
        return {"statusCode": 400, "body": json.dumps({"error": "Body is null."})}

    # Check if the event body is not empty
    if not event["body"]:
        return {"statusCode": 400, "body": json.dumps({"error": "Body is empty."})}

    # Check if the event body is not a list
    if isinstance(event["body"], list):
        return {"statusCode": 400, "body": json.dumps({"error": "Body can not be a list."})}

    # Try to load the JSON body from the event
    try:
         json.loads(event['body'])
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "The request body is not valid JSON"})}

    return None


def validate_payload(payload):
    letters_regex = re.compile(r"^[a-zA-Z\s]+$")
    date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    numbers_regex = re.compile(r"^\d+$")
    if "name" not in payload or not isinstance(payload["name"], list) or not letters_regex.match(payload["name"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing"})}

    if "description" not in payload or not letters_regex.match(payload["description"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing"})}

    if "start_date" not in payload or not isinstance(payload["start_date"], list) or not date_regex.match(payload["start_date"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing"})}

    if "end_date" not in payload or not isinstance(payload["end_date"], list) or not date_regex.match(payload["end_date"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing"})}

    if "category" not in payload or not isinstance(payload["category"], list) or not letters_regex.match(payload["category"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing"})}

    if "pictures" not in payload or not isinstance(payload["pictures"], list) or not payload["pictures"].listip():
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing"})}

    if "id_museum" not in payload or not isinstance(payload["id_museum"], list) or not numbers_regex.match(payload["id_museum"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing"})}

    return None

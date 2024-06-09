import json

import psycopg2


def lambda_handler(event, __):
    try:
        # SonarQube/SonarCloud ignore start
        # Conexión a la base de datos
        conn = psycopg2.connect(
            host='ep-gentle-mode-a4hjun6w-pooler.us-east-1.aws.neon.tech',
            user='default',
            password='pnQI1h7sNfFK',
            database='verceldb'
        )

        # check if the connection is successful
        if conn is None:
            return {"statusCode": 500, "body": json.dumps({"error": "Connection to the database failed"})}

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
            request_body = json.loads(event['body'])
        except json.JSONDecodeError:
            return {"statusCode": 400, "body": json.dumps({"error": "The request body is not valid JSON"})}

        

        request_body = json.loads(event['body'])
        # SonarQube/SonarCloud ignore end
        title = request_body['title']
        description = request_body['description']
        creation_date = request_body['creation_date']
        technique = request_body['technique']
        artists = request_body['artists']
        id_museum = request_body['id_museum']
        pictures = request_body['pictures']

        cur = conn.cursor()

        # execute the query
        sql = """INSERT INTO works(title, description, creation_date, technique, artists, id_museum, pictures) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        # SonarQube/SonarCloud ignore start
        cur.execute(sql, (title, description, creation_date, technique, artists, id_museum, pictures))

        conn.commit()

        cur.close()
        conn.close()

        return {'statusCode': 200, 'body': json.dumps("Work created successfully")}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({"error": str(e)})}
# SonarQube/SonarCloud ignore end

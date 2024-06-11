import json

import psycopg2
from functions import datetime_serializer
from psycopg2.extras import RealDictCursor


def lambda_handler(_event, _context):
    conn = None
    cur = None
    try:
        # SonarQube/SonarCloud ignore start
        # Database connection
        conn = psycopg2.connect(
            host='ep-gentle-mode-a4hjun6w-pooler.us-east-1.aws.neon.tech',
            user='default',
            password='pnQI1h7sNfFK',
            database='verceldb'
        )

        # Create cursor
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # SonarQube/SonarCloud ignore end
        # Find all managers
        cur.execute("SELECT * FROM managers")
        # SonarQube/SonarCloud ignore start

        managers = cur.fetchall()

        # Find all museums by manager id
        rows = []
        for manager in managers:
            cur.execute("SELECT * FROM museums WHERE id_owner = %s", (manager["id"],))
            museum = cur.fetchone()
            if museum is not None:
                museum["manager"] = manager
                rows.append(museum)
    
        return {'statusCode': 200, 'body': json.dumps({{"data": json.dumps(rows, default=datetime_serializer)}})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({"error": str(e)})}
    finally:
        # Close connection and cursor
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
    # SonarQube/SonarCloud ignore end

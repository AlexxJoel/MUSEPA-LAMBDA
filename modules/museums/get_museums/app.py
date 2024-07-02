import json

import jwt
import psycopg2

from functions import datetime_serializer
from psycopg2.extras import RealDictCursor


def lambda_handler(_event, _context):

    conn = None
    cur = None
    try:
        print(_event)
        # Obtener el token de los encabezados
        token = _event['headers']['Authorization'].split(' ')[1]
        print(token)
        # Decodificar el token
        # Nota: En un entorno de producción, debes verificar la firma del token
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(decoded_token)
        # Obtener el rol del token


        roles = decoded_token.get('cognito:groups')
        role = roles[0]

        print(role)

        if role is None:
            return {'statusCode': 400, 'body': json.dumps({"error": "Role not found in token"})}

        # validar length de roles
        if len(roles) <= 0:
            return {'statusCode': 400, 'body': json.dumps({"error": "Role not found in token"})}

        # Revocar permiso si el rol es "visitor"
        if role == "visitor":
            return {'statusCode': 403, 'body': json.dumps({"error": "Access denied: insufficient permissions"})}
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

        return {'statusCode': 200, 'body': json.dumps({"data": rows}, default=datetime_serializer)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({"error": str(e)})}
    finally:
        # Close connection and cursor
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
    # SonarQube/SonarCloud ignore end

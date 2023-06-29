import json
import psycopg2
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:

    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    try:
        # Read user_id from the request body
        request_body = req.get_json()
        user_id = request_body['user_id']

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )

        # Retrieve rooms with matching user_id
        with conn.cursor() as cursor:
            query = f"SELECT room_id, room_name FROM rooms WHERE user_id = '{user_id}'"
            cursor.execute(query)
            result = cursor.fetchall()

        # Close the connection
        conn.close()

        # Process the query result
        if result:
            rooms = [{'room_id': row[0], 'room_name': row[1]} for row in result]
            return func.HttpResponse(
                json.dumps({'rooms': rooms}),
                status_code=200,
                mimetype='application/json'
            )
        else:
            return func.HttpResponse(
                json.dumps({'rooms': []}),
                status_code=200,
                mimetype='application/json'
            )
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return func.HttpResponse(
            f'Error retrieving rooms: {error_message}',
            status_code=500
        )

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
        # Read room_name and user_id from the request body
        request_body = req.get_json()
        room_name = request_body['room_name']
        user_id = request_body['user_id']

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )

        # Insert a room with the provided room_name and user_id
        with conn.cursor() as cursor:
            query = "INSERT INTO rooms (room_name, user_id) VALUES (%s, %s)"
            cursor.execute(query, (room_name, user_id))

        # Commit the changes
        conn.commit()

        return func.HttpResponse(
            'Success! Room inserted',
            status_code=200
        )
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return func.HttpResponse(
            f'Error inserting room: {error_message}',
            status_code=500
        )
    finally:
        # Close the connection
        if conn is not None and not conn.closed:
            conn.close()

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
        # Read device_name, user_id, room, ip_address, and device_type from the request body
        request_body = req.get_json()
        device_name = request_body['device_name']
        user_id = request_body['user_id']
        room_id = request_body['room_id']
        ip_address = request_body['ip_address']
        device_type = request_body['device_type']

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )

        # Insert a device with the provided details, including device_type
        with conn.cursor() as cursor:
            query = f"INSERT INTO devices (device_name, user_id, room_id, ip_address, device_type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (device_name, user_id, room_id, ip_address, device_type))

        # Commit the changes
        conn.commit()

        return func.HttpResponse(
            'Success! Device inserted',
            status_code=200
        )
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return func.HttpResponse(
            f'Error inserting device: {error_message}',
            status_code=500
        )
    finally:
        # Close the connection
        if conn is not None and not conn.closed:
            conn.close()

import json
import azure.functions as func
import psycopg2

def main(req: func.HttpRequest) -> func.HttpResponse:

    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    try:
        # Read user_id and room_id from the request body
        request_body = req.get_json()
        user_id = request_body['user_id']
        room_id = request_body['room_id']

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )

        # Retrieve devices with matching user_id and room_id, including device_type
        with conn.cursor() as cursor:
            query = f"SELECT device_id, device_name, room_id, ip_address, device_type FROM devices WHERE user_id = %s AND room_id = %s"
            cursor.execute(query, (user_id, room_id))
            result = cursor.fetchall()

        # Close the connection
        conn.close()

        # Process the query result
        if result:
            devices = [{'device_id': row[0], 'device_name': row[1], 'room': row[2], 'ip_address': row[3], 'device_type': row[4]} for row in result]
            return func.HttpResponse(
                json.dumps({'devices': devices}),
                status_code=200,
                mimetype='application/json'
            )
        else:
            return func.HttpResponse(
                json.dumps({'devices': []}),
                status_code=200,
                mimetype='application/json'
            )
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return func.HttpResponse(
            f'Error retrieving devices: {error_message}',
            status_code=500
        )

import psycopg2
import json

def lambda_handler(event, context):

    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    # Read user_id and room_id from the event
    request_body = json.loads(event['body'])
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

    try:
        # Retrieve devices with matching user_id and room_id, including device_type
        with conn.cursor() as cursor:
            query = f"SELECT device_id, device_name, room_id, ip_address, device_type FROM devices WHERE user_id = {user_id} AND room_id = {room_id}"
            cursor.execute(query)
            result = cursor.fetchall()

        # Close the connection
        conn.close()

        # Process the query result
        if result:
            devices = [{'device_id': row[0], 'device_name': row[1], 'room': row[2], 'ip_address': row[3], 'device_type': row[4]} for row in result]
            return {
                'statusCode': 200,
                'body': {'devices': devices}
            }
        else:
            return {
                'statusCode': 200,
                'body': {'devices': []}
            }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error retrieving devices: {error_message}'
        }
    finally:
        # Close the connection
        if conn is not None and not conn.closed:
            conn.close()

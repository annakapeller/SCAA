import psycopg2
import json

def lambda_handler(event, context):
    
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    # Read device_name, user_id, room, ip_address, and device_type from the event
    request_body = json.loads(event['body'])
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

    try:
        # Insert a device with the provided details, including device_type
        with conn.cursor() as cursor:
            query = f"INSERT INTO devices (device_name, user_id, room_id, ip_address, device_type) VALUES ('{device_name}', {user_id}, {room_id}, '{ip_address}', '{device_type}')"
            cursor.execute(query)

        # Commit the changes
        conn.commit()

        return {
            'statusCode': 200,
            'body': 'Success! Device inserted'
        }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error inserting device: {error_message}'
        }
    finally:
        # Close the connection
        conn.close()

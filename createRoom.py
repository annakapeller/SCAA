import psycopg2
import json

def lambda_handler(event, context):
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    # Read room_name and user_id from the event
    request_body = json.loads(event['body'])
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

    try:
        # Insert a room with the provided room_name and user_id
        with conn.cursor() as cursor:
            query = f"INSERT INTO rooms (room_name, user_id) VALUES ('{room_name}', {user_id})"
            cursor.execute(query)

        # Commit the changes
        conn.commit()

        return {
            'statusCode': 200,
            'body': 'Success! Room inserted'
        }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error inserting room: {error_message}'
        }
    finally:
        # Close the connection
        conn.close()
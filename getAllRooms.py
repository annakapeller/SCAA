import psycopg2
import json

def lambda_handler(event, context):
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    # Read user_id from the event
    request_body = json.loads(event['body'])
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
            return {
                'statusCode': 200,
                'body': {'rooms': rooms}
            }
        else:
            return {
                'statusCode': 200,
                'body': {'rooms': []}
            }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error retrieving rooms: {error_message}'
        }
    finally:
        # Close the connection
        if conn is not None and not conn.closed:
            conn.close()

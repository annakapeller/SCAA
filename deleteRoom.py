import psycopg2
import json

def lambda_handler(event, context):
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    # Read room_id from the event
    request_body = json.loads(event['body'])
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
        # Delete the room with the provided room_id
        with conn.cursor() as cursor:
            query = f"DELETE FROM rooms WHERE room_id = {room_id} RETURNING *"
            cursor.execute(query)

            # Get the number of rows deleted
            num_rows_deleted = cursor.rowcount

        # Commit the changes
        conn.commit()

        return {
            'statusCode': 200,
            'body': f'Success! {num_rows_deleted} room(s) deleted'
        }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error deleting room: {error_message}'
        }
    finally:
        # Close the connection
        conn.close()

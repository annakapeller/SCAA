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
        # Read device_id from the request body
        request_body = req.get_json()
        device_id = request_body['device_id']

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )

        # Delete the device with the provided device_id
        with conn.cursor() as cursor:
            query = "DELETE FROM devices WHERE device_id = %s RETURNING *"
            cursor.execute(query, (device_id,))

            # Get the number of rows deleted
            num_rows_deleted = cursor.rowcount

        # Commit the changes
        conn.commit()

        return func.HttpResponse(
            f'Success! {num_rows_deleted} device(s) deleted',
            status_code=200
        )
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return func.HttpResponse(
            f'Error deleting device: {error_message}',
            status_code=500
        )
    finally:
        # Close the connection
        if conn is not None and not conn.closed:
            conn.close()

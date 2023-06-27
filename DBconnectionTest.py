import psycopg2
import json

def lambda_handler(event, context):
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'
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

    # Execute a test query
    query = "SELECT * FROM users LIMIT 1"
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    
    # Close the connection
    conn.close()

    # Process the query result
    if result:
        return {
            'statusCode': 200,
            'body': json.dumps(event)#f'Success! Retrieved row: {result}'
        }
    else:
        return {
            'statusCode': 500,
            'body': 'Error: No rows found'
        }
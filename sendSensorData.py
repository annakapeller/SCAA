import psycopg2
import json

def insertSensorData(event):
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    
    sns_message = event['Records'][0]['Sns']['Message']
    message = json.loads(sns_message)
    ip_address = message['ip_address']
    attribute = message['attribute']
    value = message['value']
    unit = message['unit']
    """
    request_body = json.loads(event['body'])
    ip_address = request_body.get('ip_address')
    attribute = request_body.get('attribute')
    value = request_body.get('value')
    unit = request_body.get('unit')
    """
    
    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database_name
    )

    try:
        # Insert sensor data into the sensor_data table
        with conn.cursor() as cursor:
            query = f"INSERT INTO sensor_data (ip_address, attribute, value, unit) VALUES ('{ip_address}', '{attribute}', {value}, '{unit}')"
            cursor.execute(query)

        # Commit the changes
        conn.commit()

        return {
            'statusCode': 200,
            'body': 'Success! Sensor data inserted'
        }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error inserting sensor data: {error_message}'
        }
    finally:
        # Close the connection
        conn.close()

def lambda_handler(event, context):
    return insertSensorData(event)

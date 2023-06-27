import psycopg2
import json
from decimal import Decimal
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def getSensorData(device_id):
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database_name
    )

    try:
        # Query the devices table to retrieve the IP address for the specified device_id
        with conn.cursor() as cursor:
            query = f"SELECT ip_address FROM devices WHERE device_id = {device_id}"
            cursor.execute(query)
            ip_address = cursor.fetchone()[0]

        # Query the sensor_data table to retrieve the specified fields (attribute, value, unit, timestamp) and sort by timestamp
        with conn.cursor() as cursor:
            sensor_data_query = f"SELECT attribute, value, unit, timestamp FROM sensor_data WHERE ip_address = '{ip_address}' ORDER BY timestamp"
            cursor.execute(sensor_data_query)
            sensor_data = cursor.fetchall()

        # Group sensor data by attribute
        grouped_data = {}
        for data in sensor_data:
            attribute = data[0]
            value = data[1]
            unit = data[2]
            timestamp = data[3]

            if attribute not in grouped_data:
                grouped_data[attribute] = []

            grouped_data[attribute].append({
                'value': value,
                'unit': unit,
                'timestamp': timestamp
            })

        # Prepare the response containing the grouped sensor data
        response_body = {
            'device_id': device_id,
            'ip_address': ip_address,
            'sensor_data': grouped_data
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response_body, cls=CustomEncoder)
        }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error retrieving device information and sensor data: {error_message}'
        }
    finally:
        # Close the connection
        conn.close()

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    device_id = request_body.get('device_id')
    return getSensorData(device_id)

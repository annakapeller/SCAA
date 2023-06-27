import psycopg2
import json

def lambda_handler(event, context):
    # RDS Aurora PostgreSQL database connection details
    host = '162.55.45.241'
    port = 5432
    username = 'postgres'
    password = '12345'
    database_name = 'testDB'

    # Read payload from the event
    payload = json.loads(event['body'])

    # Extract values from the payload
    filtration_level = payload['filtrationLevel']
    energy_consumption_level = payload['energyConsumptionLevel']
    led_lights_mode = payload['LEDLightsMode']
    quiet_mode = payload['quietMode']
    child_lock = payload['childLock']

    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database_name
    )

    try:
        # Update the first row with id 1 in the purifier_settings table
        with conn.cursor() as cursor:
            query = f"UPDATE purifier_settings SET filtrationLevel = {filtration_level}, energyConsumptionLevel = {energy_consumption_level}, LEDLightsMode = {led_lights_mode}, quietMode = {quiet_mode}, childLock = {child_lock} WHERE id = 1"
            cursor.execute(query)

        # Commit the changes
        conn.commit()

        return {
            'statusCode': 200,
            'body': 'Settings updated successfully'
        }
    except psycopg2.Error as e:
        # An error occurred during the query execution
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': f'Error updating settings: {error_message}'
        }
    finally:
        # Close the connection
        if conn is not None and not conn.closed:
            conn.close()

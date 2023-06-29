import json
import urllib.request
import logging

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Read payload from the request body
        payload = json.loads(req.get_body().decode('utf-8'))

        # Extract device type and settings from the payload
        device_type = payload['deviceType']
        settings = payload['settings']

        # Define the URL endpoints based on device type
        url = ""
        if device_type == "Purifier":
            url = "https://qhkgpnxtczb5s24wjd5sxngjcm0hofox.lambda-url.us-east-1.on.aws/"
        elif device_type == "Humidifier":
            url = "https://w24yeoz24a7jglqt3xagtcewbi0njsnq.lambda-url.us-east-1.on.aws/"
        else:
            return func.HttpResponse('Invalid device type', status_code=400)

        # Send the settings payload to the respective URL
        req = urllib.request.Request(url, data=json.dumps(settings).encode('utf-8'), method='POST')
        req.add_header('Content-Type', 'application/json')

        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return func.HttpResponse('Settings updated successfully', status_code=200)
            else:
                return func.HttpResponse('Error updating settings', status_code=500)

    except Exception as e:
        logging.exception('An error occurred')
        return func.HttpResponse(f'Error: {str(e)}', status_code=500)

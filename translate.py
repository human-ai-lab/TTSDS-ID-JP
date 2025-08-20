import requests, uuid, json, os
from dotenv import load_dotenv

def translate_text_to_japanese(text):
    load_dotenv()
    
    key = os.getenv('API_KEY')
    endpoint = os.getenv('ENDPOINT')
    location = os.getenv('LOCATION')
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'id',
        'to': 'ja'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    # Make the API request
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = response[0]["translations"][0]["text"]
    return translated_text

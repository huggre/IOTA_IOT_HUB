from requests import post
import json

def call_service(endpoint, token, service_tech_name, service_data):
    tech_name_list = service_tech_name.split(".")
    url = endpoint + '/api/services/' + tech_name_list[0] + '/' + tech_name_list[1]

    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }

    response = post(url, headers=headers, data=service_data)

    return response


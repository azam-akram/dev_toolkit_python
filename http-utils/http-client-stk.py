import requests
import json

def make_get_request(url, token):
    try:
        limit = 10
        offset = 2
        api_header = {'Authorization': f'bearer {token}', 'Accept': 'application/json'}
        params = {'limit': {limit}, 'offset': offset}
        response = requests.get(f"{url}", headers=api_header, params=params)

        print(f"Request URL: {response.request.url}")
        print(f'Received GET response from {response.url}')

        if response.status_code == 200:
            print('Resource retrieved successfully')
            prtefied_response = json.dumps(response.json(), indent=2)
            print(prtefied_response)
        else:
            print('Failed to retrieve resource')
    except requests.RequestException as e:
        print(f"GET request failed: {e}")

def make_post_request():
        try:
            url = "https://example.com"
            token = "test-token"

            api_header = {'Authorization': f'bearer {token}', 'Accept': 'application/json'}
            data = {'name': 'test-name', 'email': 'test@example.com'}

            # Make the POST request
            response = requests.post(url, json=data, headers=api_header)

            # Print the actual HTTP request URL
            print(f"Request URL: {response.request.url}")

            # Check the response status code
            if response.status_code == 201:
                print('Resource created successfully')
                print(response.json())
            else:
                print('Failed to create resource')
        except requests.RequestException as e:
            print(f"POST request failed: {e}")

def make_put_request(url, token, data):
    try:
        api_header = {'Authorization': f'bearer {token}', 'Accept': 'application/json'}

        # Make the PUT request
        response = requests.put(url, json=data, headers=api_header)

        # Print the actual HTTP request URL
        print(f"Request URL: {response.request.url}")

        # Check the response status code
        if response.status_code == 200:
            print('Resource updated successfully')
            print(response.json())
        else:
            print('Failed to update resource')
    except requests.RequestException as e:
        print(f"PUT request failed: {e}")


def make_delete_request(url, token, resource_id):
    try:
        api_header = {'Authorization': f'bearer {token}', 'Accept': 'application/json'}

        # Construct the URL with the resource ID
        delete_url = f"{url}/{resource_id}"

        # Make the DELETE request
        response = requests.delete(delete_url, headers=api_header)

        # Print the actual HTTP request URL
        print(f"Request URL: {response.request.url}")

        # Check the response status code
        if response.status_code == 204:
            print('Resource deleted successfully')
        else:
            print('Failed to delete resource')
    except requests.RequestException as e:
        print(f"DELETE request failed: {e}")

if __name__ == "__main__":
    #make_post_request()

    #url = "https://example.com"
    #token = "test-token"
    #data = {'name': 'test-name', 'email': 'test@example.com'}
    #make_put_request(url, token, data)
     

    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    token = "test-token"
    make_get_request(url, token)
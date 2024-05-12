import requests
import os
import json

class DemoHTTPClient:
    def __init__(self):
        self.configs = {}

    def load_config(self, config):
        """Load configuration from file."""
        try:
            home_dir = os.path.expanduser("~")
            file_path = f'{home_dir}{config}'
            with open(file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON in file '{file_path}'.")

    def make_get_request(self):
        """Make GET request."""
        try:
            url = self.configs['my-cool-api-config']['url']
            token = self.configs['my-cool-api-config']['token']

            api_headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
            api_params = {'offset': 0, 'limit': 10}

            with requests.Session() as session:
                """ 
                Use requests.Session() to leverage session management and connection pooling, 
                which can improve performance if you're making multiple requests to the same host.
                """
                response = session.get(url, headers=api_headers, params=api_params)
                print(f"GET request to {url} with params {api_params} completed with status code {response.status_code}")

                response.raise_for_status()
                """
                Use response.raise_for_status() to raise an exception for bad responses (status codes 4xx and 5xx), simplifying error handling.
                """
                res = response.json()
                print(json.dumps(res, indent=4))
                print(f'Current BTC price (USD): {res["bpi"]["USD"]["rate"]}')
                print(f'Current BTC price (GBP): {res["bpi"]["GBP"]["rate"]}')
                print(f'Current BTC price (EUR): {res["bpi"]["EUR"]["rate"]}')
        except (requests.RequestException, FileNotFoundError, ValueError) as e:
            print(f"GET request failed: {e}")

if __name__ == "__main__":
    http_client = DemoHTTPClient()
    http_client.configs = http_client.load_config('/work/python/utils-python/http-utils/configs/configs.json')

    http_client.make_get_request()

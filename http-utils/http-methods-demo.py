import requests
import json

def handle_get_response(resGet, *args, **kwargs):
  print(f'Received GET response')
  print(f'{resGet.status_code} - {resGet.url}')  
  
  if resGet.status_code == 200:
    print('Resource retrieved successfully')
    resJson = resGet.json()
    print(resJson)
  else:
    print('Failed to retrieve resource')
    
#def get_method_demo():
id = "test-id"
jwt = "sdhfjhdkfhsdkfhsdlfhdlfhshdkfsdlfhlsd"
headers = {
  "Content-Type": "application/json",
  "Accept": "application/json",
  "Authorization": f'Bearer {jwt}',
}
url = "https://example.com/v1/resource"
hooks = {'response': handle_get_response}

print(f'GET Request URL: {url}{id}')
resGet = requests.get(f"{url}{id}", hooks=hooks, headers=headers)

#get_method_demo()
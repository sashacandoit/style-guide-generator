import requests
# from api_keys import GOOGLE_API_KEY


# res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyD3VmBcNb6qLT6a5SiR3I9iIIdUK7YV600')
res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params={"key": 'AIzaSyD3VmBcNb6qLT6a5SiR3I9iIIdUK7YV600'})


data = res.json()

# for item in data['items']:
#     print(item['family'])
#     # print(item['variants'])
#     print(item['files'])


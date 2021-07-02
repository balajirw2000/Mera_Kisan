import requests

url = "FASTSMS_URL"

querystring = {"authorization":"Your_AUTH_KEY","message":"This is test message","language":"english","route":"q","numbers":"contact_number"}

headers = {
    'cache-control': "no-cache"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

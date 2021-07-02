import requests

url = "https://www.fast2sms.com/dev/bulkV2"

querystring = {"authorization":"GPhaYo5Xmngz9WudTE6HJIMLfrDwtpkOKiZF7qb8VcjCxNA3sl4tXkvEKbyQPdh6zwLDIqABH23TVFmR","message":"This is test message","language":"english","route":"q","numbers":"9167386883"}

headers = {
    'cache-control': "no-cache"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
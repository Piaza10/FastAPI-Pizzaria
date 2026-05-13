import requests

import requests

header = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzc5MjE1NTQ5fQ.5B8aivSPaDOJWQw8JGZJNbjGjceAmnxfQRZj0citePc"
}

requisicao = requests.get(
    "http://127.0.0.1:8000/auth/refresh",
    headers=header
)

print(requisicao.status_code)
print(requisicao.text)
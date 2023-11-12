import requests
import json

with open("config.json", "r") as fp:
    config = json.load(fp)

host = config["host"]
domain_name = config["domain_name"]
username = config["username"]
token = config["token"]

s = requests.Session()
s.headers["Authorization"] = f"Token {token}"

response = s.get(
    f"{host}/api/v0/user/{username}/consoles/",
)
assert response.status_code == 200, response.content
data = response.json()
console_id = data[0]["id"]

cmd = "git pull\n"
response = s.post(
    f"{host}/api/v0/user/{username}/consoles/{console_id}/send_input/",
    data={"input": cmd},
)
assert response.status_code == 200, response.content

response = s.get(
    f"{host}/api/v0/user/{username}/consoles/{console_id}/get_latest_output/"
)
assert response.status_code == 200, response.content

response = s.post(
    f"{host}/api/v0/user/{username}/webapps/{domain_name}/reload/",
)
assert response.status_code == 200, response.content

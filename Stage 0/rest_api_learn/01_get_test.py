import json
import requests
from utils import section, show_json, show_status

BASE_URL = "https://globalapi-test.fuioupay.com"
INFO = "/user/info"
TICKET = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxNjYxMzAwMSx3ZWIiLCJleHAiOjE3ODI0NjQ3MDEsImlhdCI6MTc4MjM3ODMwMX0.q4QdmS99CHqBKIQUR9P_BVd47iVl_JQ2lVcJJ_XpUR8itcSJNnNfiHALdjL6mwWepvB8ADW3O5cP-daCoPCafQ"

response = requests.post(f"{BASE_URL}{INFO}", data={"ticket": TICKET, "lang": "zh"})
print(f"response: {response}")
print(f"response.status_code: {response.status_code}")
print(f"response.text: \n{response.text}")

if response.status_code == 200 and response.text.strip():
    data = response.json()
    print(f"response.json(): \n{json.dumps(data, indent=2, ensure_ascii=False)}")
else:
    print(f"请求失败或响应为空，status_code: {response.status_code}")
    data = None

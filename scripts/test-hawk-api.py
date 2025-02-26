# Usage:
#   uv run test-hawk-api.py URL
#
# Example:
#   uv run test-hawk-api.py /data-lake/actual/
#
# /// script
# dependencies = [
#   "httpx",
#   "mohawk",
# ]
# ///

import sys

import httpx
from mohawk import Sender


access_key = "hawk-access-key"
secret_key = "hawk-secret-key"
url = f"http://localhost:8000{sys.argv[1]}"

sender = Sender(
    {
        "id": access_key,
        "key": secret_key,
        "algorithm": "sha256",
    },
    url,
    "GET",
    content="",
    content_type="application/json",
)
response = httpx.get(
    url,
    headers={
        "Authorization": sender.request_header,
        "Content-Type": "application/json",
    },
)

assert response.status_code == 200
print(len(response.text))

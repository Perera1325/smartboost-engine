from fastapi import Header, HTTPException, Request
from datetime import datetime

API_KEY = "smartboost123"

REQUEST_LOG = "../analytics/requests.log"

rate_limit = {}

async def verify_key(x_api_key: str = Header(...)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


async def log_request(request: Request):

    with open(REQUEST_LOG, "a") as f:
        f.write(f"{datetime.now()} | {request.client.host} | {request.url}\n")


def check_rate(ip):
    rate_limit[ip] = rate_limit.get(ip, 0) + 1

    if rate_limit[ip] > 20:
        raise HTTPException(status_code=429, detail="Too many requests")

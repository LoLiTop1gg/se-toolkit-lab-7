import httpx
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LMS_API_URL, LMS_API_KEY

async def get_items():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LMS_API_URL}/items/",
            headers={"Authorization": f"Bearer {LMS_API_KEY}"}
        )
        resp.raise_for_status()
        return resp.json()

async def get_pass_rates(lab: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LMS_API_URL}/analytics/pass-rates",
            params={"lab": lab},
            headers={"Authorization": f"Bearer {LMS_API_KEY}"}
        )
        resp.raise_for_status()
        return resp.json()

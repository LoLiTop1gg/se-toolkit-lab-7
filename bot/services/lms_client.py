import httpx
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LMS_API_URL, LMS_API_KEY

async def get_items():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/items/", headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def get_learners():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/learners/", headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def get_scores(lab: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/analytics/scores", params={"lab": lab}, headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def get_pass_rates(lab: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/analytics/pass-rates", params={"lab": lab}, headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def get_timeline(lab: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/analytics/timeline", params={"lab": lab}, headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def get_groups(lab: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/analytics/groups", params={"lab": lab}, headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def get_top_learners(lab: str, limit: int = 5):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/analytics/top-learners", params={"lab": lab, "limit": limit}, headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def get_completion_rate(lab: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_URL}/analytics/completion-rate", params={"lab": lab}, headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

async def trigger_sync():
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{LMS_API_URL}/pipeline/sync", headers={"Authorization": f"Bearer {LMS_API_KEY}"})
        resp.raise_for_status()
        return resp.json()

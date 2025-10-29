import httpx

from config import NOTIFIER_URL


async def post_success_notification(week_dates: str):
    async with httpx.AsyncClient() as client:
        payload = {
            "type": "notification",
            "message": f"Scraping of the Lidl brochures for week {week_dates} successful."
        }
        await client.post(f"{NOTIFIER_URL}/", json=payload)


async def post_error_notification():
    async with httpx.AsyncClient() as client:
        payload = {
            "type": "error",
            "message": "Scraping of the Lidl brochures errored."
        }
        await client.post(f"{NOTIFIER_URL}/", json=payload)

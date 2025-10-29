import httpx

from config import IMAGE_EXTRACTOR_URL
from logger import logger


async def send_image_links(image_links: list[str], week_dates: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "store": "Lidl",
                "dates": week_dates,
                "links": image_links,
            }
            resp = await client.post(f"{IMAGE_EXTRACTOR_URL}/extract-images", json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            logger.info("Resp from image extractor:")
            logger.info(data)
    except Exception as e:
        logger.error("Error from image extractor")
        logger.error(str(e))
        raise Exception("Error from image extractor")

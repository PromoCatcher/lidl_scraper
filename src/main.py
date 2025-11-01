import asyncio

from logger import logger
from scraper import scrape_url_links
from image_extractor_client import send_image_links
from notifier_client import post_success_notification, post_error_notification
from calculate_week_dates import get_next_week_range


def main():
    logger.info("Starting the process.")
    week_dates = get_next_week_range()
    try:
        links = scrape_url_links(week_dates)
        asyncio.run(send_image_links(links, week_dates))
    except Exception as e:
        logger.error(str(e))
        asyncio.run(post_error_notification())
        return

    logger.info("Process executed.")

    asyncio.run(post_success_notification(week_dates))


if __name__ == "__main__":
    main()
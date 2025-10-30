import re

from playwright.sync_api import sync_playwright

from logger import logger


def scrape_url_links(week_dates: str) -> list[str]:
    img_links: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        logger.info("Browser initiated.")

        # Open the website
        page.goto(f"https://www.lidl.bg/l/bg/broshura/{week_dates}/view/flyer/page/1")

        logger.info("Accept cookies")
        try:
            page.click("#onetrust-accept-btn-handler", timeout=10000)
        except Exception as e:
            logger.error(str(e))
            logger.error("Error on click on brochure")
            raise Exception("Error on click on brochure")
        
        while True:
            # Extract image links on current page
            logger.info("Start to extract images")
            images = page.query_selector_all(
                "li.page--current:not(.page--next):not(.page--pre) img.img"
            )

            for img in images:
                src = img.get_attribute("src")
                if src:
                    img_links.append(src)

            # Check stepper numbers
            stepper_text = page.inner_text("button.stepper--lidl")
            match = re.match(r"(\d+)\s*/\s*(\d+)", stepper_text)
            if match:
                current, total = int(match.group(1)), int(match.group(2))
                if current == total:
                    break

            # Click next button
            try:
                page.click(
                    "button.button.button--primary-negative.button--label-uppercase.button--bold.button--icon.button--center.button--hover-background.button--navigation.button--navigation-lidl[aria-label='Следваща страница']",
                    timeout=5000,
                )
            except Exception as e:
                logger.error(str(e))
                logger.error("Error on click on next button")
                break

            page.wait_for_timeout(3000)

        logger.info("Collected image links:")
       
        logger.info(len(img_links))

        browser.close()

    logger.info("End of scraping")

    return img_links
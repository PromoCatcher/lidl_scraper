import re

from playwright.sync_api import sync_playwright, ElementHandle

from logger import logger


def scrape_url_links(week_dates: str) -> list[str]:
    img_links: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        logger.info("Browser initiated.")

        page.goto("https://www.lidl.bg/")

        logger.info("Accept cookies")
        try:
            page.click("#onetrust-accept-btn-handler", timeout=10000)
        except Exception as e:
            logger.error(str(e))
            logger.error("Error on click on accept cookie")
            raise Exception("Error on click on accepct cookie")

        try:
            page.click("a.n-navigation__menu-nav--link.n-header__icon-link", timeout=5000)
        except Exception as e:
            logger.error(str(e))
            logger.error("Error on click on brochures link")
            raise Exception("Error on click on brochures link")

        page.wait_for_selector("a.flyer")
        a_els = page.query_selector_all("a.flyer")

        logger.info("Selected flyer elements")

        print(len(a_els))

        def find_correct_link(el: ElementHandle) -> bool:
            href = el.get_attribute("href")
            if not href:
                return False
            print(href)
            return week_dates in href

        a_el = next(filter(find_correct_link, a_els), None)

        if not a_el:
            raise Exception("No element found for the flyer for the next week!")

        logger.info("Found element for the brochure")

        brochure_link = a_el.get_attribute("href")
        if not brochure_link:
            raise Exception("No element found for the flyer for the next week!")

        # Open the website
        page.goto(brochure_link)

        logger.info("page opened")
        
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
from os import environ

from dotenv import load_dotenv


load_dotenv()


IMAGE_EXTRACTOR_URL = environ["IMAGE_EXTRACTOR_URL"]
NOTIFIER_URL = environ.get("NOTIFIER_URL")

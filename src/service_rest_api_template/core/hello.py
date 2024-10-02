import logging.config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HelloService:
    def __init__(self, hello_message: str):
        self.hello_message = hello_message

    def run(self, name: str) -> str:
        logger.info(f"Running with name: {name}")
        return f"{self.hello_message}, {name}"

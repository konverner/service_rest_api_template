import logging

from fastapi import APIRouter, HTTPException
from service_rest_api_template.api import schemas
from service_rest_api_template.core.hello import HelloService

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
hello_service = HelloService("Hello")

@router.get("/", response_model=schemas.HelloResponse)
def hello(name: str = "World"):
    try:
        message = hello_service.run(name)
        return schemas.HelloResponse(message=message)
    except Exception as e:
        logger.error(f"Error generating hello message: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

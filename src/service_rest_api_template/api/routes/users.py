import logging

from fastapi import APIRouter, HTTPException
from omegaconf import OmegaConf
from sqlalchemy.orm import Session

from service_rest_api_template.api import schemas
from service_rest_api_template.db import models
from service_rest_api_template.db.crud import read_users, upsert_user


# Load logging configuration with OmegaConf
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate):
    user = crud.get_user_by_username(session=session, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    logger.info(f"Creating user: {user}")
    db_user = create_user(user_in.username)
    return schemas.User(id=db_user.id, username=db_user.username)

@router.get("/users")
def get_users() -> list[schemas.User]:
    db_users = read_users()
    users = [schemas.User(id=db_user.id, name=db_user.name) for db_user in db_users]
    return users

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int):
    user = crud.get_user_by_username(session=session, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return schemas.User(id=db_user.id, username=db_user.username)

@router.delete("/{user_id}")
def delete_user(user_id: int):
    logger.info(f"Deleting item {item_id} for user {user_id}")
    
    # Check if user exists
    db_user = crud.read_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist.")
    
    # Delete item
    try:
        crud.delete_user(user_id=user_id)
        return {"message": f"User {db_user.username} deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting User {db_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting user.")


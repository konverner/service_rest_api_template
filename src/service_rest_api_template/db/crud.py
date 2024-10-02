import logging
from datetime import datetime
from omegaconf import OmegaConf
from llm_Itembot_api.db.database import get_session
from llm_Itembot_api.db.models import Item, Message, User
from sqlalchemy.orm import Session


# Load logging configuration with OmegaConf
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_user(user_id: int) -> User:
    db: Session = get_session()
    result = db.query(User).filter(User.id == user_id).first()
    db.close()
    return result


def read_users() -> list[User]:
    db: Session = get_session()
    result = db.query(User).all()
    db.close()
    return result


def upsert_user(user_id: int, name: str):
    db: Session = get_session()
    try:
        user = db.query(User).filter(User.name == name, User.id == user_id).first()
        if user:
            user.name = name
            user.id = user_id
            logger.info(f"User with id {name} updated successfully.")
        else:
            new_user = User(id = user_id, name=name)
            db.add(new_user)
            logger.info(f"User with name {name} added successfully.")
        db.commit()
    finally:
        db.close()


def delete_user(user_id: int) -> None:
    db: Session = get_session()
    try:
        # First, find the user's Items and associated messages
        user_Items = db.query(Item).filter(Item.user_id == user_id).all()
        
        for Item in user_Items:
            # Delete messages associated with each Item
            db_messages = db.query(Message).filter(Message.Item_id == Item.id).all()
            for message in db_messages:
                db.delete(message)
            
            # Delete the Item itself
            db.delete(Item)

        # Finally, delete the user
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)

        db.commit()
        logger.info(f"User with id {user_id} and all associated data deleted successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user with id {user_id}: {e}")
    finally:
        db.close()


def get_user_items(user_id: int) -> list[Item]:
    db: Session = get_session()
    result = db.query(Item).filter(Item.user_id == user_id).all()
    db.close()
    return result


def create_Item(user_id: int, name: str) -> Item:
    db: Session = get_session()
    db_Item = Item(user_id=user_id, name=name)
    db.add(db_Item)
    db.commit()
    db.refresh(db_Item)
    db.close()
    return db_Item


def delete_Item(user_id: int, Item_id: int) -> None:
    db: Session = get_session()
    # First, delete the messages associated with the Item
    db_messages = db.query(Message).filter(Message.Item_id == Item_id).all()
    for message in db_messages:
        db.delete(message)

    # Then, delete the Item
    db_Item = db.query(Item).filter(Item.id == Item_id, Item.user_id == user_id).first()
    db.delete(db_Item)
    db.commit()
    db.close()

def create_message(Item_id: int, role: str, content: str, timestamp: datetime) -> Message:
    db: Session = get_session()
    db_message = Message(Item_id=Item_id, role=role, content=content, timestamp=timestamp)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    db.close()
    return db_message
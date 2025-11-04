from sqlalchemy.orm import Session

# GOOD
from . import models
from . import schemas
from . import security


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_post(db: Session, post: schemas.PostCreate, owner_id: int):
    db_post = models.Post(**post.model_dump(), owner_id=owner_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate, owner_id: int):
    # Only fetch posts owned by the current user to enforce ownership checks.
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == owner_id).first()
    if not db_post:
        return None

    update_data = post_update.model_dump(exclude_unset=True)
    # Apply only the fields included in the update payload.
    for field, value in update_data.items():
        setattr(db_post, field, value)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

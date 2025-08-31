# app/crud/post.py
from sqlmodel import Session, select
from app.models.post import Post, PostCreate

def create_post(session: Session, post: PostCreate) -> Post:
    db_post = session.exec(
        select(Post).where(Post.title == post.title)
    ).first()

    if db_post:
        raise ValueError(f"Post with title {post.title} already exists")
    db_post = post
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

def get_posts(session: Session) -> list[Post]:
    return session.exec(select(Post)).all()

def get_post(session: Session, post_id: int) -> Post | None:
    return session.get(Post, post_id)

def update_post(session: Session, post_id: int, post_update: PostCreate) -> Post | None:
    db_post = session.get(Post, post_id)
    if db_post:
        post_data = post_update.dict(exclude_unset=True)
        for key, value in post_data.items():
            setattr(db_post, key, value)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
    return db_post

def delete_post(session: Session, post_id: int) -> bool:
    post = session.get(Post, post_id)
    if post:
        session.delete(post)
        session.commit()
        return True
    return False

def get_all_posts(session: Session) -> list[Post]:
    return session.exec(select(Post)).all()
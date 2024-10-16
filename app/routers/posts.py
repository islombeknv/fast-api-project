from fastapi import HTTPException, status, Depends, APIRouter, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user), 
                    limit:int = 10, skip: int = 0, 
                    search: Optional[str] = ''):

    result = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()
    
    if not result:
        raise HTTPException(detail="post does not exits", status_code=status.HTTP_404_NOT_FOUND)

    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * ;""", (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    owner_id = current_user.id
    new_post = models.Post(owner_id=owner_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post:
        return post
    
    raise HTTPException(detail="no data", status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),)) 
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_quary = db.query(models.Post).filter(models.Post.id == id)
    post = post_quary.first()
    if post is None:
        raise HTTPException(detail="post does not exits", status_code=status.HTTP_404_NOT_FOUND)
    
    if post.owner_id != current_user.id:
        raise HTTPException(detail="post does not exits you cretaed", status_code=status.HTTP_403_FORBIDDEN)
    
    post_quary.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


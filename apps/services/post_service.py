from dataclasses import asdict
from fastapi import HTTPException
from sqlmodel import (
    Session, select
)
from enum import Enum
import time
from apps.dependencies.tables import Posts
from apps.models.post import *


class RESULT_CODE(Enum):
    NOT_FOUND = "Not Found"
    FAILED = "Failed"
    SUCCESS = "success"

class PostService:
    def get_post(self, db: Session, sReq: sPostReq, view: int=1):
        
        post = db.get(Posts, sReq.post_id)

        if not post:
            return RESULT_CODE.NOT_FOUND.value
        if post.published == False and sReq.user_id != post.user_id:
            return RESULT_CODE.FAILED.value
        try:
            post.views = post.views + view
            db.add(post)
            db.commit()
            db.refresh(post)
        except Exception as e:
            print(e)
        return {
            "post_id": post.post_id, 
            "user_id": post.user_id, 
            "category": post.category,
            "title": post.title, 
            "content": post.content, 
            "created_at": post.created_at,
            "published": post.published
        }

    def get_posts(self, db: Session, page: int=1, limit: int=10, category: str=None):
        if page < 1:
            page = 1
        if limit < 1:
            return []
        try:
            nOffset = (page - 1) * limit

            query = select(Posts)


            if category and category != "전체":
                query = query.where(Posts.category == category)


            famousPosts_query = query.order_by(Posts.views.desc()).limit(3)
            famousPosts = db.exec(famousPosts_query).all()
            
            posts_query = query.order_by(Posts.post_id.desc()).offset(nOffset).limit(limit)
            posts = db.exec(posts_query).all()

            if not posts:
                return PostsResp(famousPosts=[], posts=[], err_str="해당 페이지에 게시글이 없습니다.")

            return PostsResp(famousPosts=famousPosts, posts=posts)

        except Exception as e:
            return PostsResp(famousPosts=[], posts=[], err_str=f"서버 오류: {str(e)}")
        
    def get_posts_query(self, db: Session, page: int=1, limit: int=10, category: str=None, query: str=None):
        # 검색에 검색어 입력 시 사용할 함수(query라는 검색어 추가)
        if page < 1:
            page = 1
        if limit < 1:
            return []
        try:
            nOffset = (page - 1) * limit

            SQLquery = select(Posts)
            
            
            if category and category != "전체":
                SQLquery = SQLquery.where(Posts.category == category)
            
            famousPosts_query = SQLquery.order_by(Posts.views.desc()).limit(3)
            famousPosts = db.exec(famousPosts_query).all()

            if query:
                SQLquery = SQLquery.where(Posts.title.contains(query) | Posts.content.contains(query))
            
            posts_query = SQLquery.offset(nOffset).limit(limit).order_by(Posts.post_id.desc())
            posts = db.exec(posts_query).all()
    
            if not posts:
                return PostsResp(famousPosts=[], posts=[], err_str="해당 페이지에 게시글이 없습니다.")

            return PostsResp(famousPosts=famousPosts, posts=posts)
        except Exception as e:
            return PostsResp(famousPosts=[], posts=[], err_str=f"서버 오류: {str(e)}")


    def create_post(self, db:Session, cPost: CreatePostReq) -> RESULT_CODE:
        try:
            postModel = Posts()
            postModel.user_id = cPost.user_id
            postModel.category = cPost.category
            postModel.title = cPost.title
            postModel.content = cPost.content
            postModel.created_at = int(time.time())
            postModel.published = cPost.published
            postModel.views = 0
            db.add(postModel)
            db.commit()
            db.refresh(postModel)
        except Exception as e:
            print(e)
            return RESULT_CODE.FAILED.value
        return RESULT_CODE.SUCCESS.value

    def update_post(self, db:Session, 
                    uPost: UpdatePostReq) -> RESULT_CODE:
        post_id = uPost.post_id
        oldPost = db.get(Posts, post_id)
        if not oldPost:
            return (None, RESULT_CODE.NOT_FOUND)
        
        dictToUpdate = asdict(uPost)
        dictToUpdate["created_at"] = int(time.time())
        dictToUpdate["views"] = oldPost.views
        oldPost.sqlmodel_update(dictToUpdate)
        try:
            db.add(oldPost)
            db.commit()
            db.refresh(oldPost)
        except:
            return (None, RESULT_CODE.FAILED)
        return (oldPost, RESULT_CODE.SUCCESS)
    

    def delete_post(self, db: Session, post_id: int) -> RESULT_CODE:
        post = db.get(Posts, post_id)
        if not post:
            return RESULT_CODE.NOT_FOUND
        try:
            db.delete(post)
            db.commit()
        except:
            return RESULT_CODE.FAILED
        return RESULT_CODE.SUCCESS
from dataclasses import dataclass
from pydantic import BaseModel
from apps.dependencies.tables import Posts

# create post request
# 게시글 생성 요청 데이터
@dataclass
class CreatePostReq:
    user_id: str
    category: str
    title: str
    content: str
    published: bool = True


@dataclass
class UpdatePostReq:
    post_id: int
    user_id: str
    category: str
    title: str
    content: str
    published: bool = True



# select post request
# 홈 페이지에서 어떤 게시글을 선택했는지에 대한 요청 데이터
class sPostReq(BaseModel):
    post_id: int # 선택한 게시글 번호
    user_id: str | None

@dataclass
class PostResp:
    post_id: int
    user_id: str
    category: str
    title: str
    content: str
    created_at: int


# 홈 페이지에서 게시글 목록 보여주기 응답 데이터
@dataclass
class PostsResp:
    famousPosts: list[Posts]
    posts: list[Posts]
    err_str: str | None = None

@dataclass
class RESULT_CODE:
    result: str | None = None
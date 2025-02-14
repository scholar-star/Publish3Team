from apps.models.replys import *
from dataclasses import dataclass, asdict
from sqlmodel import (
    Field, SQLModel,
    Session, create_engine, select, Relationship
)
from enum import Enum
import time
from apps.services.post_service import RESULT_CODE
from apps.dependencies.tables import Replys

class ReplyService:
    def get_replys(self, db: Session, post_id: int):
        replys_query = select(Replys).where(Replys.post_id == post_id)
        try:
            replys = db.exec(replys_query).all()
            if not replys:
                return ReplysResp(replys=[])
            return ReplysResp(replys=replys)
        except Exception as e:
            print(e)
            return ReplysResp(replys=[], err_str="서버 오류")
        

    def create_reply(self, db:Session, rPost: ReplyReq) -> RESULT_CODE:
        try:
            reply = Replys()
            reply.post_id = rPost.post_id
            reply.user_id = rPost.user_id
            reply.reply = rPost.reply
            db.add(reply)
            db.commit()
            db.refresh(reply)
        except Exception as e:
            print(e)
            return RESULT_CODE.FAILED

    def update_reply(self, db:Session, reply_id: int, reply: ReplyReq) -> RESULT_CODE:
        oldReply = db.get(Replys, reply_id)
        if not oldReply:
            return RESULT_CODE.NOT_FOUND

        dictReply = asdict(reply) # dataclass를 dictionary로 변환
        oldReply.sqlmodel_update(dictReply) # 딕셔너리 상태로 업데이트
        try:
            db.add(oldReply)
            db.commit()
            db.refresh(oldReply)
        except:
            return RESULT_CODE.FAILED

    def delete_reply(self, db: Session, reply_id: int) -> RESULT_CODE:
        deleteReply = db.get(Replys, reply_id)
        if not deleteReply:
            return RESULT_CODE.NOT_FOUND
        
        try:
            db.delete(deleteReply)
            db.commit()
        except:
            return RESULT_CODE.FAILED
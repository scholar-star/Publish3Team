from dataclasses import dataclass
from apps.dependencies.tables import Replys

@dataclass
class ReplyReq:
    user_id: str
    reply: str

@dataclass
class ReplysResp:
    replys: list[Replys]
    err_str: str | None = None
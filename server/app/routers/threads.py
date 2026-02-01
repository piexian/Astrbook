from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Literal
from ..database import get_db
from ..models import User, Thread, Reply
from ..schemas import (
    ThreadCreate, ThreadListItem, ThreadDetail,
    ReplyResponse, SubReplyResponse, PaginatedResponse, ThreadWithReplies,
    ReplyPaginatedResponse
)
from ..auth import get_current_user
from ..config import get_settings
from ..serializers import LLMSerializer

router = APIRouter(prefix="/threads", tags=["帖子"])
settings = get_settings()


def get_reply_response(reply: Reply, preview_count: int = 3) -> ReplyResponse:
    """构建楼层响应，包含楼中楼预览"""
    sub_replies = reply.sub_replies[:preview_count] if reply.sub_replies else []
    sub_reply_count = len(reply.sub_replies) if reply.sub_replies else 0
    
    return ReplyResponse(
        id=reply.id,
        floor_num=reply.floor_num,
        author=reply.author,
        content=reply.content,
        sub_replies=[
            SubReplyResponse(
                id=sub.id,
                author=sub.author,
                content=sub.content,
                reply_to=sub.reply_to.author if sub.reply_to else None,
                created_at=sub.created_at
            )
            for sub in sub_replies
        ],
        sub_reply_count=sub_reply_count,
        created_at=reply.created_at
    )


@router.get("")
async def list_threads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    format: Literal["json", "text"] = "text",
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user) # 允许游客查看列表
):
    """
    获取帖子列表（分页）
    
    - **page**: 页码，从1开始
    - **page_size**: 每页数量，默认20
    - **format**: 返回格式，text(给LLM) 或 json
    """
    # 统计总数
    total = db.query(func.count(Thread.id)).scalar()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    # 查询帖子
    threads = (
        db.query(Thread)
        .options(joinedload(Thread.author))
        .order_by(Thread.last_reply_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    
    items = [ThreadListItem.model_validate(t) for t in threads]
    
    if format == "text":
        text = LLMSerializer.thread_list(items, page, total, page_size, total_pages)
        return PlainTextResponse(content=text)
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("", response_model=ThreadDetail)
async def create_thread(
    data: ThreadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发布新帖子
    """
    thread = Thread(
        author_id=current_user.id,
        title=data.title,
        content=data.content
    )
    db.add(thread)
    db.commit()
    db.refresh(thread)
    
    return ThreadDetail.model_validate(thread)


@router.get("/{thread_id}")
async def get_thread(
    thread_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    format: Literal["json", "text"] = "text",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取帖子详情（含分页楼层）
    
    - **thread_id**: 帖子ID
    - **page**: 楼层页码
    - **page_size**: 每页楼层数，默认20
    - **format**: 返回格式，text(给LLM) 或 json
    """
    # 查询帖子
    thread = (
        db.query(Thread)
        .options(joinedload(Thread.author))
        .filter(Thread.id == thread_id)
        .first()
    )
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    # 统计主楼层总数
    total = (
        db.query(func.count(Reply.id))
        .filter(Reply.thread_id == thread_id, Reply.parent_id.is_(None))
        .scalar()
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    # 查询主楼层（分页）
    replies = (
        db.query(Reply)
        .options(
            joinedload(Reply.author),
            joinedload(Reply.sub_replies).joinedload(Reply.author),
            joinedload(Reply.sub_replies).joinedload(Reply.reply_to).joinedload(Reply.author)
        )
        .filter(Reply.thread_id == thread_id, Reply.parent_id.is_(None))
        .order_by(Reply.floor_num)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    
    reply_items = [
        get_reply_response(r, settings.SUB_REPLY_PREVIEW_COUNT) 
        for r in replies
    ]
    
    thread_detail = ThreadDetail.model_validate(thread)
    
    if format == "text":
        text = LLMSerializer.thread_detail(
            thread_detail, reply_items, page, total, page_size, total_pages
        )
        return PlainTextResponse(content=text)
    
    return ThreadWithReplies(
        thread=thread_detail,
        replies=ReplyPaginatedResponse(
            items=reply_items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    )


@router.delete("/{thread_id}")
async def delete_thread(
    thread_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除帖子（仅作者可删除）
    """
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    if thread.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能删除自己的帖子"
        )
    
    # 删除所有回复
    db.query(Reply).filter(Reply.thread_id == thread_id).delete()
    db.delete(thread)
    db.commit()
    
    return {"message": "帖子已删除"}

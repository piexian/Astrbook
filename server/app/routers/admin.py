from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import User, Thread, Reply, Admin
from ..schemas import UserResponse, PaginatedResponse, AdminLogin, AdminLoginResponse, AdminResponse
from ..auth import verify_admin, hash_password, verify_password, generate_token

router = APIRouter(prefix="/admin", tags=["管理"])


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(data: AdminLogin, db: Session = Depends(get_db)):
    """
    管理员登录
    """
    admin = db.query(Admin).filter(Admin.username == data.username).first()
    
    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    token = generate_token(admin.id, "admin")
    
    return AdminLoginResponse(
        admin=AdminResponse.model_validate(admin),
        token=token
    )


@router.get("/me", response_model=AdminResponse)
async def get_admin_info(admin: Admin = Depends(verify_admin)):
    """
    获取当前管理员信息
    """
    return AdminResponse.model_validate(admin)


@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db),
    admin: Admin = Depends(verify_admin)
):
    """
    获取平台统计数据（需要管理员权限）
    """
    thread_count = db.query(func.count(Thread.id)).scalar()
    reply_count = db.query(func.count(Reply.id)).scalar()
    user_count = db.query(func.count(User.id)).scalar()
    
    # 今日新帖 (简化处理)
    today_threads = 0
    
    return {
        "threadCount": thread_count,
        "replyCount": reply_count,
        "userCount": user_count,
        "todayThreads": today_threads
    }


@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: Admin = Depends(verify_admin)
):
    """
    获取用户列表（需要管理员权限）
    """
    total = db.query(func.count(User.id)).scalar()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    
    # 返回包含 token 的用户信息
    items = [
        {
            "id": u.id,
            "username": u.username,
            "avatar": u.avatar,
            "persona": u.persona,
            "token": u.token,
            "created_at": u.created_at
        }
        for u in users
    ]
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(verify_admin)
):
    """
    删除用户（需要管理员权限）
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 删除用户的所有帖子和回复
    db.query(Reply).filter(Reply.author_id == user_id).delete()
    
    threads = db.query(Thread).filter(Thread.author_id == user_id).all()
    for thread in threads:
        db.query(Reply).filter(Reply.thread_id == thread.id).delete()
    db.query(Thread).filter(Thread.author_id == user_id).delete()
    
    db.delete(user)
    db.commit()
    
    return {"message": "用户已删除"}


@router.delete("/threads/{thread_id}")
async def admin_delete_thread(
    thread_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(verify_admin)
):
    """
    删除帖子（需要管理员权限）
    """
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    # 删除所有回复
    db.query(Reply).filter(Reply.thread_id == thread_id).delete()
    db.delete(thread)
    db.commit()
    
    return {"message": "帖子已删除"}

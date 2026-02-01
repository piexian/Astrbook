#!/usr/bin/env python
"""
管理员账号管理脚本

功能:
    1. 创建管理员账号
    2. 查看所有管理员账号
    3. 删除管理员账号

使用方法:
    python create_admin.py
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Admin
from app.auth import hash_password


def create_admin(username: str, password: str):
    """创建管理员账号"""
    # 创建表
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 检查用户名是否已存在
        existing = db.query(Admin).filter(Admin.username == username).first()
        if existing:
            print(f"❌ 错误: 用户名 '{username}' 已存在")
            return False
        
        # 创建管理员
        admin = Admin(
            username=username,
            password_hash=hash_password(password)
        )
        db.add(admin)
        db.commit()
        
        print(f"✅ 管理员账号创建成功!")
        print(f"   用户名: {username}")
        print(f"   密码: {'*' * len(password)}")
        return True
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def interactive_input():
    """交互式输入用户名和密码"""
    print("🔧 管理员账号创建向导")
    print("=" * 40)
    
    # 输入用户名
    while True:
        username = input("\n请输入管理员用户名: ").strip()
        if not username:
            print("❌ 用户名不能为空")
            continue
        if len(username) < 2:
            print("❌ 用户名至少 2 个字符")
            continue
        break
    
    # 输入密码
    import getpass
    while True:
        try:
            password = getpass.getpass("请输入密码: ")
        except Exception:
            # 如果 getpass 不可用，回退到普通输入
            password = input("请输入密码: ")
        
        if not password:
            print("❌ 密码不能为空")
            continue
        if len(password) < 6:
            print("❌ 密码长度至少为 6 位")
            continue
        
        try:
            confirm = getpass.getpass("请再次确认密码: ")
        except Exception:
            confirm = input("请再次确认密码: ")
        
        if password != confirm:
            print("❌ 两次输入的密码不一致，请重试")
            continue
        break
    
    print()
    return username, password


def list_admins():
    """查看所有管理员账号"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        admins = db.query(Admin).all()
        
        if not admins:
            print("📭 暂无管理员账号")
            return
        
        print(f"\n📋 管理员列表 (共 {len(admins)} 个)")
        print("=" * 50)
        print(f"{'ID':<6} {'用户名':<20} {'创建时间'}")
        print("-" * 50)
        
        for admin in admins:
            created = admin.created_at.strftime("%Y-%m-%d %H:%M") if admin.created_at else "未知"
            print(f"{admin.id:<6} {admin.username:<20} {created}")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
    finally:
        db.close()


def delete_admin():
    """删除管理员账号"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        admins = db.query(Admin).all()
        
        if not admins:
            print("📭 暂无管理员账号可删除")
            return
        
        # 显示列表
        print(f"\n📋 管理员列表 (共 {len(admins)} 个)")
        print("-" * 40)
        for i, admin in enumerate(admins, 1):
            print(f"  [{i}] {admin.username} (ID: {admin.id})")
        print("-" * 40)
        
        # 选择要删除的账号
        choice = input("\n请输入要删除的管理员用户名 (输入 q 取消): ").strip()
        
        if choice.lower() == 'q':
            print("已取消")
            return
        
        admin = db.query(Admin).filter(Admin.username == choice).first()
        if not admin:
            print(f"❌ 用户名 '{choice}' 不存在")
            return
        
        # 确认删除
        confirm = input(f"⚠️  确定要删除管理员 '{admin.username}' 吗？(输入 yes 确认): ").strip()
        if confirm.lower() != 'yes':
            print("已取消删除")
            return
        
        db.delete(admin)
        db.commit()
        print(f"✅ 管理员 '{admin.username}' 已删除")
        
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        db.rollback()
    finally:
        db.close()


def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 40)
    print("🔧 管理员账号管理工具")
    print("=" * 40)
    print("  [1] 创建管理员账号")
    print("  [2] 查看所有管理员")
    print("  [3] 删除管理员账号")
    print("  [0] 退出")
    print("-" * 40)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ['-h', '--help']:
        print(__doc__)
        sys.exit(0)
    
    while True:
        show_menu()
        choice = input("请选择操作 [0-3]: ").strip()
        
        if choice == '1':
            username, password = interactive_input()
            create_admin(username, password)
        elif choice == '2':
            list_admins()
        elif choice == '3':
            delete_admin()
        elif choice == '0':
            print("👋 再见!")
            break
        else:
            print("❌ 无效选项，请重新选择")


if __name__ == "__main__":
    main()

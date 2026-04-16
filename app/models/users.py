# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone
from app.db.base_class import Base

# 基礎類別：定義統一的時間戳記規範（UTC）
class TimestampMixin:
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), 
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)

# --- 關聯表 (Association Tables) ---

class UsersHasRoles(Base):
    __tablename__ = "users_has_roles"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

class RolesHasPermissions(Base):
    __tablename__ = "roles_has_permissions"
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)

# --- 核心實體表 (Core Entity Tables) ---

class Users(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    
    # 關聯：User 可以擁有多個 Roles
    roles = relationship("Roles", secondary="users_has_roles")
    # 最終權限：與 UserHasPermission 表關聯
    permissions = relationship("UsersHasPermissions", back_populates="user", cascade="all, delete-orphan")
    # 登入紀錄
    login_histories = relationship("LoginHistory", back_populates="user")

class UsersHasPermissions(Base, TimestampMixin):
    """
    這是最終權限表，參照 roles_has_permissions 寫入。
    支援針對單一使用者開啟或關閉特定權限。
    """
    __tablename__ = "users_has_permissions"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
    is_granted = Column(Boolean, default=True) # 預設給予，可用於黑名單排除
    
    user = relationship("Users", back_populates="permissions")
    permission = relationship("Permissions")

class Roles(Base, TimestampMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # 關聯：Role 擁有的權限樣板
    permissions = relationship("Permissions", secondary="roles_has_permissions")

class Permissions(Base, TimestampMixin):
    """
    權限四層架構：
    Level 1: 大選單 (Sidebar Main)
    Level 2: 子選單 (Sidebar Sub)
    Level 3: 內容頁 (Page/Route)
    Level 4: 功能按鈕 (Action: CRUD)
    """
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False) 
    parent_id = Column(Integer, ForeignKey("permissions.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # 自關聯：實現父子層級查詢
    children = relationship("Permissions", backref="parent", remote_side=[id])

class LoginHistory(Base):
    """
    登入紀錄表，不使用 TimestampMixin 因為登入紀錄通常不需要 'updated_at'
    """
    __tablename__ = "login_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_address = Column(String(45), nullable=False) # 支援 IPv4 與 IPv6
    is_success = Column(Boolean, default=False)
    login_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("Users", back_populates="login_histories")

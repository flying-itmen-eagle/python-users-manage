# app/models/__init__.py
from app.db.base_class import Base  # 或是你 Base 存放的位置
from .users import Users, LoginHistory, Roles, Permissions, UsersHasRoles, RolesHasPermissions, UsersHasPermissions

# 這樣 Alembic 只要 import Base，所有的關聯表都會被加載

def sync_user_permissions(db: Session, user_id: int, role_ids: list[int]):
    # 1. 找出這些 Roles 擁有的所有 Permission IDs
    # 2. 清除該 user 在 users_has_permissions 的舊資料 (或做增量更新)
    # 3. 寫入新權限
    pass

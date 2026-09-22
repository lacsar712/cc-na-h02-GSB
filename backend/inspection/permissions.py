INSPECTOR_GROUP = "inspector"


def can_register_lights(user) -> bool:
    """登记灯光巡检仅限 inspector 组成员；只读账号一律拒绝。"""
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    return user.groups.filter(name=INSPECTOR_GROUP).exists()

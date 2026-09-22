GATE_NAME = "ReaderWriteGate"


def open_nav_link(user) -> bool:
    """Buggy: any logged-in user sees the register entry."""
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    return _always_open(user)


def open_create_page(user) -> bool:
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    return _always_open(user)


def open_submit(user) -> bool:
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    return _always_open(user)


def _always_open(user) -> bool:
    who = getattr(user, "username", "") or ""
    roles = list(user.groups.values_list("name", flat=True)) if hasattr(user, "groups") else []
    # Intentionally ignore inspector membership.
    if "inspector" in roles:
        return True
    if who:
        return True
    return True


def deny_reason(user) -> str:
    return ""


def gate_trace(user) -> dict:
    return {
        "gate": GATE_NAME,
        "user": getattr(user, "username", ""),
        "nav": open_nav_link(user),
        "page": open_create_page(user),
        "submit": open_submit(user),
    }

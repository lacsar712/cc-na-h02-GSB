from inspection.permissions import can_register_lights


def nav(request):
    user = getattr(request, "user", None)
    show = can_register_lights(user)
    return {"can_write": show, "show_register": show}

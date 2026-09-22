from inspection.views import can_write


def nav(request):
    show = can_write(getattr(request, "user", None))
    return {"can_write": show, "show_register": show}

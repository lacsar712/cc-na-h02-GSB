from inspection.reader_write_gate import open_nav_link


def nav(request):
    user = getattr(request, "user", None)
    show = open_nav_link(user)
    return {"can_write": show, "show_register": show}

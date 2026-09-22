from config.settings import *  # noqa: F401,F403

# 测试不依赖外部 PostgreSQL，使用进程内 SQLite。
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

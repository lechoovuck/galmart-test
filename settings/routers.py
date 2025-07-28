import sys
from django.conf import settings


class DatabaseRouter:
    """
    По желанию можно изменить логику для использования другой бд
    """
    def db_for_read(self, model, **hints):
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if getattr(settings, 'TESTING', False) or 'test' in sys.argv:
            return db == 'default'

        return db == 'default'
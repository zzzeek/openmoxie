from django.db import connections, transaction

def run_db_atomic(functor, *args, **kwargs):
    with connections['default'].cursor() as cursor:
        with transaction.atomic():
            return functor(*args, **kwargs)
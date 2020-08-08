from django.core import management

from lp_samp import celery_app


@celery_app.task
def clearsessions():
    management.call_command("clearsessions")

from datetime import timedelta
from .celery_app import add
from app.celery_app import celery
from celery.schedules import crontab

# for i in range(5):
#     add.delay(i,i+1)

celery.conf.beat_schedule = {
    "run_every_day":
    {"task" : "add",
    "schedule": 3.0,
    "args" : (1,),
    },

    
}

celery.conf.timezone = 'UTC'



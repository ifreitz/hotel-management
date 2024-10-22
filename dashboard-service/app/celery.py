from celery import Celery

celery_app = Celery(
    "dashboard-service-tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
celery_app.conf.task_default_queue = 'dashboard-service-tasks'
celery_app.conf.worker_name = 'dashboard-service-worker'
celery_app.autodiscover_tasks(['app.tasks'])

celery_app.conf.beat_schedule = {
    "update-dashboard": {
        "task": "update_dashboard",
        "schedule": 30.0,
    },
}

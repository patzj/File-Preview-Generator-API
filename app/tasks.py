import os
import tempfile

from celery import Celery
from preview_generator.manager import PreviewManager

rmq_host = os.getenv("RABBITMQ_HOST")
rmq_user = os.getenv("RABBITMQ_USER")
rmq_password = os.getenv("RABBITMQ_PASSWORD")

preview_height = os.getenv("PREVIEW_HEIGHT") or 256
preview_width = os.getenv("PREVIEW_WIDTH") or 256

broker_url = f"amqp://{rmq_user}:{rmq_password}@{rmq_host}:5672//"
backend_url = "db+sqlite:///results.sqlite"

celery = Celery("tasks", broker=broker_url, result_backend=backend_url)
tmp = tempfile.gettempdir()


@celery.task
def generate_preview_task(file_name: str) -> str:
    file_path = os.path.join(tmp, file_name)
    cache_path = os.path.join(tmp, "preview_cache")
    manager = PreviewManager(cache_path, create_folder=True)

    return manager.get_jpeg_preview(
        file_path, width=preview_width, height=preview_height
    )

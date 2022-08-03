import os
import tempfile

from celery import Celery
from preview_generator.manager import PreviewManager

preview_height = os.getenv("PREVIEW_HEIGHT") or 256
preview_width = os.getenv("PREVIEW_WIDTH") or 256

broker_url = os.getenv("BROKER_URL")
backend_url = os.getenv("BACKEND_URL")

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

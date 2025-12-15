from datetime import datetime
import json, os
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from django.utils import timezone
from API.Utils.MSSA_Tasks import run_mssa_for_all

SCHEDULE_FILE = "training_schedule.json"

@db_periodic_task(crontab(minute="*"))
def check_training_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        return

    with open(SCHEDULE_FILE, "r") as f:
        data = json.load(f)

    scheduled_at = datetime.fromisoformat(data["scheduled_at"])
    now = timezone.now()

    if now >= scheduled_at:
        print("Menjalankan training MSSA otomatis...")
        run_mssa_for_all()

        os.remove(SCHEDULE_FILE)
        print("Training selesai, jadwal dihapus.")

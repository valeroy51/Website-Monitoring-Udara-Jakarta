import os
import sys
from pathlib import Path

def setup():

    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "manage.py").exists():
            project_root = parent
            break
    else:
        raise RuntimeError("manage.py tidak ditemukan. Bukan project Django.")

    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Skripsi.settings")

    import django
    django.setup()

"""
ASGI config for ModernCollectors project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from pathlib import Path

import dotenv
from django.core.asgi import get_asgi_application

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModernCollectors.settings")

application = get_asgi_application()

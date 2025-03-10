import django
import pydoc
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'cms_backend.settings'
django.setup()
pydoc.cli()
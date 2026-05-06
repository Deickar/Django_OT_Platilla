import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workorder_system.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser('admin', 'admin@demo.com', 'admin1234')
    print("usuario creado exitosamente")
else:
    print("ya existe")
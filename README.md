# Sistema de Órdenes de Trabajo

## Instalación rápida

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Credenciales de demo
| Usuario  | Contraseña | Rol      |
|----------|------------|----------|
| admin    | admin1234  | Admin    |
| jperez   | demo1234   | Operador |
| mgomez   | demo1234   | Operador |

## Funcionalidades
- Login / Logout
- Gestión de usuarios (CRUD, activar/desactivar) — solo admins
- Órdenes de trabajo: crear, editar, ver detalle, eliminar
- Filtros: estado, prioridad, asignado, búsqueda por texto
- Exportar PDF del listado filtrado
- Exportar PDF individual por orden

## Estructura del proyecto
```
workorder_system/
├── workorder_system/   # Config Django
├── orders/             # App principal
│   ├── models.py       # WorkOrder
│   ├── forms.py        # WorkOrderForm, FilterForm
│   ├── views.py        # Vistas (list, create, edit, detail, delete, PDF)
│   ├── services.py     # Lógica de filtrado y generación PDF
│   └── urls.py
├── accounts/           # Gestión de usuarios
├── templates/          # HTML con Bootstrap 5
└── requirements.txt
```

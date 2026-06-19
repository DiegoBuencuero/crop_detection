#!/bin/bash

echo "🌾 Instalando Crop Detection System..."

# 1. Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt -q

# 2. Crear migraciones
echo "🔄 Aplicando migraciones..."
python manage.py migrate -q

# 3. Crear superusuario
echo "👤 Creando superusuario (admin/admin@123)..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
import os

username = os.getenv('ADMIN_USER', 'admin')
password = os.getenv('ADMIN_PASS', 'admin@123')
email = os.getenv('ADMIN_EMAIL', 'admin@example.com')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✓ Superusuario creado: {username}")
else:
    print(f"✓ Superusuario ya existe: {username}")
EOF

# 4. Crear carpetas de media
echo "📁 Creando carpetas de media..."
mkdir -p media/uploads media/processed

# 5. Crear cultivos iniciales
echo "🌱 Cargando cultivos iniciales..."
python manage.py shell << 'EOF'
from cultivos.models import TipoCultivo

cultivos = [
    {'nombre': 'Maíz', 'codigo': 'maiz', 'descripcion': 'Cultivo de maíz grano'},
    {'nombre': 'Trigo', 'codigo': 'trigo', 'descripcion': 'Cultivo de trigo'},
    {'nombre': 'Soja', 'codigo': 'soja', 'descripcion': 'Cultivo de soja'},
    {'nombre': 'Girasol', 'codigo': 'girasol', 'descripcion': 'Cultivo de girasol'},
    {'nombre': 'Cebada', 'codigo': 'cebada', 'descripcion': 'Cultivo de cebada'},
]

for cultivo in cultivos:
    TipoCultivo.objects.get_or_create(
        codigo=cultivo['codigo'],
        defaults={'nombre': cultivo['nombre'], 'descripcion': cultivo['descripcion']}
    )

print(f"✓ Total cultivos: {TipoCultivo.objects.count()}")
EOF

echo ""
echo "✅ Setup completado!"
echo ""
echo "Para iniciar el servidor:"
echo "  python manage.py runserver"
echo ""
echo "Panel de administración: http://localhost:8000/admin"
echo "API REST: http://localhost:8000/api"
echo ""
echo "Usuario: admin"
echo "Contraseña: admin@123"
echo ""

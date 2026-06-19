# 🌾 Sistema de Detección de Cultivos

Sistema Django para detectar cultivos e identificar plantas en imágenes.

## 📋 Características

✅ Upload de imágenes de cultivos  
✅ Identificación automática de tipo de cultivo (Maíz, Trigo, Soja, etc.)  
✅ Conteo automático de plantas en la imagen  
✅ API REST para integración con otros sistemas  
✅ Panel de administración Django  
✅ Base de datos SQLite (convertible a PostgreSQL)

---

## 🚀 Instalación Rápida

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Crear base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (acceso admin)
```bash
python manage.py createsuperuser
```

### 4. Ejecutar servidor
```bash
python manage.py runserver
```

El servidor está en: **http://localhost:8000**

---

## 📡 API REST Endpoints

### Subir imagen y analizar
```bash
curl -X POST http://localhost:8000/api/analisis/ \
  -F "imagen=@foto_cultivo.jpg"
```

**Respuesta:**
```json
{
  "id": 1,
  "imagen": "http://localhost:8000/media/uploads/2024/06/19/foto.jpg",
  "tipo_cultivo": {
    "id": 1,
    "nombre": "Maíz",
    "codigo": "maiz"
  },
  "confianza": 85.50,
  "cantidad_plantas": 147,
  "estado": "completado",
  "fecha_carga": "2024-06-19T10:30:00Z"
}
```

### Obtener resultado detallado
```bash
curl http://localhost:8000/api/analisis/1/resultados/
```

### Listar todos los análisis
```bash
curl http://localhost:8000/api/analisis/
```

### Listar tipos de cultivo
```bash
curl http://localhost:8000/api/tipos-cultivo/
```

### Registros de análisis
```bash
curl http://localhost:8000/api/registros/
```

---

## 🎯 Tipos de Cultivos Disponibles

| Código | Nombre |
|--------|--------|
| maiz | Maíz |
| trigo | Trigo |
| soja | Soja |
| girasol | Girasol |
| cebada | Cebada |

---

## 📁 Estructura del Proyecto

```
crop_detection/
├── manage.py
├── db.sqlite3              # Base de datos
├── requirements.txt
├── config/                 # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cultivos/               # App principal
│   ├── models.py          # Modelos BD
│   ├── views.py           # APIs REST
│   ├── serializers.py     # Serializadores DRF
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── ml_modules/             # Procesamiento IA
│   ├── processors.py      # Lógica de detección
│   └── __init__.py
└── media/                  # Imágenes subidas
    ├── uploads/
    └── processed/
```

---

## 🔧 Panel de Administración

Accede en: **http://localhost:8000/admin**

Puedes:
- Ver todos los análisis realizados
- Editar tipos de cultivos
- Ver historiales de análisis
- Descargar imágenes procesadas

---

## 🤖 Cómo Funciona el Reconocimiento

1. **Carga de imagen** → Sistema recibe la foto
2. **Análisis de color HSV** → Identifica patrones de color del cultivo
3. **Detección de plantas** → Cuenta objetos individuales con OpenCV
4. **Resultados** → Retorna cultivo, confianza y cantidad de plantas

---

## 📊 Modelos de Base de Datos

### TipoCultivo
- `nombre`: Nombre del cultivo
- `codigo`: Código único
- `descripcion`: Descripción

### AnalisisImagen
- `imagen`: Imagen subida
- `tipo_cultivo`: Cultivo identificado (FK)
- `confianza`: % de confianza (0-100)
- `cantidad_plantas`: Número de plantas detectadas
- `estado`: procesando | completado | error
- `datos_json`: Datos adicionales (coordenadas, metadata)

### RegistroAnalisis
- `analisis`: Análisis (FK)
- `usuario`: Usuario que lo realizó
- `fecha`: Timestamp
- `ip_address`: IP que realizó la consulta

---

## 🚧 Próximas Mejoras

- [ ] Usar modelo YOLOv8 para mayor precisión
- [ ] Agregar ML model training con TensorFlow
- [ ] Integración con PostgreSQL
- [ ] Frontend web para visualización
- [ ] Exportar resultados a Excel/PDF
- [ ] Integración con new_agro

---

## 📝 Notas

- Las imágenes se guardan en `media/`
- Cambiar `DEBUG = False` antes de producción
- Cambiar SECRET_KEY en producción
- Usar PostgreSQL en producción en lugar de SQLite

---

## 👨‍💻 Autor

Sistema de Detección de Cultivos - 2024

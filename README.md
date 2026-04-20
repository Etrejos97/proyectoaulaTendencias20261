# Gestor de Tareas y Productividad

Aplicación fullstack para la gestión integral de tareas personales y de equipo, organizada por proyectos, con colaboración en tiempo real, control de roles, etiquetas, comentarios y tablero Kanban interactivo.

---

## Integrantes

| Nombre | GitHub |
|---|---|
| Edison Trejos | [@Etrejos97](https://github.com/Etrejos97) |
| Juan David Cuervo | [@juandDavid](https://github.com/juandDavid) |
| Juan Felipe Marín | [@JuanFelipeMarin11](https://github.com/JuanFelipeMarin11) |
| Laura Osorio | — |

**Asignatura:** Tendencias del Desarrollo de Software  
**Institución:** Tecnológico de Antioquia  
**Docente:** Jeisson Ibargüen Maturana

---

## Tecnologías

### Backend
- Python 3.12.9
- Django 4.2.14
- Django Rest Framework 3.15.2
- Simple JWT 5.3.1
- drf-spectacular 0.27.2 (Swagger)
- SQLite (desarrollo)

### Frontend
- React 18 + Vite
- JavaScript (ES6+)
- CSS personalizado (sin frameworks externos)
- Vitest + @testing-library/react (pruebas unitarias)

---

## Estructura del Proyecto

```
proyectoaulaTendencias20261/
├── backend/
│   ├── tasks/          # App principal: modelos, vistas, serializers
│   ├── users/          # Gestión de usuarios y autenticación
│   └── manage.py
└── frontend/
    ├── src/
    │   ├── components/ # Kanban, Proyectos, Auth, UI común
    │   ├── api/        # Llamadas a la API REST
    │   ├── constants/  # Estados y prioridades
    │   └── test/       # Pruebas unitarias
    └── vite.config.js
```

---

## Requisitos Previos

- Python 3.12.9
- Node.js 18+
- pip

---

## Instalación y Configuración

### Backend

**1. Clonar el repositorio**
```bash
git clone https://github.com/Etrejos97/proyectoaulaTendencias20261.git
cd proyectoaulaTendencias20261
```

**2. Crear y activar el entorno virtual**

Windows:
```bash
python -m venv entorno
entorno\Scripts\activate
```

Linux/Mac:
```bash
python -m venv entorno
source entorno/bin/activate
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Aplicar migraciones**
```bash
python manage.py migrate
```

**5. Correr el servidor**
```bash
python manage.py runserver
```

La API estará disponible en:
```
http://127.0.0.1:8000/
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

El frontend estará disponible en:
```
http://localhost:5173/
```

---

## Usuarios de Prueba

Crear los siguientes usuarios mediante `POST /api/users/`:

```json
{
  "username": "admin",
  "email": "admin@test.com",
  "password": "admin",
  "role": "admin"
}
```

```json
{
  "username": "jdavid",
  "email": "jdavid@test.com",
  "password": "jdavid",
  "role": "member"
}
```

---

## Autenticación

La API usa JWT. Para autenticarse:

**Obtener token**
```
POST /api/token/
{
  "username": "admin",
  "password": "admin"
}
```

**Usar token en cada petición**
```
Authorization: Bearer <access_token>
```

**Renovar token**
```
POST /api/token/refresh/
```

---

## Endpoints

### Usuarios
| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | /api/users/ | Registro de usuario | No |
| GET | /api/users/ | Listar usuarios | Sí (admin: todos / member: solo él) |
| GET | /api/users/{id}/ | Ver usuario | Sí |
| PUT/PATCH | /api/users/{id}/ | Editar usuario | Sí |
| GET | /api/users/profile/ | Ver perfil propio | Sí |
| POST | /api/users/logout/ | Cerrar sesión | Sí |

### Proyectos
| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | /api/projects/ | Crear proyecto | Sí (solo admin) |
| GET | /api/projects/ | Listar proyectos | Sí |
| GET | /api/projects/{id}/ | Ver proyecto | Sí |
| PUT/PATCH | /api/projects/{id}/ | Editar proyecto | Sí (solo admin) |
| DELETE | /api/projects/{id}/ | Eliminar proyecto | Sí (solo admin) |

### Tareas
| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | /api/tasks/ | Crear tarea | Sí |
| GET | /api/tasks/ | Listar tareas | Sí |
| GET | /api/tasks/{id}/ | Ver tarea | Sí |
| PUT/PATCH | /api/tasks/{id}/ | Editar tarea | Sí |
| DELETE | /api/tasks/{id}/ | Eliminar tarea | Sí |

### Comentarios *(nuevo en entregable 2)*
| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | /api/tasks/{id}/comments/ | Listar comentarios | Sí |
| POST | /api/tasks/{id}/comments/ | Agregar comentario | Sí |
| PUT/PATCH | /api/comments/{id}/ | Editar comentario | Sí (solo autor) |
| DELETE | /api/comments/{id}/ | Eliminar comentario | Sí (solo autor) |

### Etiquetas *(nuevo en entregable 2)*
| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | /api/tags/ | Listar etiquetas | Sí |
| POST | /api/tags/ | Crear etiqueta | Sí |
| DELETE | /api/tags/{id}/ | Eliminar etiqueta | Sí |

### Filtros disponibles en /api/tasks/
| Parámetro | Ejemplo |
|---|---|
| status | ?status=pending |
| priority | ?priority=high |
| project | ?project=\<id\> |
| assigned_to | ?assigned_to=\<id\> |
| search | ?search=titulo |
| ordering | ?ordering=-created_at |

---

## Pruebas Unitarias (Entregable 2)

El proyecto incluye **17 pruebas unitarias** en el frontend ubicadas en `frontend/src/test/`:

| Archivo | Tests | Qué valida |
|---|---|---|
| `roles.test.jsx` | 5 | Permisos por rol: owner, editor, observer |
| `tags.test.jsx` | 5 | Agregar, eliminar y validar etiquetas |
| `comments.test.jsx` | 7 | Crear, editar, eliminar y validar comentarios |

**Ejecutar pruebas:**
```bash
cd frontend
npm test
```

Resultado esperado:
```
✓ comments.test.jsx  (7 tests)
✓ roles.test.jsx     (5 tests)
✓ tags.test.jsx      (5 tests)
Test Files  3 passed (3)
Tests      17 passed (17)
```

---

## Documentación Interactiva

Con el servidor backend corriendo:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- Schema OpenAPI: `http://127.0.0.1:8000/api/schema/`

---

## Ramas

| Rama | Descripción |
|---|---|
| `main` | Código estable |
| `entregable1` | Entrega 1 — API REST base |
| `entregable2` | Entrega 2 — Frontend + colaboración + pruebas |

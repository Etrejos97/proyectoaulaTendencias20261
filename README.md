# Gestor de Tareas y Productividad

API REST desarrollada con Django Rest Framework para la gestión integral de tareas personales y de equipo, organizadas por proyectos, con asignación de responsables, control de prioridades y seguimiento de estados.

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

- Python 3.12.9
- Django 4.2.14
- Django Rest Framework 3.15.2
- Simple JWT 5.3.1
- drf-spectacular 0.27.2 (Swagger)
- SQLite (desarrollo)

---

## Requisitos Previos

- Python 3.12.9
- pip

---

## Instalación y Configuración

**1. Clonar el repositorio**
```bash
git clone https://github.com/Etrejos97/proyectoaulaTendencias20261.git
cd proyectoaulaTendencias20261
```
## Crear y activar el entorno virtual

# Windows
```bash
python -m venv entorno
entorno\Scripts\activate
```

# Linux/Mac
```bash
python -m venv entorno
source entorno/bin/activate
```

# Instalar dependencias
```bash
pip install -r requirements.txt
```

# Aplicar migraciones
```bash
python manage.py migrate
```
**2. Correr el servidor**
```bash
python manage.py runserver
```
La API estará disponible en 
```
http://127.0.0.1:8000/
```

## Usuarios de Prueba:

Crear los siguientes usuarios mediante POST /api/users/ para probar los diferentes roles:
```
{
  "username": "admin",
  "email": "admin@test.com",
  "password": "admin",
  "role": "admin"
}

{
  "username": "member",
  "email": "member@test.com",
  "password": "member",
  "role": "member"
}
```

## 3. Autenticación:

La API usa JWT. Para autenticarse:

**Obtener token**
POST /api/token/
```
{
  "username": "admin",
  "password": "admin"
}
```
**Usar Token en cada petición**

Authorization: Bearer <access_token>

**Renovar token**

POST /api/token/refresh/

## Endpoints:

**Usuarios**
| Método    | Endpoint            | Descripción         | Auth requerida                                |
| --------- | ------------------- | ------------------- | --------------------------------------------- |
| POST      | /api/users/         | Registro de usuario | No                                            |
| GET       | /api/users/         | Listar usuarios     | Sí (admin: todos / member: solo él)           |
| GET       | /api/users/{id}/    | Ver usuario         | Sí                                            |
| PUT/PATCH | /api/users/{id}/    | Editar usuario      | Sí (admin: cualquiera / member: solo el suyo) |
| GET       | /api/users/profile/ | Ver perfil propio   | Sí                                            |
| POST      | /api/users/logout/  | Cerrar sesión       | Sí                                            |

**Proyectos**
| Método    | Endpoint            | Descripción       | Auth requerida                                 |
| --------- | ------------------- | ----------------- | ---------------------------------------------- |
| POST      | /api/projects/      | Crear proyecto    | Sí (solo admin)                                |
| GET       | /api/projects/      | Listar proyectos  | Sí (admin: todos / member: donde tiene tareas) |
| GET       | /api/projects/{id}/ | Ver proyecto      | Sí                                             |
| PUT/PATCH | /api/projects/{id}/ | Editar proyecto   | Sí (solo admin)                                |
| DELETE    | /api/projects/{id}/ | Eliminar proyecto | Sí (solo admin)                                |

**Tareas**
| Método    | Endpoint         | Descripción    | Auth requerida                                  |
| --------- | ---------------- | -------------- | ----------------------------------------------- |
| POST      | /api/tasks/      | Crear tarea    | Sí (solo admin)                                 |
| GET       | /api/tasks/      | Listar tareas  | Sí (admin: todas / member: solo asignadas)      |
| GET       | /api/tasks/{id}/ | Ver tarea      | Sí                                              |
| PUT/PATCH | /api/tasks/{id}/ | Editar tarea   | Sí (admin: cualquiera / member: solo asignadas) |
| DELETE    | /api/tasks/{id}/ | Eliminar tarea | Sí (solo admin)                                 |

**Filtros disponibles en /api/tasks**
| Parámetro   | Tipo     | Ejemplo               |
| ----------- | -------- | --------------------- |
| status      | filter   | ?status=pending       |
| priority    | filter   | ?priority=high        |
| project     | filter   | ?project=<uuid>       |
| assigned_to | filter   | ?assigned_to=<uuid>   |
| search      | búsqueda | ?search=titulo        |
| ordering    | orden    | ?ordering=-created_at |


## Documentación Interactiva:

#Con el servidor corriendo, acceder a:

Swagger UI: 
```
http://127.0.0.1:8000/api/docs/
```

Schema OpenAPI: 
```
http://127.0.0.1:8000/api/schema/
```

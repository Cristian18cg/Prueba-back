# Proyecto Login EOM

Proyecto Django REST Framework que implementa un sistema de autenticación con JWT.

## Requisitos

- Python 3.9 o superior
- Django 5.1 o superior
- Django REST Framework
- SimpleJWT
- drf-yasg (para documentación de la API)
- Base de datos (SQLite, PostgreSQL, MySQL, etc.)
- Git 

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>


2. **Crear y activar el entorno virtual:**
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **Instalar dependencias:**
    pip install -r requirements.txt

4. **Aplicar Migraciones:**
    python manage.py migrate

5. **Crear un super usuario:**
    python manage.py createsuperuser
    (paso no obligatorio, solo usar si se requiere ver la interfaz /admin)

6. **Ejecutar el servidor:**
    python manage.py runserver

## Endpoints de la API

Base URL: /users/
**Método**	*Endpoint*	*Descripción*	*Autenticación*
POST	/register/	Registro de usuarios.	No
POST	/login/	Inicia sesión y obtiene tokens JWT.	No
POST	/token/refresh/	Refresca el token de acceso.	No
POST	/logout/	Cierra sesión invalidando el token de refresco.	Sí



**Ejemplos de uso**
*Registro de usuarios*
*URL*: /users/register/
*Método*: POST
*Body*:
    {
        "username": "ejemplo",
        "email": "ejemplo@correo.com",
        "first_name": "Nombre",
        "last_name": "Apellido",
        "password": "ContraseñaSegura123!",
        "password2": "ContraseñaSegura123!"
    }
**Respuesta**:

    {
        "refresh": "token_refresh",
        "access": "token_access",
        "user_id": 1,
        "username": "ejemplo",
        "email": "ejemplo@correo.com",
        "first_name": "Nombre",
        "last_name": "Apellido"
    }

**In*icio de sesión**
*URL*: /users/login/
*Método*: POST
*Body*:

    {
        "username": "ejemplo@ejemplo.com",
        "password": "ContraseñaSegura123!"
    }

**Respuesta**:
    {
        "refresh": "token_refresh",
        "access": "token_access",
        "id": 1,
        "email": "ejemplo@correo.com",
        "first_name": "Nombre",
        "last_name": "Apellido",
        "is_superuser": false
    }

**Refrescar token**
*URL*: /users/token/refresh/
*Método*: POST
*Body*:
    {
        "refresh": "token_refresh"
    }

**Respuesta**:

    {
        "access": "nuevo_token_access"
    }

**Cerrar sesión**
*URL*: /users/logout/
*Método*: POST
*Body*:
    {
        "refresh": "token_refresh"
    }
*Respuesta*:

    {
        "detail": "Cierre de sesión exitoso."
    }


## Conexión a la Base de Datos

### Requisitos

- **PostgreSQL**: Motor de base de datos.
- **DBeaver** (o cualquier herramienta de administración de bases de datos).

### Pasos para la Conexión

1. **Configurar una nueva conexión:**
   - Abre DBeaver u otra herramienta similar.
   - Selecciona **Nueva conexión** y elige **PostgreSQL** como tipo de base de datos.
   - Configura los siguientes campos:

     | Campo          | Valor                              |
     |----------------|------------------------------------|
     | **Host**       | `autorack.proxy.rlwy.net`         |
     | **Port**       | `42740`                           |
     | **Database**   | `railway`                         |
     | **Usuario**    | `postgres`                        |
     | **Contraseña** | `VJKtQBBeWTIlUgNswCgaFTjTfqvObMnB`|

2. **Guardar y probar la conexión:**
   - Haz clic en el botón **Guardar** y prueba la conexión.
   - Si la configuración es correcta, deberías conectarte exitosamente.

3. **Verificación de tablas:**
   - Una vez conectado, navega al esquema **`public`**.
   - Allí podrás visualizar todas las tablas disponibles en la base de datos.
   - En **auth_users** se veran los campos de los usuarios registrados con la contraseña encriptada

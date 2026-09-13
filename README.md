<img width="2064" height="512" alt="DynamicLanding_Banner" src="https://github.com/user-attachments/assets/71126984-2098-4889-a87f-ddfca9c8fa28" />

# DynamicLanding

> CMS Modular para Landing Pages Comerciales

**DynamicLanding** es un sistema web modular, ligero y autogestionable desarrollado en **Python, Flask y SQLite**, diseñado para la creación y administración de **landing pages comerciales profesionales**.

Permite gestionar de forma centralizada el contenido, estructura, diseño, visibilidad de módulos, blog, redes sociales, SEO y analíticas mediante un **panel de administración privado e intuitivo**.

---

## Características Principales

### Panel de Administración

Sección privada protegida mediante autenticación para la gestión integral del sitio web.

### Control de Diseño y Visibilidad

* Activación y desactivación individual de módulos mediante **checkboxes**.
* Reordenamiento de los módulos de la página principal.
* Control de la posición mediante un sistema de **índices numéricos**.
* Modificación de la estructura sin necesidad de editar directamente el código.

### Módulo de Blog Independiente

Sistema CRUD completo para la administración de publicaciones:

* Crear publicaciones.
* Editar publicaciones.
* Activar o desactivar el blog globalmente.
* Configurar fechas de publicación.
* Agregar textos enriquecidos.
* Incorporar imágenes.
* Agregar hipervínculos.
* Visualización pública de las publicaciones.

### Analíticas de Tráfico Internas

Sistema integrado para registrar y consultar las visitas del sitio.

Permite visualizar estadísticas:

* Por año.
* Por mes.
* Desde el lanzamiento del sitio.
* Mediante gráficos de líneas interactivos.

### Optimización SEO Dinámica

Configuración SEO directamente desde el panel de administración:

* Título de página (`<meta title>`).
* Descripción para motores de búsqueda.
* Etiquetas **Open Graph**.
* Configuración independiente sin necesidad de modificar las plantillas manualmente.

### Integración con Redes Sociales

Módulo preparado para la integración con APIs externas, permitiendo mostrar publicaciones recientes de plataformas como **Instagram** directamente en la landing page.

### Stack Ligero y Portable

Diseñado para ser sencillo de instalar, mantener y desplegar.

* Dependencias mínimas.
* Sin servidores de bases de datos complejos.
* Base de datos **SQLite**.
* Arquitectura fácil de transportar y adaptar.

---

## Stack Tecnológico

| Tecnología         | Descripción                                           |
| ------------------ | ----------------------------------------------------- |
| **Python**         | Lenguaje de desarrollo principal.                     |
| **Flask**          | Framework web ligero para el servidor.                |
| **SQLite**         | Base de datos relacional local.                       |
| **Jinja2**         | Motor de plantillas HTML.                             |
| **Bootstrap**      | Estilos y maquetación responsiva.                     |
| **Font Awesome**   | Iconografía para la interfaz de usuario.              |
| **Chart.js**       | Biblioteca JS para gráficos y visualización de datos. |

---

## Estructura del Proyecto

```text
DynamicLanding/
│
├── app.py                  # Archivo principal de rutas y lógica de Flask
├── database.py             # Inicialización del esquema SQLite
├── requirements.txt        # Dependencias del proyecto
├── database.db             # Base de datos SQLite (generada localmente)
│
├── static/                 # Archivos estáticos
│   ├── css/                # Hojas de estilo
│   ├── js/                 # Scripts JavaScript
│   └── uploads/            # Imágenes y archivos subidos
│
└── templates/              # Plantillas HTML con Jinja2
    ├── admin/              # Vistas del Dashboard
    │   ├── Contenidos
    │   ├── Blog
    │   ├── SEO
    │   └── Analíticas
    │
    └── public/             # Vistas públicas
        ├── Landing Page
        └── Blog
```
---
## Modelo de Base de Datos

El sistema utiliza un esquema relacional optimizado en SQLite para gestionar contenidos, módulos, blog y analíticas de forma limpia y sin redundancias:


<img width="8192" height="2326" alt="ER_model" src="https://github.com/user-attachments/assets/193edd9b-33c4-40e3-9a94-db1eb9a61e91" />
<p align="center">
  <em>Figura 1: Modelo relacional de la base de datos.</em>
</p>

---

## Instalación y Configuración Local

Sigue los siguientes pasos para ejecutar **DynamicLanding** en tu entorno local.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/dynamiclanding.git
cd dynamiclanding
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos

Ejecuta el script de configuración para crear las tablas necesarias en SQLite:

```bash
python database.py
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

Una vez iniciada la aplicación, abre tu navegador y visita:

```text
http://127.0.0.1:5000
```

---

## Acceso al Sistema

Una vez ejecutada la aplicación encontrarás:

**Landing Page pública**

```text
http://127.0.0.1:5000
```

**Panel de Administración**

```text
http://127.0.0.1:5000/admin
```

> La ruta exacta del panel puede variar según la configuración de las rutas definidas en `app.py`.

---

## Objetivo del Proyecto

DynamicLanding nace como una solución **simple, flexible y ligera** para desarrollar sitios comerciales que puedan ser administrados posteriormente por usuarios sin necesidad de modificar directamente el código fuente.

El objetivo es centralizar la gestión de:

```text
Contenido
   ↓
Diseño
   ↓
Módulos
   ↓
Blog
   ↓
SEO
   ↓
Redes Sociales
   ↓
Analíticas
```

Todo desde un único **Dashboard de administración**.

---

## Estado del Proyecto

**En desarrollo**

El proyecto continúa evolucionando con nuevas funcionalidades, mejoras de interfaz, optimización del código e integración de nuevos módulos.

---

## Tecnologías y Arquitectura

DynamicLanding está construido siguiendo una arquitectura web sencilla y portable, buscando mantener un equilibrio entre:

* Rendimiento
* Modularidad
* Facilidad de mantenimiento
* Portabilidad
* Personalización
* Administración segura

---

## Licencia

Este proyecto está actualmente en desarrollo. La información sobre su licencia y condiciones de uso será incorporada posteriormente.

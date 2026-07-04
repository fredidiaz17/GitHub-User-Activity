[Proyecto Anterior (Proyecto #1 - Task Tracker)](https://github.com/fredidiaz17/Task-Traker-CLI)

> 🌐 [Read this in English](README.md)

# Proyecto #2 - GitHub User Activity

GitHub User Activity es un proyecto extraído de [Roadmap.sh](https://roadmap.sh/projects/github-user-activity).

## ¿De qué trata?

El proyecto hace uso de la API de GitHub para obtener los **eventos** realizados por un usuario en los últimos 30 días (siendo este el plazo máximo que ofrece la API) y mostrarlos de manera presentable.

Adicionalmente, el proyecto incluye la funcionalidad de consultar los **repositorios** de un usuario, haciendo uso de otro endpoint de la API de GitHub.

Todo el programa se ejecuta desde la línea de comandos (CLI) y **sin librerías externas** (por lo que librerías como `requests` están descartadas).

---

## Requisitos previos

- Python **3.10** o superior (se hace uso de `match` statements)
- No requiere dependencias externas

---

## Instalación y ejecución

1. Clonamos el repositorio.
```bash
git clone https://github.com/fredidiaz17/github-user-activity.git
```

2. Nos ubicamos en la carpeta del proyecto. Ejemplo:

```bash
cd github-user-activity
```
3. Ejecutamos el programa según lo que queramos usar. Ejemplo:
```bash
python github-activity.py <usuario> -e
```

---

## Uso y argumentos

El programa recibe un **usuario de GitHub** como parámetro obligatorio, junto con uno de los dos modos de consulta disponibles: **eventos** o **repositorios** (ambos son mutuamente excluyentes).

### Usuario
Parámetro posicional obligatorio. Indica el usuario de GitHub sobre el que se realizará la consulta.

---

### `-e` / `--event` — Eventos
Consulta los eventos del usuario en los últimos 30 días.

```bash
python github-activity.py fredidiaz17 -e
```

#### Parámetros opcionales para Eventos

| Argumento | Abreviatura | Descripción | Ejemplo |
|-----------|-------------|-------------|---------|
| `--filter` | `-f` | Filtra los eventos por tipo. | `python github-activity.py fredidiaz17 -e -f pushes` |

---

### `-r` / `--repos` — Repositorios
Consulta los repositorios públicos del usuario.

```bash
python github-activity.py fredidiaz17 -r
```

#### Parámetros opcionales para Repositorios

| Argumento | Abreviatura | Descripción | Ejemplo |
|-----------|-------------|-------------|---------|
| `--contains` | `-c` | Filtra repos cuyo nombre contenga el texto indicado. | `python github-activity.py fredidiaz17 -r -c task` |
| `--language` | `-l` | Filtra repos por lenguaje predominante. | `python github-activity.py fredidiaz17 -r -l C` |

---

## Funcionalidades adicionales

### Caché
Cada consulta a la API guarda su resultado en caché localmente, evitando llamadas redundantes para el mismo usuario dentro de un intervalo de tiempo determinado. El programa genera y utiliza dos archivos de caché: uno para **eventos** y otro para **repositorios**.
* **Validez**: Ambas cachés tienen un periodo válido de 1 hora. La API vuelve a ser consultada una vez pasada dicha hora o al preguntar por otro usuario.
* **Nombre y ubicación**: La caché de **eventos** recibe el nombre de `events.json`, el de **repositorios** se llama `repos.json`. Ambos archivos son guardados en la carpeta `cache/`.


### Argparse
El manejo de argumentos se realiza con `argparse`, módulo de la biblioteca estándar de Python, lo que garantiza una experiencia de CLI cómoda y consistente sin incumplir la restricción de librerías externas.

---

## Estructura del proyecto
```text
github-user-activity/
├── github-activity.py       # Punto de entrada del programa
├── cache/                   # Generado automáticamente al hacer la primera consulta
│   ├── events.json    
│   └── repos.json
├── src/
│   ├── g_a_events.py
│   ├── g_a_repos.py
│   ├── g_a_requests.py
│   └── github_activity_functions.py
└── README.md
```


---

## Limitaciones

- La API de GitHub limita el historial de eventos a los **últimos 30 días**.
- Solo se consultan repositorios y eventos **públicos**.
- La API de GitHub tiene un rate limiting de 60 por hora a usuarios sin token de autenticación.

---

## Retos durante el desarrollo

1. **Construcción de mensajes por evento**: La documentación oficial de GitHub no especifica el mensaje a mostrar para cada tipo de evento; fue necesario recurrir a foros y referencias de la comunidad.
2. **Diversidad de payloads**: Cada evento tiene su propio payload, con estructuras variables entre sí. La documentación oficial ofrece información limitada al respecto, lo que requirió exploración adicional.

---

## Licencia

Este es un **proyecto personal sin licencia definida**.

---

[Siguiente Proyecto (Proyecto #3 - Expense-Tracker)](https://github.com/fredidiaz17/Expense-Tracker)
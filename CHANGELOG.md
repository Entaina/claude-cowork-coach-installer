# Changelog

Todos los cambios relevantes del coach se anotan aquí. El formato sigue [Keep a Changelog](https://keepachangelog.com/es/) y el versionado es [Semántico](https://semver.org/lang/es/) (`MAYOR.MENOR.PARCHE`).

Este archivo cuenta **qué** cambió en cada versión. **Cómo** aplicarlo a una instalación existente vive en `migrations/<versión>.md`, que `UPDATE.md` ejecuta en orden al actualizar. Ni este archivo ni las migraciones se copian a tu carpeta — se leen desde el repositorio, igual que `INSTALL.md`.

Las secciones de cada versión usan el vocabulario de las migraciones — **Añadido**, **Cambiado**, **Retirado**, **Migrado** (cambios de sitio o de forma que conservan el contenido) y **Repo** (solo repositorio) — cuyas reglas exactas define `UPDATE.md`. El marcador `AIOS/VERSION.md` lo fija el propio proceso de actualización al completar cada versión; al actualizar nunca se copia del repositorio.

Regla de oro de la actualización: **nunca toca contenido tuyo** — `ME.md`, `projects/`, `areas/`, `knowledge/` ni `episodic/` — y **nunca borra** skills ni entradas que tú hayas creado. Solo añade y modifica lo que aquí se lista. Una operación **Migrado** puede mover o reformatear también skills tuyas, pero conservando su contenido íntegro y siempre con tu OK: migrar no es borrar.

## [2.3.1] - 2026-10-27

Claude Code en Windows sin Git ni pasos manuales con Python. Cómo actualizar, en `migrations/2.3.1.md`.

### Cambiado

- `AIOS/integrations/claude_code.py` — el hook `SessionStart` se registra sin shell: Claude Code lanza el Python que hizo la instalación por su ruta absoluta, con el adaptador como argumento. Deja de depender de `python3`, que en Windows suele faltar o abrir la Microsoft Store, y de las diferencias de comillas entre Git Bash y PowerShell. Reinstalar sustituye en su sitio el hook de texto de 2.2.0–2.3.0. Sin base de zonas horarias (Windows sin `tzdata`), el lector corta el día con la hora local del sistema e indica `timezone_source: system`.
- `AIOS/claude-code.md` — Python pasa a ser un paso de la instalación: el agente lo comprueba y, si falta, lo instala con el OK del usuario (`winget` para el usuario en Windows, herramientas de línea de comandos en macOS). Git no se instala y el aviso de Claude Code de que no está disponible se explica como normal. Ya no se pide `tzdata`.

### Repo (no se aplica a tu carpeta)

- README e INSTALL — Python lo instala el coach y Git no hace falta.
- Pruebas — hook sin shell ejecutado como lo lanza Claude Code, sustitución del hook de 2.3.0, intérprete no identificable y lector sin base de zonas. Originales 2.3.0 de los dos archivos cambiados y su prueba de integridad.

Contrastado el 2026-10-27 en Linux con Claude Code 2.1.310: el hook sin shell registra la sesión y el lector recupera sus mensajes. Windows sigue sin probarse en una máquina real.

## [2.3.0] - 2026-10-27

Compatibilidad con la app de escritorio de Amazon Quick, sobre la misma carpeta local, y zona horaria del usuario en lugar de Madrid fija. Cowork, Claude Code y GPT conservan sus adaptadores. Cómo actualizar, en `migrations/2.3.0.md`.

### Añadido

- `AIOS/amazon-quick.md` — preparación de la carpeta en Quick, agente Coach que lee `AGENTS.md` al empezar cada conversación, lectura del historial de la cuenta, una revisión conjunta programada con el equipo encendido y la app abierta, verificación y límites conocidos.

### Cambiado

- Zona horaria del usuario — el coach fecha el día, las señales, el intervalo de conversaciones y los horarios con la línea «Zona horaria» de `ME.md` (identificador IANA). Sin esa línea, como en las instalaciones anteriores, sigue usando `Europe/Madrid`. Cambian `AIOS/entornos-locales.md` (la regla), `episodic-learner`, los sistemas de Learning y Proyectos y el mapa de contenido.
- `AIOS/claude-code.md` y `AIOS/integrations/claude_code.py` — el lector de historial toma la zona de `ME.md`, admite `--tz` e informa de la zona usada; `/coach-review` elige el día en esa zona. Sin la línea, mismo resultado que en 2.2.0.
- `AIOS/entornos-locales.md` — Quick en el alcance, el arranque, el historial y la programación. La versión web de Quick queda fuera, con el resto de modalidades cloud.
- Mapas y sistemas de Learning/Proyectos — Quick ejecuta las dos fases en una sola revisión, como GPT local, y su primera comprobación es una ejecución única a pocos minutos vista.
- Descripción de `episodic-learner` — incluye Quick; su workflow se conserva.

### Repo (no se aplica a tu carpeta)

- README e INSTALL — instalación en Quick con la ruta de la carpeta al principio del prompt, creación del agente Coach por el usuario y rutina dentro de la jornada. La entrevista confirma la zona horaria a partir de la ubicación y la plantilla `ME.md` gana la línea «Zona horaria»; solo afecta a instalaciones nuevas.
- Migración 2.3.0 con los ocho originales afectados de 2.2.0; no cambia los dos arranques ni los datos del usuario, `ME.md` incluido.
- Prueba de integridad de esos originales y prueba del lector con una zona distinta de Madrid; `AIOS/VERSION.md` del repositorio pasa a 2.3.0.

Contrastado el 2026-10-27 en macOS con Quick 1.1.3905 y una cuenta individual. La revisión conjunta completa, varias ejecuciones diarias, las cuentas de empresa con administrador y Windows siguen sin probar.

## [2.2.0] - 2026-10-07

Integración nativa de Claude Code CLI en la carpeta local del coach. Cowork y GPT conservan sus adaptadores. Cómo actualizar, en `migrations/2.2.0.md`.

### Añadido

- `AIOS/claude-code.md` — configuración, historial, revisión y verificación de Code; requiere Python 3.9+ y zona horaria Europe/Madrid.
- `AIOS/integrations/claude_code.py` — instalación local con vista previa, wrappers delgados de skills, `/coach-review` y hook SessionStart que registra solo metadatos de esta carpeta. Lector acotado a las transcripciones registradas, con fechas/fuentes, límites de lectura y cobertura parcial. No escanea historiales globales ni cambia permisos o programaciones.

### Cambiado

- `AIOS/entornos-locales.md`, mapas y sistemas de Learning/Proyectos — incorporan Code y la revisión conjunta a demanda. La programación del CLI depende de una sesión activa; no se presenta como tarea nocturna permanente.
- Descripción de `episodic-learner` — incluye Code; su workflow se conserva.
- `skill-installer` — reutiliza el alcance que ya haya elegido el usuario, concreta la ubicación nativa de Code y detiene la actualización ante wrappers personalizados.

### Repo (no se aplica a tu carpeta)

- README e INSTALL — añaden la instalación de Code en la carpeta permanente y su prueba en una sesión nueva. Las skills/hook se generan al activar esta integración, no se copian ya activados a otras apps.
- Migración 2.2.0 con los siete originales afectados de 2.1.0; no cambia los dos arranques ni los datos del usuario.
- Pruebas del adaptador y originales; `AIOS/VERSION.md` del repositorio pasa a 2.2.0.

El historial JSONL de Claude es un formato interno: cambios o fuentes inaccesibles se comunican como límites, nunca como falta de actividad. Las sesiones anteriores al alta no se importan automáticamente. Antigravity y cloud siguen fuera.

## [2.1.0] - 2026-09-22

Entrevista breve y soporte para ChatGPT Work / Codex en la app local, conservando Cowork. El acceso al historial se adapta a las herramientas realmente disponibles y declara la cobertura. Cómo aplicarlo, en `migrations/2.1.0.md`.

### Añadido

- `AGENTS.md` — las mismas instrucciones completas que `CLAUDE.md`, para que cada app use el archivo que reconoce. Ambos se mantienen sincronizados.
- `AIOS/entornos-locales.md` — acceso nativo a conversaciones de Cowork y GPT local, filtrado por proyecto/fecha, cobertura y programación. En GPT, una revisión conjunta; en Cowork, se conservan las dos tareas.

### Cambiado

- `CLAUDE.md` — conserva el arranque completo y coincide con `AGENTS.md`; se actualizan ambos en conjunto. La actualización preserva las reglas personalizadas y resuelve las diferencias antes de escribir.

- `AIOS/mapa-contenido.md` y `AIOS/mapa-skills.md` — registran el arranque común y el acceso a conversaciones de GPT. El mapa de contenido aclara cómo completar un día histórico a petición explícita sin perder su contenido ni propuestas.
- `AIOS/skills/episodic-learner/SKILL.md` — usa el adaptador local disponible, indica cobertura, no interpreta falta de acceso como falta de actividad y conserva señales/propuestas al reejecutarse. Los compromisos requieren evidencia del usuario.
- Las descripciones de `semantic-learner` y `procedural-learner` reflejan el orden secuencial; se mantienen sus criterios de aprendizaje.
- `AIOS/systems/learning-system.md` — las pasadas escriben en secuencia, mantienen el mismo día/log al cruzar medianoche y respetan propuestas ya resueltas; distingue prueba manual y ejecución programada.
- `AIOS/systems/proyectos-y-areas.md` — admite objetivos sin definir y la revisión conjunta en GPT; conserva la fecha del log y evita regenerar propuestas resueltas.

### Repo (no se aplica a tu carpeta)

- `INSTALL.md`, `README.md` y plantilla `ME.md` — tres bloques de entrevista, asistente personal y Goals opcionales. Los huecos de contexto detectados (rol, tareas frecuentes…) quedan en Pendientes para próximas sesiones, sin alargar la entrevista ni convertirlos en compromisos. Reanudación sin volver a copiar y prueba válida con cero propuestas.
- `migrations/2.1.0.md` y sus originales 2.0.0 — actualización conservadora y retomable; no cambia ME.md ni configura tareas automáticamente. Advierte del prompt antiguo de Cowork y ofrece adaptarlo con confirmación.
- `tests/` — comprobaciones del paquete y guía de pruebas de comportamiento; se excluye de la copia al usuario.
- `AIOS/VERSION.md` del repositorio pasa a `2.1.0`. Las releases de GitHub se gestionan aparte.

Antigravity, las modalidades web/cloud y la adaptación del historial de Claude Code CLI no se incorporan en esta versión.

## [2.0.0] - 2026-07-23

Las skills adoptan el estándar [Agent Skills](https://agentskills.io/specification): cada una pasa de archivo suelto a directorio con su `SKILL.md`, y su frontmatter al formato de la especificación — `name`, `description` (con las frases de disparo dentro) y `metadata` (`system`, `status`, fechas). Cambia la forma, no el contenido — con una excepción declarada: las tres skills que gestionan skills actualizan además su workflow. Es un salto MAYOR porque rompe las rutas canónicas y el esquema anterior. Cómo aplicarlo, en `migrations/2.0.0.md`.

### Migrado

- Las 11 skills del coach (contenido-janitor, episodic-learner, procedural-learner, project-janitor, project-learner, project-manager, pulidor, semantic-learner, skill-builder, skill-installer, skills-janitor) — de `AIOS/skills/<name>.md` a `AIOS/skills/<name>/SKILL.md`. En las ocho primeras solo cambian ruta y frontmatter (y en project-manager, una línea corregida: la detección diaria es de project-learner, no de semantic-learner); en skill-builder, skills-janitor y skill-installer también el workflow, puesto al día con el formato nuevo.
- Las skills creadas por el usuario — se transforman al formato nuevo en su carpeta, conservando el contenido íntegro.
- `AIOS/Templates/skill-template.md` — sustituida por la plantilla del formato nuevo (si la editaste, se te enseña la diferencia y eliges, como con las skills).

### Cambiado

- `AIOS/systems/skills.md` — nueva sección **El formato** (el contrato del estándar y su URL); skills-janitor pasa a auditar contra ella; los ejemplos, al formato nuevo.
- `AIOS/systems/pulidor.md`, `AIOS/systems/learning-system.md` y `AIOS/Templates/system-template.md` — retoques de una línea (las frases de disparo viven en la description; "archivo o directorio nuevo"; vocabulario).
- `AIOS/mapa-contenido.md` y `AIOS/mapa-skills.md` — la estructura de `skills/`, el destino de la plantilla y los estados apuntan al formato nuevo.

### Retirado

- Copias locales obsoletas de archivos del repositorio en la raíz de tu carpeta, solo si existen: `CHANGELOG.md`, `UPDATE.md`, `INSTALL.md`, `README.md`. No forman parte de la instalación — se leen siempre del repositorio.

> Al completar la migración hay que regenerar los wrappers que skill-installer hubiera instalado en tus agentes (apuntan a las rutas viejas); la migración lo recuerda al final.

### Repo (no se aplica a tu carpeta)

- `migrations/` — nuevo. Un archivo de instrucciones por versión (`migrations/1.1.0.md`, `migrations/2.0.0.md`), que `UPDATE.md` ejecuta en orden al actualizar, más su material de apoyo (`migrations/2.0.0/originals/`: los originales 1.1.0 de las 11 skills y de la plantilla, para detectar por comparación exacta si editaste algo). El CHANGELOG cuenta qué cambió; la migración, cómo aplicarlo.
- `UPDATE.md` — pasa a ser el ejecutor de migraciones: aplica `migrations/<versión>.md` por cada versión pendiente y define el vocabulario de operaciones (con la nueva **Migrado** y la regla de rutas movidas).
- `CHANGELOG.md` — el preámbulo remite a las migraciones; la regla de oro aclara que migrar no es borrar.
- `README.md` — el prompt de instalación excluye también `migrations/` de la copia; el de actualización pide aplicar también las migraciones que declare el CHANGELOG (antes prometía "de forma aditiva"); la descripción de `AIOS/` menciona el directorio por skill.
- `AIOS/VERSION.md` del repositorio pasa a `2.0.0` (el de tu carpeta lo fija el propio proceso de actualización al completar).

## [1.1.0] - 2026-07-16

Se incorpora `skill-installer` y se estrena el sistema de actualización (este `CHANGELOG.md`, `UPDATE.md` y el marcador `AIOS/VERSION.md`). Cómo aplicarlo, en `migrations/1.1.0.md`.

### Añadido

- `AIOS/skills/skill-installer.md` — nueva skill. Proyecta una skill canónica de `AIOS/skills/` al agente anfitrión (Cowork, Claude Code…) como skill nativa que el host descubre y dispara solo, con un wrapper delgado que apunta al canónico. No duplica el workflow ni usa symlinks. Cópiala tal cual desde el repositorio. *(Nota de la 2.0.0: esta ruta ya no existe en el repositorio — la skill vive ahora en `AIOS/skills/skill-installer/SKILL.md`. Si vienes de 1.0.0, salta esta copia: la migración de la 2.0.0 la crea directamente en su forma nueva.)*

> `AIOS/VERSION.md` se estrena en esta versión como marcador de versión, pero **no** es un archivo que se copie al actualizar (ver la nota del marcador en el preámbulo): lo escribe el propio proceso de actualización con la versión que va aplicando. En esta actualización, quedará en `1.1.0` al completarla.

### Cambiado

- `AIOS/systems/skills.md` — registrar `skill-installer`: (1) añadir `skill-installer` al final de la lista `skills:` del frontmatter; (2) añadir su bullet en la sección **Skills**; (3) añadir su línea en **Orquestación**; (4) el resumen del sistema ahora menciona que las skills "se proyectan nativas al agente anfitrión". Edición aditiva — conserva el resto de skills que tengas registradas.
- `AIOS/mapa-skills.md` — añadir la entrada de `skill-installer` bajo la sección **Skills — las capacidades del coach, gestionadas**, tras `skills-janitor`. Edición aditiva.
- `AIOS/mapa-contenido.md` — en la línea de `AIOS/` de la sección **Navegación**, mencionar `VERSION.md` como la versión instalada del coach. Edición aditiva.

### Repo (no se aplica a tu carpeta)

- `UPDATE.md` — nuevo. Prompt de actualización que un agente ejecuta desde el repositorio, análogo a `INSTALL.md`.
- `CHANGELOG.md` — nuevo (este archivo).
- `README.md` — nueva sección **Actualización** con su prompt para copiar y pegar; el prompt de **Instalación** ahora excluye también `UPDATE.md` y `CHANGELOG.md` de la copia.

## [1.0.0] - 2026-07-16

Primera versión con seguimiento del coach: arranque (`CLAUDE.md`, `ME.md`), mapas (`AIOS/mapa-contenido.md`, `AIOS/mapa-skills.md`), plantillas, sistemas y skills de Learning, Skills, Contenido, Proyectos y Áreas, y Pulidor, más el flujo de instalación (`README.md`, `INSTALL.md`).

Toda instalación anterior a `1.1.0` — es decir, sin `AIOS/VERSION.md` — se considera `1.0.0` a efectos de actualización.

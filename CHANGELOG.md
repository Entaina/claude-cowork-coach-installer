# Changelog

Todos los cambios relevantes del coach se anotan aquí. El formato sigue [Keep a Changelog](https://keepachangelog.com/es/) y el versionado es [Semántico](https://semver.org/lang/es/) (`MAYOR.MENOR.PARCHE`).

Este archivo cuenta **qué** cambió en cada versión. **Cómo** aplicarlo a una instalación existente vive en `migrations/<versión>.md`, que `UPDATE.md` ejecuta en orden al actualizar. Ni este archivo ni las migraciones se copian a tu carpeta — se leen desde el repositorio, igual que `INSTALL.md`.

Las secciones de cada versión usan el vocabulario de las migraciones — **Añadido**, **Cambiado**, **Retirado**, **Migrado** (cambios de sitio o de forma que conservan el contenido) y **Repo** (solo repositorio) — cuyas reglas exactas define `UPDATE.md`. El marcador `AIOS/VERSION.md` lo fija el propio proceso de actualización al completar cada versión; al actualizar nunca se copia del repositorio.

Regla de oro de la actualización: **nunca toca contenido tuyo** — `ME.md`, `projects/`, `areas/`, `knowledge/` ni `episodic/` — y **nunca borra** skills ni entradas que tú hayas creado. Solo añade y modifica lo que aquí se lista. Una operación **Migrado** puede mover o reformatear también skills tuyas, pero conservando su contenido íntegro y siempre con tu OK: migrar no es borrar.

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

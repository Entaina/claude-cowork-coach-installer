# Changelog

Todos los cambios relevantes del coach se anotan aquí. El formato sigue [Keep a Changelog](https://keepachangelog.com/es/) y el versionado es [Semántico](https://semver.org/lang/es/) (`MAYOR.MENOR.PARCHE`).

Este archivo es la fuente para actualizar una instalación ya existente: `UPDATE.md` lo lee y aplica, versión a versión, solo los cambios que le falten. No se copia a tu carpeta — se lee desde el repositorio al actualizar, igual que `INSTALL.md`.

**Cómo leer cada versión al actualizar:**

- **Añadido** — archivos nuevos que no tienes. Se copian tal cual desde el repositorio, a la misma ruta.
- **Cambiado** — archivos que ya tienes y que pueden llevar añadidos tuyos (mapas, sistemas). Se editan de forma **quirúrgica**: se añade solo lo que indica la entrada, sin sobrescribir el archivo entero. Si algo ya está, se salta.
- **Retirado** — archivos o entradas que se eliminan. Se retira solo lo nombrado explícitamente, y siempre con tu confirmación.
- **Repo** — cambios que solo viven en el repositorio (`README.md`, `INSTALL.md`, este archivo…). No hay nada que aplicar en tu carpeta.

El marcador `AIOS/VERSION.md` es **especial**: la actualización nunca lo copia ni lo aplica entrada por entrada, aunque una versión lo mencione. Lo gestiona el propio proceso, fijándolo a cada versión a medida que la completa (ver `UPDATE.md`), para que el marcador jamás vaya por delante de lo realmente aplicado.

Regla de oro de la actualización: **nunca toca contenido tuyo** — `ME.md`, `projects/`, `areas/`, `knowledge/` ni `episodic/` — y **nunca borra** skills ni entradas que tú hayas creado. Solo añade y modifica lo que aquí se lista.

## [1.1.0] - 2026-07-16

Se incorpora `skill-installer` y se estrena el sistema de actualización (este `CHANGELOG.md`, `UPDATE.md` y el marcador `AIOS/VERSION.md`).

### Añadido

- `AIOS/skills/skill-installer.md` — nueva skill. Proyecta una skill canónica de `AIOS/skills/` al agente anfitrión (Cowork, Claude Code…) como skill nativa que el host descubre y dispara solo, con un wrapper delgado que apunta al canónico. No duplica el workflow ni usa symlinks. Cópiala tal cual desde el repositorio.

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

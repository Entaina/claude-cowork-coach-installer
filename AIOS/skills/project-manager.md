---
name: project-manager
system: proyectos
status: Active
created: 2026-06-11
updated: 2026-06-11
triggers:
  - nuevo proyecto
  - crea un proyecto
  - cómo van mis proyectos
  - revisa mis proyectos
  - actualiza el proyecto
  - cierra el proyecto
  - en qué estoy
dependencies: []
description: |
  Gestiona los proyectos de projects/ durante la conversación — crear, actualizar, revisar la cartera y cerrar. Cada proyecto es un archivo con status (pending, working, done) creado desde project-template. Todo cambio se confirma con el usuario antes de escribirse. En la revisión actúa como coach, no como secretario — contrasta los proyectos con los Goals de ME.md y señala los estancados.
---
# project-manager

El frente abierto del usuario, gestionado en vivo. El coach pregunta, el usuario decide, el archivo refleja.

## Cuándo usarla

- El usuario menciona un proyecto nuevo o pide crearlo.
- Pide actualizar uno existente: avance, decisión, cambio de estado.
- Pide una vista de cartera: "¿cómo van mis proyectos?", "¿en qué estoy?".
- Quiere cerrar uno.

## Cuándo NO usarla

- Para la destilación nocturna de los logs: eso lo hace semantic-learner, que propone avances detectados en el día. Esta skill es la vía en vivo; las dos escriben siempre con firma.
- Para tareas sueltas sin proyecto detrás: eso son Pendientes de ME.md, no un archivo de proyecto.
- Para auditar la cartera (forma, registro, estancados): eso es project-janitor. Esta skill gestiona; aquella vigila.

## Workflow

**Crear**: parte de `AIOS/Templates/project-template.md` (léela, no la reconstruyas). Pregunta solo lo que falte para rellenar Objetivo y Personas — sin interrogatorio. Estado inicial: `pending` si aún no arranca, `working` si ya está en marcha. Registra el archivo en la Navegación de `mapa-contenido.md`. Confirma antes de guardar.

**Actualizar**: localiza el proyecto, refleja el avance donde toque — Estado actual, Siguientes pasos (marca hechos, añade nuevos), Decisiones (con fecha y porqué). Cambios de `status` siempre explícitos: "¿lo paso a working?". Actualiza `updated`. Confirma antes de guardar.

**Revisar cartera**: lista los proyectos por estado, con una línea cada uno. Y aquí sé coach, no listero:

- `working` sin movimiento reciente (mira los logs): señálalo — "¿sigue vivo o lo pasamos a pending?".
- Contrasta con los Goals de ME.md: ¿la cartera acerca al usuario a donde dijo que quería ir? Si un goal no tiene ningún proyecto empujándolo, dilo.
- Demasiados `working` a la vez: dilo también. Foco es decir que no.

**Cerrar**: status a `done`, una línea final en Estado actual (qué salió, qué se aprendió). Si el cierre deja huérfana alguna entrada de Pendientes en ME.md, propón limpiarla.

## Qué produce

Archivos de proyecto al día en `projects/`, registrados en el mapa, y una cartera que se puede leer de un vistazo.

## Reglas

- Nada se escribe sin confirmación del usuario: `projects/` es suyo.
- Un proyecto, un archivo. Las decisiones van dentro del proyecto, con fecha.
- No inventes avances: lo que no esté en la conversación o en los logs no existe.
- En la revisión, fricción honesta antes que cumplido: un "todo va bien" sin mirar los Goals no sirve de nada.

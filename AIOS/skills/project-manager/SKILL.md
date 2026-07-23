---
name: project-manager
description: >-
  Gestiona los proyectos de projects/ y las áreas de areas/ durante la
  conversación — crear, actualizar, revisar y cerrar o archivar. Proyecto =
  resultado con final (pending, working, done); área = responsabilidad
  continua con estándar (active, archived); el test es "¿puede acabarse?".
  Todo cambio se confirma con el usuario antes de escribirse. En la revisión
  actúa como coach, no como secretario — cartera agrupada por área, contraste
  con los Goals de ME.md, estancados y áreas descuidadas. Se activa con frases
  como: "nuevo proyecto", "crea un proyecto", "nueva área", "cómo van mis
  proyectos", "cómo van mis áreas", "revisa mis proyectos", "actualiza el
  proyecto", "cierra el proyecto", "en qué estoy".
metadata:
  system: proyectos-y-areas
  status: active
  created: "2026-06-11"
  updated: "2026-06-11"
---
# project-manager

El frente de ejecución del usuario, gestionado en vivo. El coach pregunta, el usuario decide, el archivo refleja.

## Cuándo usarla

- El usuario menciona un proyecto o una responsabilidad continua nueva, o pide crearlos.
- Pide actualizar algo existente: avance, decisión, cambio de estado, cambio de estándar de un área.
- Pide una vista de cartera: "¿cómo van mis proyectos?", "¿cómo van mis áreas?", "¿en qué estoy?".
- Al aplicar las propuestas aprobadas del project-learner en la sesión diaria del sistema (creaciones desde plantilla, actualizaciones, cambios de estado).
- Quiere cerrar un proyecto o archivar un área.

## Proyecto vs. Área

Antes de crear, aplica el test PARA: **"¿puede acabarse?"** Sí → proyecto (`projects/`, project-template, `pending|working|done`). No → área (`areas/`, area-template, `active|archived`). Si dudas, pregunta con el test a la vista. Un proyecto declara en su frontmatter `area:` a qué área empuja, si la hay.

## Cuándo NO usarla

- Para la detección diaria sobre el log: eso lo hace project-learner, que propone proyectos nuevos y avances detectados en el día. Esta skill es la vía en vivo; las dos escriben siempre con firma.
- Para tareas sueltas sin proyecto detrás: eso son Pendientes de ME.md, no un archivo de proyecto.
- Para auditar la cartera (forma, registro, estancados): eso es project-janitor. Esta skill gestiona; aquella vigila.

## Workflow

**Crear un proyecto**: parte de `AIOS/Templates/project-template.md` (léela, no la reconstruyas). Pregunta solo lo que falte para rellenar Objetivo, área a la que empuja y Personas — sin interrogatorio. Estado inicial: `pending` si aún no arranca, `working` si ya está en marcha. Registra el archivo en la Navegación de `mapa-contenido.md`. Confirma antes de guardar.

**Crear un área**: parte de `AIOS/Templates/area-template.md` (léela). Lo que define un área es su **Estándar** — qué significa que esté "bien" —; no la crees sin él. Estado inicial `active`. Registra y confirma igual.

**Actualizar**: localiza el archivo, refleja el cambio donde toque — en proyectos: Estado actual, Siguientes pasos, Decisiones (con fecha y porqué); en áreas: Estándar, Personas, Notas. Cambios de `status` siempre explícitos: "¿lo paso a working?", "¿la archivo?". Actualiza `updated`. Confirma antes de guardar.

**Revisar cartera**: agrupa los proyectos por área (los sin área, al final) y lista las áreas con su estándar en una línea. Y aquí sé coach, no listero:

- `working` sin movimiento reciente (mira los logs): señálalo — "¿sigue vivo o lo pasamos a pending?".
- Áreas descuidadas: si sus Señales de salud llevan tiempo sin buena pinta en los logs, dilo.
- Contrasta con los Goals de ME.md: ¿la cartera acerca al usuario a donde dijo que quería ir? Si un goal no tiene ningún proyecto ni área empujándolo, dilo.
- Demasiados `working` a la vez: dilo también. Foco es decir que no.

**Cerrar / archivar**: proyecto → status `done`, una línea final en Estado actual (qué salió, qué se aprendió). Área → status `archived` solo si la responsabilidad de verdad terminó (cambio de rol, traspaso); las áreas no se "acaban" por aburrimiento. Si el cierre deja huérfana alguna entrada de Pendientes en ME.md, propón limpiarla.

## Qué produce

Archivos de proyecto al día en `projects/`, registrados en el mapa, y una cartera que se puede leer de un vistazo.

## Reglas

- Nada se escribe sin confirmación del usuario: `projects/` es suyo.
- Un proyecto, un archivo. Las decisiones van dentro del proyecto, con fecha.
- No inventes avances: lo que no esté en la conversación o en los logs no existe.
- En la revisión, fricción honesta antes que cumplido: un "todo va bien" sin mirar los Goals no sirve de nada.

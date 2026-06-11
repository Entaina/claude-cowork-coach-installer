---
name: proyectos
skills: project-manager, project-janitor
created: 2026-06-11
---
# Sistema Proyectos

Mantiene visible, al día y fiable el frente abierto del usuario: qué proyectos hay, en qué estado están y si la cartera empuja hacia los Goals. Los proyectos viven en `projects/` como memoria de trabajo — un archivo por proyecto, con `status: pending | working | done`.

## Skills

- **project-manager**: crea, actualiza, revisa y cierra proyectos durante la conversación, siempre con confirmación. En la revisión actúa como coach: señala estancados y contrasta la cartera con los Goals.
- **project-janitor**: audita `projects/` contra la plantilla, el mapa y los logs — forma, registro y ciclo de vida (working estancados, pending eternos, done a medias). Reporta primero, arregla con aprobación.

## Orquestación

A demanda, sin tareas programadas propias. El sistema tiene tres vías que se complementan:

- **En vivo**: project-manager, cuando el usuario habla de sus proyectos.
- **En diferido**: semantic-learner (Learning System) detecta avances en los logs nocturnos y los propone; al firmarlos, se aplican a los archivos de `projects/`.
- **Higiene**: project-janitor, periódicamente o antes de una revisión de cartera, para que la revisión parta de datos que cuadran.

**El hand-off**: todas las vías escriben solo con firma del usuario. El janitor detecta pero nunca cambia estados — eso pasa por project-manager. El archivo del proyecto es la fuente de verdad, no el log.

## Cuándo NO usarlo

- Como gestor de tareas sueltas: lo que no tenga objetivo y siguiente paso propio son Pendientes de ME.md, no proyectos.
- Como sustituto de la herramienta de gestión del equipo (Basecamp, Jira...): aquí vive la vista *del usuario* sobre sus frentes, no el tracker del equipo.

## Ejemplos correctos

- *"Crea un proyecto para la migración del taller."* project-manager parte de la plantilla, pregunta el objetivo y quién decide, lo crea en `pending`, lo registra en el mapa y confirma.
- *"¿Están los proyectos en orden?"* project-janitor encuentra un working sin tocar en dos semanas y un proyecto sin registrar en el mapa; reporta, y con el visto bueno registra el archivo — el working estancado lo deja en manos del usuario vía project-manager.

## Ejemplos incorrectos

- *El coach actualiza el status de un proyecto porque "se deduce de la conversación", sin preguntar.* Los cambios de estado son siempre explícitos.
- *Crear un proyecto por cada tarea mencionada.* Inflación de cartera: si cabe en un Pendiente, es un Pendiente.
- *El janitor "arregla" un working estancado pasándolo a pending él solo.* El janitor detecta; decide el usuario.

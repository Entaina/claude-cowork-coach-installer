---
name: proyectos
skills: project-manager, project-learner, project-janitor
created: 2026-06-11
---
# Sistema Proyectos

Mantiene visible, al día y fiable el frente abierto del usuario: qué proyectos hay, en qué estado están y si la cartera empuja hacia los Goals. Los proyectos viven en `projects/` como memoria de trabajo — un archivo por proyecto, con `status: pending | working | done`.

## Skills

- **project-manager**: crea, actualiza, revisa y cierra proyectos durante la conversación, siempre con confirmación. En la revisión actúa como coach: señala estancados y contrasta la cartera con los Goals. Es la única vía de escritura en `projects/`.
- **project-learner**: detecta cada noche, en el log del día, proyectos nuevos y movimiento de los existentes (avances, decisiones, estados que mienten). Solo propone; las aprobadas se aplican vía project-manager.
- **project-janitor**: audita `projects/` contra la plantilla, el mapa y los logs — forma, registro y ciclo de vida (working estancados, pending eternos, done a medias). Reporta primero, arregla con aprobación.

## Orquestación

Dos vías a demanda y una programada diaria:

- **En vivo**: project-manager, cuando el usuario habla de sus proyectos.
- **Higiene**: project-janitor, a demanda o antes de una revisión de cartera, para que la revisión parta de datos que cuadran.
- **Detección diaria programada** (23:45 por defecto, Europe/Madrid — tras la nocturna del Learning System, porque lee su log). Su prompt es fino y apunta a las skills — nunca duplica sus workflows:

> "Ejecuta el Sistema Proyectos según `AIOS/systems/proyectos.md`: project-learner sobre el log de hoy; termina presentándome sus propuestas (proyectos nuevos, avances, cambios de estado) y espera mi respuesta."

**El hand-off**: todas las vías escriben solo con firma del usuario. La sesión diaria queda a la espera, como la del Learning System: el usuario responde al abrirla, el coach aplica lo aprobado vía project-manager (plantilla incluida si es creación), descarta el resto y actualiza los estados en el log. Las propuestas pendientes de días anteriores se re-presentan. El Learning System no toca `projects/`; el janitor detecta pero nunca cambia estados. El archivo del proyecto es la fuente de verdad, no el log.

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

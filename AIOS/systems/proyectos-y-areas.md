---
name: proyectos-y-areas
skills: project-manager, project-learner, project-janitor
created: 2026-06-11
---
# Sistema Proyectos y Áreas

Mantiene visible, al día y fiable el frente de ejecución del usuario: qué proyectos hay y en qué estado, qué responsabilidades continuas atiende, y si todo ello empuja hacia los Goals. Los proyectos viven en `projects/` y las áreas en `areas/`, como memoria de trabajo.

## Proyecto vs. Área (al estilo PARA)

- **Proyecto**: resultado concreto con final. Se puede terminar. `status: pending | working | done`. Vive en `projects/`.
- **Área**: responsabilidad continua con un *estándar* que mantener. No se termina: se atiende o se descuida. `status: active | archived`. Vive en `areas/`.

El test: **"¿puede acabarse?"** — sí → proyecto; no → área. Un proyecto normalmente empuja un área (lo declara en su frontmatter `area:`) o un goal; cuando el proyecto acaba, el área sigue ahí.

## Skills

- **project-manager**: crea, actualiza, revisa y cierra proyectos y áreas durante la conversación, siempre con confirmación. En la revisión actúa como coach: cartera agrupada por área, estancados, áreas descuidadas, goals sin proyecto que los empuje. Es la única vía de escritura en `projects/` y `areas/`.
- **project-learner**: detecta cada noche, en el log del día, proyectos nuevos, áreas que asoman y movimiento de los existentes (avances, decisiones, estados que mienten). Solo propone; las aprobadas se aplican vía project-manager.
- **project-janitor**: audita `projects/` y `areas/` contra plantillas, mapa y logs — forma, registro y ciclo de vida (working estancados, pending eternos, done a medias, áreas descuidadas o mal archivadas). Reporta primero, arregla con aprobación.

## Orquestación

Dos vías a demanda y una programada diaria:

- **En vivo**: project-manager, cuando el usuario habla de sus proyectos o responsabilidades.
- **Higiene**: project-janitor, a demanda o antes de una revisión de cartera, para que la revisión parta de datos que cuadran.
- **Detección diaria programada** (23:45 por defecto, Europe/Madrid — tras la nocturna del Learning System, porque lee su log). Su prompt es fino y apunta a las skills — nunca duplica sus workflows:

> "Ejecuta el Sistema Proyectos y Áreas según `AIOS/systems/proyectos-y-areas.md`: project-learner sobre el log de hoy; termina presentándome sus propuestas (proyectos nuevos, áreas nuevas, avances, cambios de estado) y espera mi respuesta."

**El hand-off**: todas las vías escriben solo con firma del usuario. La sesión diaria queda a la espera, como la del Learning System: el usuario responde al abrirla, el coach aplica lo aprobado vía project-manager (plantilla incluida si es creación), descarta el resto y actualiza los estados en el log. Las propuestas pendientes de días anteriores se re-presentan. El Learning System no toca `projects/` ni `areas/`; el janitor detecta pero nunca cambia estados. Los archivos son la fuente de verdad, no el log.

## Cuándo NO usarlo

- Como gestor de tareas sueltas: lo que no tenga objetivo y siguiente paso propio (proyecto) ni estándar que mantener (área) son Pendientes de ME.md.
- Como sustituto de la herramienta de gestión del equipo (Basecamp, Jira...): aquí vive la vista *del usuario* sobre sus frentes, no el tracker del equipo.

## Ejemplos correctos

- *"Crea un proyecto para la migración del taller."* project-manager parte de la plantilla, pregunta el objetivo, a qué área empuja y quién decide, lo crea en `pending`, lo registra en el mapa y confirma.
- *"Llevo semanas apagando fuegos con los proveedores."* No puede acabarse → es un área. project-manager propone crearla con su estándar ("pedidos servidos sin incidencias, dos revisiones al mes") y deja los fuegos concretos como proyectos o pendientes.
- *Por la mañana, sesión diaria:* "2 propuestas: (1) proyecto nuevo 'auditoría ISO' detectado en la reunión de ayer; (2) el área de equipo registra cambio — Marta pasa a coordinar el turno de tarde. ¿Cuáles aplico?"

## Ejemplos incorrectos

- *El coach cambia el status de un proyecto o archiva un área porque "se deduce", sin preguntar.* Los cambios de estado son siempre explícitos.
- *Crear un proyecto por cada tarea mencionada, o un área por cada tema.* Inflación: si cabe en un Pendiente, es un Pendiente; si no hay estándar que mantener, no es área.
- *El janitor "arregla" un working estancado pasándolo a pending él solo.* El janitor detecta; decide el usuario.

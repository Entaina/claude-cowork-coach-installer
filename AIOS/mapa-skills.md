# Mapa de skills

Catálogo de lo que el coach sabe hacer, agrupado por sistema. **Consúltalo antes de procesar cualquier petición no trivial**: si hay skill para ello, se usa. Cada skill o sistema nuevo se registra aquí en el momento de crearse (vía skill-builder) — si el mapa no lo menciona, no existe.

## Learning System — cómo aprende el coach

Ver `systems/learning-system.md`. Una tarea programada nocturna; el usuario firma por la mañana.

- **episodic-learner** — compone el log del día leyendo las sesiones de Cowork y mantiene los Pendientes de ME.md. El único que escribe directo. Triggers: `genera el log de hoy`, `cierra el día`, `reconstruye el log`.
- **semantic-learner** — propone cambios a knowledge/ y a Quién soy/Goals de ME.md, con destino, cambio y fuente. No toca projects/. No aplica nada. Triggers: `propuestas semánticas`, `qué has aprendido de mí`.
- **procedural-learner** — propone cambios a Preferencias/Reglas de ME.md y candidatas a skill cuando detecta patrones repetidos. No aplica nada. Triggers: `propuestas procedurales`, `qué deberías hacer distinto`.

## Skills — las capacidades del coach, gestionadas

Ver `systems/skills.md`. A demanda.

- **skill-builder** — crea y registra skills nuevas de forma consistente; única vía de creación. Triggers: `crea una skill`, `nueva skill`, `skill para`, `quiero capturar esto como skill`.
- **skills-janitor** — audita skills y sistemas contra mapa-skills y el esquema de skill-builder. Reporta primero, arregla con aprobación. Triggers: `audita las skills`, `están las skills en orden`, `skill drift`.

## Contenido — el mapa del territorio, fiable

Ver `systems/contenido.md`. A demanda.

- **contenido-janitor** — audita mapa-contenido contra la carpeta real (navegación) y los archivos contra las plantillas (creación). Reporta primero, arregla con aprobación. Triggers: `audita el contenido`, `está la carpeta en orden`, `drift de carpetas`.

## Proyectos y Áreas — tu frente de ejecución, visible y al día

Ver `systems/proyectos-y-areas.md`. A demanda, más una detección diaria programada (project-learner, tras la nocturna del learning). Proyecto = se puede acabar (`pending|working|done`); área = responsabilidad continua con estándar (`active|archived`). El Learning System no toca projects/ ni areas/: la única vía de escritura es project-manager.

- **project-manager** — crea, actualiza, revisa y cierra proyectos y áreas, siempre con confirmación. En la revisión agrupa por área, contrasta con los Goals y señala estancados y áreas descuidadas. Triggers: `nuevo proyecto`, `nueva área`, `cómo van mis proyectos`, `actualiza el proyecto`, `cierra el proyecto`, `en qué estoy`.
- **project-learner** — detecta en el log del día proyectos nuevos, áreas que asoman y movimiento de los existentes; solo propone, y lo aprobado se aplica vía project-manager. Triggers: `propuestas de proyectos`, `qué proyectos has detectado`.
- **project-janitor** — audita projects/ y areas/ contra plantillas, mapa y logs: forma, registro y ciclo de vida (working estancados, pending eternos, done a medias, áreas descuidadas). Reporta primero; los cambios de estado pasan por project-manager. Triggers: `audita los proyectos`, `audita las áreas`, `están los proyectos en orden`, `drift de proyectos`.

## Pulidor — feedback sin sustituirte

Ver `systems/pulidor.md`. A demanda, en mitad de cualquier conversación.

- **pulidor** — compañero de pensamiento: pregunta qué tipo de pulido se necesita, saca puntos ciegos y tensiones, contrasta con los Goals, nunca escribe el producto final. Triggers: `pule esto`, `dame feedback`, `qué se me escapa`, `estoy atascado`, `segunda opinión`.

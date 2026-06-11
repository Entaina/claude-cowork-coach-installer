# Mapa de skills

Catálogo de lo que el coach sabe hacer, agrupado por sistema. **Consúltalo antes de procesar cualquier petición no trivial**: si hay skill para ello, se usa. Cada skill o sistema nuevo se registra aquí en el momento de crearse (vía skill-builder) — si el mapa no lo menciona, no existe.

## Learning System — cómo aprende el coach

Ver `systems/learning-system.md`. Una tarea programada nocturna; el usuario firma por la mañana.

- **episodic-learner** — compone el log del día leyendo las sesiones de Cowork y mantiene los Pendientes de ME.md. El único que escribe directo. Triggers: `genera el log de hoy`, `cierra el día`, `reconstruye el log`.
- **semantic-learner** — propone cambios a knowledge/ y a Quién soy/Goals de ME.md, con destino, cambio y fuente. No aplica nada. Triggers: `propuestas semánticas`, `qué has aprendido de mí`.
- **procedural-learner** — propone cambios a Preferencias/Reglas de ME.md y candidatas a skill cuando detecta patrones repetidos. No aplica nada. Triggers: `propuestas procedurales`, `qué deberías hacer distinto`.

## Taller — mantiene el AIOS fiable

Ver `systems/taller.md`. A demanda.

- **skill-builder** — crea y registra skills nuevas de forma consistente; única vía de creación. Triggers: `crea una skill`, `nueva skill`, `skill para`, `quiero capturar esto como skill`.
- **contenido-janitor** — audita mapa-contenido contra la carpeta real (navegación y formatos). Reporta primero, arregla con aprobación. Triggers: `audita el contenido`, `está la carpeta en orden`, `drift de carpetas`.
- **skills-janitor** — audita skills y sistemas contra mapa-skills y el esquema de skill-builder. Reporta primero, arregla con aprobación. Triggers: `audita las skills`, `están las skills en orden`, `skill drift`.

## Pulidor — feedback sin sustituirte

Ver `systems/pulidor.md`. A demanda, en mitad de cualquier conversación.

- **pulidor** — compañero de pensamiento: pregunta qué tipo de pulido se necesita, saca puntos ciegos y tensiones, contrasta con los Goals, nunca escribe el producto final. Triggers: `pule esto`, `dame feedback`, `qué se me escapa`, `estoy atascado`, `segunda opinión`.

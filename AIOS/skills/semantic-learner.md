---
name: semantic-learner
system: learning-system
status: Active
created: 2026-06-11
updated: 2026-06-11
triggers:
  - propuestas semánticas
  - qué has aprendido de mí
  - semantic learner
dependencies: []
description: |
  Lee el log del día y redacta propuestas de cambio para la memoria semántica y de trabajo — los archivos de knowledge/, los proyectos de projects/ (avances, decisiones, cambios de estado) y las secciones Quién soy y Goals de ME.md. Cada propuesta lleva destino, cambio concreto y fuente. No aplica nada: esa memoria solo cambia con la firma del usuario. Segundo paso de la tarea nocturna del Learning System, en paralelo con procedural-learner.
---
# semantic-learner

Destila hechos duraderos del registro del día. Propone; no escribe en la memoria.

## Cuándo usarla

- Cada noche, tras episodic-learner, dentro de la tarea programada del Learning System.
- A demanda, si el usuario quiere ver qué daría de sí el día antes de la pasada nocturna.

## Cuándo NO usarla

- Para actualizar un archivo de knowledge a petición directa del usuario en mitad de una sesión — eso es una edición normal con confirmación, no necesita learner.
- Para preferencias, reglas o skills: eso es territorio de procedural-learner.

## Workflow

1. Si el log de hoy no existe, ejecuta episodic-learner primero. No trabajes de memoria: el log es la única fuente.
2. Lee el log completo, con atención especial a las señales `novedoso` y `decidido`.
3. Contrasta cada hallazgo con lo que ya dice la memoria — `ME.md` (Quién soy, Goals), los archivos de `knowledge/` y los proyectos de `projects/`:
   - ¿Contradice algo escrito? → propuesta de corrección.
   - ¿Extiende algo escrito? → propuesta de ampliación.
   - ¿Estrena tema (un cliente, una persona)? → propuesta de archivo nuevo en `knowledge/` (o en `projects/` si es un proyecto, con la plantilla de proyecto).
   - ¿Avanza un proyecto (decisión, paso completado, cambio de estado pending/working/done)? → propuesta de actualización de su archivo en `projects/`.
4. Redacta cada propuesta en el bloque `## Propuestas` del log con la plantilla: destino, cambio concreto (el texto que se añadiría o modificaría, no una vaguedad), fuente (sesión y momento), estado `pendiente`.
5. No modifiques ningún archivo de destino. Tu output son propuestas.

## Qué produce

Propuestas semánticas al pie del log, listas para que el usuario las firme o descarte.

## Reglas

- Una propuesta = un cambio. No agrupes tres ideas en una propuesta.
- El cambio se redacta listo para aplicar: si el usuario dice "sí", se copia tal cual.
- Usa las palabras del usuario cuando existan en el log. No las reescribas.
- Sin señal, sin propuesta. Un día rutinario produce cero propuestas semánticas, y eso está bien — no rellenes.
- Nunca propongas sobre material que el usuario pidió no registrar.

## Casos límite

- **El log de hoy ya está consolidado** (`consolidado: sí`): no hay nada que hacer; dilo y para.
- **Señal ambigua** (no está claro si contradice o extiende): redacta la propuesta como pregunta — "el log sugiere X, pero ME.md dice Y, ¿cuál vale?" — mejor que adivinar.
- **Hallazgo enorme** (la entrevista inicial, un día de muchas decisiones): tope de 5-7 propuestas, las de más señal. El resto puede esperar a otro día; el usuario no va a firmar veinte cosas por la mañana.

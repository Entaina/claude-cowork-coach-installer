---
name: project-learner
system: proyectos
status: Active
created: 2026-06-11
updated: 2026-06-11
triggers:
  - propuestas de proyectos
  - qué proyectos has detectado
  - project learner
dependencies: []
description: |
  Lee el log del día y detecta movimiento de proyectos — proyectos nuevos que asoman en las conversaciones, avances y decisiones de los existentes, estados que ya no cuadran con la realidad. Todo lo convierte en propuestas (crear, actualizar, cambiar estado) que esperan la firma del usuario; las aprobadas se aplican vía project-manager. No aplica nada por su cuenta. Corre cada noche en la tarea programada del Sistema Proyectos, tras la nocturna del Learning System.
---
# project-learner

Detecta el movimiento de la cartera en el registro del día. Propone; quien escribe es project-manager, con firma.

## Cuándo usarla

- Cada noche, en la tarea programada del Sistema Proyectos (tras la nocturna del Learning System, porque lee su log).
- A demanda, si el usuario quiere saber qué movimiento de proyectos dio el día.

## Cuándo NO usarla

- Para gestionar proyectos en vivo durante una conversación: eso es project-manager.
- Para auditar forma, registro o ciclo de vida: eso es project-janitor.
- Para señales que no van de proyectos (hechos, preferencias): eso es el Learning System.

## Workflow

1. Si el log de hoy no existe, ejecuta episodic-learner primero. El log es la única fuente.
2. Lee el log completo y los archivos de `projects/`. Busca tres cosas:
   - **Proyecto nuevo**: algo con objetivo y trabajo real detrás que asoma en el día y no tiene archivo. → Propuesta de creación desde `AIOS/Templates/project-template.md`, con el status que corresponda (`pending` o `working`).
   - **Avance de existente**: decisión tomada, paso completado, persona nueva, cambio de rumbo que toca a un proyecto con archivo. → Propuesta de actualización (qué sección, qué texto).
   - **Estado que miente**: el log demuestra que un `pending` ya está en marcha, o que un `working` se dio por cerrado. → Propuesta de cambio de status, explícita.
3. Redacta cada propuesta en el bloque `## Propuestas` del log, tipo `proyectos`, con la plantilla: destino, cambio concreto listo para aplicar, fuente, estado `pendiente`.
4. No crees ni modifiques nada en `projects/`. Tu output son propuestas; las aprobadas se aplican vía project-manager.

## Qué produce

Propuestas de proyectos al pie del log, listas para la firma del usuario.

## Reglas

- Si cabe en un Pendiente de ME.md, no es un proyecto: no infles la cartera. Un proyecto necesita objetivo y siguiente paso propios.
- Una propuesta = un proyecto y un cambio. El cambio, redactado listo para aplicar.
- Los cambios de estado siempre como propuesta explícita, nunca implícitos dentro de otra.
- Sin movimiento, sin propuestas. Cero es un resultado válido.
- Usa las palabras del usuario cuando existan en el log.

## Casos límite

- **El mismo proyecto asoma varios días sin que el usuario apruebe crearlo**: re-presenta la propuesta (sigue `pendiente`), no la dupliques.
- **Movimiento ambiguo** (¿es proyecto o tarea suelta?): propónlo como pregunta, con la regla del Pendiente a la vista, y que decida el usuario.
- **Día con mucho movimiento**: tope de 5 propuestas, las de más señal.

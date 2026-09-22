---
name: procedural-learner
description: >-
  Lee el log del día y redacta propuestas para la memoria procedural — las
  secciones Preferencias y Reglas de ME.md, y skills nuevas cuando detecta
  patrones repetidos en los logs recientes. Cada propuesta lleva destino,
  cambio concreto y fuente. No aplica nada ni crea skills: las aprobadas pasan
  por skill-builder. Segundo paso de la tarea nocturna del Learning System, en
  paralelo con semantic-learner. Se activa con frases como: "propuestas
  procedurales", "qué deberías hacer distinto", "procedural learner".
metadata:
  system: learning-system
  status: active
  created: "2026-06-11"
  updated: "2026-06-11"
---
# procedural-learner

Aprende cómo trabajar con el usuario, no qué sabe de él. Propone; no escribe en la memoria.

## Cuándo usarla

- Cada noche, tras episodic-learner, dentro de la tarea programada del Learning System.
- A demanda, si el usuario pregunta qué debería cambiar en la forma de trabajar juntos.

## Cuándo NO usarla

- Para hechos sobre el usuario o su mundo: eso es territorio de semantic-learner.
- Para crear una skill ya aprobada: eso lo hace skill-builder. Esta skill solo detecta y propone.

## Workflow

1. Si el log de hoy no existe, ejecuta episodic-learner primero. El log es la única fuente.
2. Lee el log completo, con atención especial a las señales `preferencia/regla`.
3. Contrasta con las secciones Preferencias y Reglas de `ME.md`:
   - ¿Hábito o criterio nuevo que merece quedar escrito? → propuesta de adición.
   - ¿Una regla existente que lo de hoy contradice? → propuesta de corrección, citando ambas versiones.
4. Busca **patrones repetidos** en los logs de los últimos 7-14 días: la misma tarea, la misma estructura de petición, el mismo tipo de documento, varias veces. Si lo hay, propone una skill ("cada semana preparas X — ¿creo una skill para eso?"), con destino `skill-builder`.
5. Redacta cada propuesta en el bloque `## Propuestas` del log: destino, cambio concreto, fuente, estado `pendiente`.
6. No modifiques ME.md ni crees skills. Tu output son propuestas.

## Qué produce

Propuestas procedurales al pie del log: cambios a Preferencias/Reglas y candidatas a skill.

## Reglas

- Una preferencia se propone cuando hay señal repetida o explícita, no por una frase suelta dicha una vez con prisa.
- El cambio se redacta listo para aplicar, en el estilo de ME.md (frases cortas, imperativas).
- Una candidata a skill necesita al menos dos repeticiones reales en los logs. Con una, anótala mentalmente y espera.
- Sin señal, sin propuesta. Cero propuestas es un resultado válido.

## Casos límite

- **El log de hoy ya está consolidado**: no hay nada que hacer; dilo y para.
- **Preferencia que contradice una Regla de serie** (por ejemplo, "no me desafíes tanto"): proponla igualmente, citando la regla afectada — las reglas son del usuario, no del sistema. Que decida él.
- **Patrón detectado pero ya existe una skill parecida**: propone extender la existente, no crear una gemela. Cita la skill por nombre.

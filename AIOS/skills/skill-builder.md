---
name: skill-builder
system: taller
status: Active
created: 2026-06-11
updated: 2026-06-11
triggers:
  - crea una skill
  - nueva skill
  - hazme una skill
  - skill para
  - quiero capturar esto como skill
  - skill builder
dependencies: []
description: |
  Crea una skill nueva como archivo Markdown único en AIOS/skills/, con el frontmatter completo del esquema, y la registra en mapa-skills.md bajo su sistema. Ninguna skill se crea por otra vía — es la única puerta de entrada, para que las convenciones no se pierdan. Se dispara cuando el usuario aprueba una candidata del procedural-learner o pide capturar un workflow repetible como skill.
---
# skill-builder

Una skill para crear skills. Captura un workflow repetible en un archivo bien formado y bien registrado.

## Cuándo usarla

- El usuario aprueba una propuesta de skill del procedural-learner.
- El usuario pide directamente: "crea una skill para X", "quiero capturar esto como skill".

## Cuándo NO usarla

- Para editar una skill existente — eso es una edición normal con confirmación (y un repaso de skills-janitor después si cambió el frontmatter).
- Para reparar un mapa-skills roto — eso es trabajo de skills-janitor, no lo arregles a medio construir.

## Qué necesita antes de escribir

Confirma con el usuario, en una o dos preguntas como máximo (no lo interrogues):

- **Propósito** — qué hace la skill, en una frase.
- **Triggers** — las frases que el usuario diría de verdad para invocarla. Voz real, no nombres de comando abstractos.
- **Sistema** — a qué sistema existente pertenece. Si ninguno encaja, propón crear uno; nunca lo inventes sin preguntar.
- **Pasos** — el workflow concreto que la skill codifica.

Si algo falta, pregunta. No adivines.

## Workflow

1. **Lee primero las fuentes de verdad**: `ME.md`, `mapa-contenido.md`, `mapa-skills.md`. Comprueba que no existe ya una skill que haga lo pedido — si existe, propón extenderla en vez de crear una gemela.
2. **Elige nombre**: kebab-case, patrón verbo-sustantivo cuando se pueda (`preparar-reunion`, `revisar-semana`). El nombre del archivo y el campo `name` deben coincidir exactamente.
3. **Toma como molde una skill existente** del mismo sistema o de forma parecida — copia su orden de secciones y su voz, no empieces de cero.
4. **Escribe el archivo** en `AIOS/skills/{nombre}.md` con el esquema de frontmatter de `mapa-contenido.md`: name, system, status, created, updated, triggers, dependencies, description. La `description` es el campo que más trabaja: el coach la lee para decidir si disparar la skill. Vaga = skill muda.
5. **Cuerpo**: tagline tras el H1, Cuándo usarla, Cuándo NO usarla, Workflow numerado, Qué produce, Reglas. Casos límite si los hay. Voz tersa, sin tropos de IA.
6. **Registra** la skill en `mapa-skills.md`, bajo su sistema, con descripción de una línea y triggers. Si el sistema es nuevo, crea antes su nota en `AIOS/systems/` con la plantilla y añádela al mapa.
7. **Enséñasela al usuario** antes de darla por hecha — la description y los triggers son sensibles a su voz. "¿Guardo?".

## Qué produce

Una skill registrada y lista para dispararse, con su sistema al día.

## Reglas

- Un archivo, una skill. Nunca bundles ni subdirectorios.
- Una skill que no está en mapa-skills no existe. Registra siempre.
- El archivo de la skill es la fuente de verdad: los prompts de tareas programadas apuntan a la skill, nunca duplican su workflow.
- No repitas convenciones que ya viven en ME.md o en los mapas — refiérete a ellas.

## Casos límite

- **Ya existe una skill parecida**: propón extenderla. No crees gemelas.
- **La skill encaja en más de un sistema**: elige el más fuerte como `system`; menciona la relación en la description.
- **Skill experimental**: `status: Draft` hasta que esté lista. Las Draft se registran en el mapa marcadas como tal.

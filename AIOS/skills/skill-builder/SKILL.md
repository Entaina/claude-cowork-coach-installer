---
name: skill-builder
description: >-
  Crea una skill nueva como directorio con su SKILL.md en AIOS/skills/,
  siguiendo El formato del estándar Agent Skills, y la registra en
  mapa-skills.md bajo su sistema. Ninguna skill se crea por otra vía — es la
  única puerta de entrada, para que las convenciones no se pierdan. Se dispara
  cuando el usuario aprueba una candidata del procedural-learner o pide
  capturar un workflow repetible como skill. Se activa con frases como: "crea
  una skill", "nueva skill", "hazme una skill", "skill para", "quiero capturar
  esto como skill", "skill builder".
metadata:
  system: skills
  status: active
  created: "2026-06-11"
  updated: "2026-07-23"
---
# skill-builder

Una skill para crear skills. Captura un workflow repetible en un directorio bien formado y bien registrado.

## Cuándo usarla

- El usuario aprueba una propuesta de skill del procedural-learner.
- El usuario pide directamente: "crea una skill para X", "quiero capturar esto como skill".

## Cuándo NO usarla

- Para editar una skill existente — eso es una edición normal con confirmación (y un repaso de skills-janitor después si cambió el frontmatter).
- Para reparar un mapa-skills roto — eso es trabajo de skills-janitor, no lo arregles a medio construir.

## Qué necesita antes de escribir

Confirma con el usuario, en una o dos preguntas como máximo (no lo interrogues):

- **Propósito** — qué hace la skill, en una frase.
- **Frases de disparo** — las que el usuario diría de verdad para invocarla. Voz real, no nombres de comando abstractos. Van dentro de la `description`, al final.
- **Sistema** — a qué sistema existente pertenece (irá en `metadata.system`). Si ninguno encaja, propón crear uno; nunca lo inventes sin preguntar.
- **Pasos** — el workflow concreto que la skill codifica.

Si algo falta, pregunta. No adivines.

## Workflow

1. **Lee primero las fuentes de verdad**: `ME.md`, `mapa-contenido.md`, `mapa-skills.md` y la sección **El formato** de `AIOS/systems/skills.md`. Comprueba que no existe ya una skill que haga lo pedido — si existe, propón extenderla en vez de crear una gemela.
2. **Elige nombre**: kebab-case, patrón verbo-sustantivo cuando se pueda (`preparar-reunion`, `revisar-semana`). El nombre del directorio y el campo `name` deben coincidir exactamente; las reglas del nombre están en El formato.
3. **Toma como molde una skill existente** del mismo sistema o de forma parecida — copia su orden de secciones y su voz, no empieces de cero.
4. **Escribe la skill** en `AIOS/skills/{nombre}/SKILL.md` partiendo de `AIOS/Templates/skill-template.md` (léela, no la reconstruyas de memoria). La `description` es el campo que más trabaja: el coach la lee para decidir si disparar la skill, y lleva dentro las frases de disparo. Vaga = skill muda.
5. **Cuerpo**: tagline tras el H1, Cuándo usarla, Cuándo NO usarla, Workflow numerado, Qué produce, Reglas. Casos límite si los hay. Voz tersa, sin tropos de IA.
6. **Registra** la skill en `mapa-skills.md`, bajo su sistema, con descripción de una línea y sus frases de disparo. Si el sistema es nuevo, crea antes su nota en `AIOS/systems/` partiendo de `AIOS/Templates/system-template.md` y añádela al mapa.
7. **Enséñasela al usuario** antes de darla por hecha — la description es sensible a su voz. "¿Guardo?".

## Qué produce

Una skill registrada y lista para dispararse, con su sistema al día.

## Reglas

- Un directorio, una skill: el cuerpo vive en su `SKILL.md`. `scripts/`, `references/` y `assets/` se admiten solo cuando aportan (código auxiliar, material de consulta largo, plantillas propias) — nunca para trocear una skill simple.
- Una skill que no está en mapa-skills no existe. Registra siempre.
- El `SKILL.md` de la skill es la fuente de verdad: los prompts de tareas programadas apuntan a la skill, nunca duplican su workflow.
- No repitas convenciones que ya viven en ME.md o en los mapas — refiérete a ellas.

## Casos límite

- **Ya existe una skill parecida**: propón extenderla. No crees gemelas.
- **La skill encaja en más de un sistema**: elige el más fuerte como `metadata.system`; menciona la relación en la description.
- **Skill experimental**: `metadata.status: draft` hasta que esté lista. Las draft se registran en el mapa marcadas como tal.

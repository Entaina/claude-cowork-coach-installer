---
name: skills-janitor
system: skills
status: Active
created: 2026-06-11
updated: 2026-06-11
triggers:
  - skills janitor
  - audita las skills
  - revisa las skills
  - están las skills en orden
  - skill drift
dependencies: []
description: |
  Audita los archivos de AIOS/skills/ y AIOS/systems/ contra mapa-skills.md y contra el esquema definido por skill-builder. Caza drift en tres direcciones — lado archivo (frontmatter incompleto, name que no coincide con el nombre del archivo, system que apunta a una nota inexistente), lado registro (skill sin entrada en el mapa, entrada bajo el sistema equivocado, skill retirada aún listada) y lado huérfano (entradas del mapa que apuntan a archivos borrados). Reporta primero, arregla con aprobación, nunca edita en silencio.
---
# skills-janitor

Escanea las skills. Compara con el mapa y el esquema. Reporta el drift. Arregla con aprobación.

Los archivos de `AIOS/skills/` son la fuente de verdad. `mapa-skills.md` es el registro — se reconcilia *hacia* los archivos, nunca al revés. El esquema de skill-builder es la norma: toda skill debe validar contra él.

## Cuándo usarla

- Después de crear, renombrar o retirar varias skills.
- Como pasada de higiene periódica cuando el mapa empiece a oler a desactualizado.
- Si solo una skill cambió, arregla el mapa a mano — el janitor renta cuando hay varias que comprobar.

## Cuándo NO usarla

- Para crear skills: eso es skill-builder.
- Para auditar carpetas o plantillas: eso es contenido-janitor.

## Workflow

### 1. Escanear los archivos

Lee cada `.md` de `AIOS/skills/` y `AIOS/systems/`. Extrae el frontmatter. Anota cualquier archivo con YAML roto.

### 2. Comprobaciones lado archivo

Por cada skill:

- **El nombre del archivo coincide con `name:`.** Si no, hay un renombrado a medias.
- **`system:` apunta a una nota que existe** en `AIOS/systems/`. Sin sistemas fantasma.
- **`description:` no está vacía.** Es el campo que decide si la skill se dispara; vacía = skill muda.
- **`status:` es uno de** `Active`, `Draft`, `Retired`.
- **`triggers:` tiene al menos una frase.**

Por cada sistema: su campo `skills:` lista solo skills cuyos archivos existen, y toda skill que declare ese sistema aparece en la lista.

### 3. Comprobaciones lado registro (skill ↔ mapa)

Lee `mapa-skills.md`. Por cada skill Active:

- Tiene su entrada bajo la sección de su sistema, con descripción de una línea y triggers.
- La sección del sistema apunta a la nota correcta de `systems/`.
- Las Retired no aparecen como activas; las Draft van marcadas.

### 4. Huérfanos

Toda skill o sistema mencionado en el mapa debe tener archivo. Lo que apunte a archivos borrados se marca para retirar del mapa.

### 5. Reporte

Salida en chat, sin escribir archivos:

```
# Informe skills-janitor — AAAA-MM-DD
Skills: N (Active A, Draft D, Retired R) · Sistemas: M

## Lado archivo
- skill.md — {problema concreto} (o "sin problemas")
## Lado registro
- skill — {falta en el mapa / sección equivocada / ...} (o "sin problemas")
## Huérfanos
- mapa-skills menciona {x} pero no existe (o "ninguno")
## Salud
{“En orden” o “N problemas en M skills.”}
```

Espera la aprobación del usuario antes de tocar nada.

### 6. Arreglo (con aprobación)

- **Arreglos seguros**: añadir entradas que faltan al mapa, mover entradas a su sección correcta, retirar huérfanos del mapa.
- **Se reporta pero NO se auto-arregla**: discrepancias nombre-archivo (es un renombrado, decisión del usuario), descriptions vacías (necesitan criterio humano), YAML roto en una skill (enseña el diff propuesto antes).

## Qué produce

Un informe de drift y, con visto bueno, el mapa y los archivos vueltos a cuadrar.

## Reglas

- Nunca edites una skill para contentar al mapa: los archivos mandan.
- Lee primero, escribe después. El informe siempre precede al cambio.
- Sé específico: nombra la skill, el campo y el problema. "Las skills están desincronizadas" no sirve; "pulidor.md declara system: feedback pero no existe systems/feedback.md" sí.

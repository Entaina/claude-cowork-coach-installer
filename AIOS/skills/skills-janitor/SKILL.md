---
name: skills-janitor
description: >-
  Audita las skills de AIOS/skills/ y los sistemas de AIOS/systems/ contra
  mapa-skills.md y contra El formato (el contrato del estándar Agent Skills
  recogido en systems/skills.md). Caza drift en tres direcciones — lado skill
  (SKILL.md ausente o con YAML roto, name que no coincide con el directorio,
  campos del formato viejo en el nivel superior, metadata.system que apunta a
  una nota inexistente), lado registro (skill sin entrada en el mapa, entrada
  bajo el sistema equivocado, skill retirada aún listada) y lado huérfano
  (entradas del mapa que apuntan a skills borradas). Reporta primero, arregla
  con aprobación, nunca edita en silencio. Se activa con frases como: "skills
  janitor", "audita las skills", "revisa las skills", "están las skills en
  orden", "skill drift".
metadata:
  system: skills
  status: active
  created: "2026-06-11"
  updated: "2026-07-23"
---
# skills-janitor

Escanea las skills. Compara con el mapa y El formato. Reporta el drift. Arregla con aprobación.

Los `SKILL.md` de `AIOS/skills/` son la fuente de verdad. `mapa-skills.md` es el registro — se reconcilia *hacia* los archivos, nunca al revés. La norma es **El formato** (`AIOS/systems/skills.md`): toda skill debe validar contra él.

## Cuándo usarla

- Después de crear, renombrar o retirar varias skills.
- Como pasada de higiene periódica cuando el mapa empiece a oler a desactualizado.
- Si solo una skill cambió, arregla el mapa a mano — el janitor renta cuando hay varias que comprobar.

## Cuándo NO usarla

- Para crear skills: eso es skill-builder.
- Para auditar carpetas o plantillas: eso es contenido-janitor.

## Workflow

### 1. Escanear los archivos

Lee cada `SKILL.md` de `AIOS/skills/*/` y cada `.md` de `AIOS/systems/`. Extrae el frontmatter. Anota cualquier archivo con YAML roto, todo directorio de `AIOS/skills/` sin `SKILL.md` dentro, y todo `.md` suelto en `AIOS/skills/` — resto del formato viejo, pendiente de migrar.

### 2. Comprobaciones lado skill

Por cada skill, contra El formato:

- **El nombre del directorio coincide con `name:`** (y cumple sus reglas: minúsculas, números y guiones). Si no, hay un renombrado a medias.
- **`description:` no está vacía, cabe en su límite y lleva las frases de disparo.** Es el campo que decide si la skill se dispara; vacía = skill muda.
- **Nada del formato viejo en el nivel superior**: `triggers`, `status`, `system`, `dependencies`, `created` o `updated` sueltos son drift — los campos del coach viven en `metadata`, y las frases de disparo, dentro de la `description`.
- **`metadata.system` apunta a una nota que existe** en `AIOS/systems/`. Sin sistemas fantasma.
- **`metadata.status` es uno de** `active`, `draft`, `retired`.

Por cada sistema: su campo `skills:` lista solo skills cuyos directorios existen, y toda skill que declare ese sistema en `metadata.system` aparece en la lista.

### 3. Comprobaciones lado registro (skill ↔ mapa)

Lee `mapa-skills.md`. Por cada skill activa:

- Tiene su entrada bajo la sección de su sistema, con descripción de una línea y sus frases de disparo.
- La sección del sistema apunta a la nota correcta de `systems/`.
- Las retired no aparecen como activas; las draft van marcadas.

### 4. Huérfanos

Toda skill o sistema mencionado en el mapa debe tener su directorio o nota. Lo que apunte a skills borradas se marca para retirar del mapa.

### 5. Reporte

Salida en chat, sin escribir archivos:

```
# Informe skills-janitor — AAAA-MM-DD
Skills: N (active A, draft D, retired R) · Sistemas: M

## Lado skill
- {skill}/SKILL.md — {problema concreto} (o "sin problemas")
## Lado registro
- {skill} — {falta en el mapa / sección equivocada / ...} (o "sin problemas")
## Huérfanos
- mapa-skills menciona {x} pero no existe (o "ninguno")
## Salud
{“En orden” o “N problemas en M skills.”}
```

Espera la aprobación del usuario antes de tocar nada.

### 6. Arreglo (con aprobación)

- **Arreglos seguros**: añadir entradas que faltan al mapa, mover entradas a su sección correcta, retirar huérfanos del mapa.
- **Se reporta pero NO se auto-arregla**: discrepancias nombre-directorio (es un renombrado, decisión del usuario), descriptions vacías (necesitan criterio humano), YAML roto o campos del formato viejo en una skill (enseña el diff propuesto antes).

## Qué produce

Un informe de drift y, con visto bueno, el mapa y los archivos vueltos a cuadrar.

## Reglas

- Nunca edites una skill para contentar al mapa: los archivos mandan.
- Lee primero, escribe después. El informe siempre precede al cambio.
- Sé específico: nombra la skill, el campo y el problema. "Las skills están desincronizadas" no sirve; "pulidor/SKILL.md declara metadata.system: feedback pero no existe systems/feedback.md" sí.

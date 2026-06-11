# Mapa de contenido

Manual del coach para moverse por esta carpeta y crear archivos en ella. Tiene dos mitades: **Navegación** (qué hay y cuándo leerlo) y **Creación** (cómo se crean archivos bien formados).

## Navegación

- `CLAUDE.md` — wrapper de arranque. No se toca.
- `ME.md` — briefing del usuario: quién es, goals, preferencias, reglas, pendientes. Se lee en cada arranque.
- `knowledge/` — memoria semántica: el mundo del usuario (clientes, proyectos, equipo...). Archivos sueltos, sin subcarpetas; la estructura se gana cuando duele no tenerla, no antes. Se lee según el tema de la sesión.
- `episodic/logs/` — memoria episódica: un log por día (`AAAA-MM-DD.md`), compuesto por el episodic-learner. Los logs de días anteriores son historia: no se reescriben (solo su frontmatter, al consolidar).
- `AIOS/` — memoria procedural: este mapa, `mapa-skills.md`, `skills/` (una skill por archivo) y `systems/` (una nota por sistema).

### Reglas de escritura

- El único que escribe sin permiso es el **episodic-learner**, y solo en sus dos destinos: el log del día y la sección Pendientes de `ME.md`.
- `knowledge/`, `AIOS/` y el resto de `ME.md` cambian únicamente con confirmación explícita del usuario.
- Skills y sistemas se crean solo vía **skill-builder**.

### Mantenimiento

Cada archivo nuevo en `knowledge/` se registra en este mapa (sección Navegación) al crearse. Si el mapa no lo menciona, no existe. El drift lo caza **contenido-janitor**.

## Creación

- Todo archivo nuevo parte de una plantilla de las de abajo. Lee la plantilla de este archivo cada vez — no la reconstruyas de memoria.
- Lista el árbol antes de colocar un archivo nuevo: que no caiga en la capa equivocada.
- Fechas siempre completas y en Europe/Madrid: `AAAA-MM-DD` en frontmatter, `AAAA-MM-DD HH:MM` en señales.
- Estados de una propuesta: `pendiente` → `incorporada` o `descartada`. Estado de un log: `consolidado: pendiente` → `consolidado: sí` (lo marca el Learning System al resolver sus propuestas).
- Usa las palabras del usuario cuando existan. No las reescribas.

## Plantillas

### Archivo de knowledge/

```
---
created: {AAAA-MM-DD}
updated: {AAAA-MM-DD}
---
# {Título}

{Contenido en secciones ##.}
```

### Log diario (`episodic/logs/AAAA-MM-DD.md`)

```
---
date: {AAAA-MM-DD}
consolidado: pendiente
---
# Log {AAAA-MM-DD}

## Qué pasó
{Narrativa breve con la forma del día — no una lista de actividades.}

## Señales
### {AAAA-MM-DD HH:MM} - {novedoso|decidido|no resuelto|preferencia/regla}
{Una frase declarativa. Una idea por bloque.}

## Propuestas
### Propuesta {N} — {semántica|procedural}
- Destino: {archivo o sección}
- Cambio: {el texto concreto que se añadiría o modificaría, listo para aplicar}
- Fuente: {de qué sesión/momento sale}
- Estado: pendiente
```

### Skill (`AIOS/skills/*.md`)

```
---
name: {nombre-de-la-skill}
system: {sistema al que pertenece}
status: Active
created: {AAAA-MM-DD}
updated: {AAAA-MM-DD}
triggers:
  - {frase que la dispara}
  - {otra frase}
dependencies: []
description: |
  {Qué hace la skill y cuándo usarla. Específica — el coach la lee para decidir
  si dispararla. Sin dos puntos, que rompen el YAML.}
---
# {nombre-de-la-skill}

{Tagline de una línea.}

## Cuándo usarla
## Cuándo NO usarla
## Workflow
## Qué produce
## Reglas
```

Campos: `status` es `Active`, `Draft` o `Retired`. `description` es el campo que más trabaja — vaga = skill muda. `triggers` con la voz real del usuario, no nombres de comando.

### Sistema (`AIOS/systems/*.md`)

```
---
name: {nombre-del-sistema}
skills: {skills que lo componen, separadas por comas}
created: {AAAA-MM-DD}
---
# {Nombre del Sistema}

{Qué resuelve y por qué existe, en dos o tres frases.}

## Skills
- {skill}: {una línea sobre su papel en el sistema}

## Orquestación
{Cómo y cuándo se ejecutan: orden, paralelo, tarea programada, triggers. Si hay tarea programada, su prompt es fino y apunta a las skills — nunca duplica sus workflows.}

## Cuándo NO usarlo
## Ejemplos correctos
## Ejemplos incorrectos
```

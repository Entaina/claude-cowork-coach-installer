# Mapa de contenido

Manual del coach para moverse por esta carpeta y crear archivos en ella. Tiene dos mitades: **Navegación** (qué hay y cuándo leerlo) y **Creación** (cómo se crean archivos bien formados).

## Navegación

- `CLAUDE.md` — wrapper de arranque. No se toca.
- `ME.md` — briefing del usuario: quién es, goals, preferencias, reglas, pendientes. Se lee en cada arranque.
- `projects/` — memoria de trabajo: un archivo por proyecto (resultado concreto con final), con `status: pending | working | done`. Los `working` son el frente abierto del usuario: consúltalos al planificar o cuando el tema lo pida.
- `areas/` — memoria de trabajo: un archivo por área de responsabilidad continua (no se termina; tiene un estándar que mantener), con `status: active | archived`. El test proyecto/área: "¿puede acabarse?". Ambas carpetas se gestionan vía project-manager (Sistema Proyectos y Áreas).
- `knowledge/` — memoria semántica: el mundo del usuario (clientes, personas, equipo...). Archivos sueltos, sin subcarpetas; la estructura se gana cuando duele no tenerla, no antes. Se lee según el tema de la sesión.
- `episodic/logs/` — memoria episódica: un log por día (`AAAA-MM-DD.md`), compuesto por el episodic-learner. Los logs de días anteriores son historia: no se reescriben (solo su frontmatter, al consolidar).
- `AIOS/` — memoria procedural: este mapa, `mapa-skills.md`, `Templates/` (plantillas), `skills/` (una skill por archivo) y `systems/` (una nota por sistema).

### Reglas de escritura

- El único que escribe sin permiso es el **episodic-learner**, y solo en sus dos destinos: el log del día y la sección Pendientes de `ME.md`.
- `projects/`, `areas/`, `knowledge/`, `AIOS/` y el resto de `ME.md` cambian únicamente con confirmación explícita del usuario.
- Skills y sistemas se crean solo vía **skill-builder**.

### Mantenimiento

Cada archivo nuevo en `projects/`, `areas/` o `knowledge/` se registra en este mapa (sección Navegación) al crearse. Si el mapa no lo menciona, no existe. El drift lo caza **contenido-janitor**.

## Creación

- **Todo archivo nuevo parte de una plantilla de `AIOS/Templates/`. Lee el archivo de la plantilla cada vez — no la reconstruyas de memoria.** Las plantillas cambian; el archivo es la fuente de verdad.
- Lista el árbol antes de colocar un archivo nuevo: que no caiga en la capa equivocada.
- Fechas siempre completas y en Europe/Madrid: `AAAA-MM-DD` en frontmatter, `AAAA-MM-DD HH:MM` en señales.
- Usa las palabras del usuario cuando existan. No las reescribas.

### Plantillas disponibles

| Tipo de archivo | Plantilla | Destino |
| --- | --- | --- |
| Cualquier nota de knowledge (fallback universal) | `AIOS/Templates/base-template.md` | `knowledge/` |
| Proyecto | `AIOS/Templates/project-template.md` | `projects/` |
| Área de responsabilidad | `AIOS/Templates/area-template.md` | `areas/` |
| Persona (jefe, equipo, cliente) | `AIOS/Templates/persona-template.md` | `knowledge/` |
| Log diario | `AIOS/Templates/log-template.md` | `episodic/logs/` |
| Skill | `AIOS/Templates/skill-template.md` | `AIOS/skills/` (solo vía skill-builder) |
| Sistema | `AIOS/Templates/system-template.md` | `AIOS/systems/` (solo vía skill-builder) |

Cuando ninguna especializada encaje, usa `base-template.md`.

### Estados

- Propuesta: `pendiente` → `incorporada` o `descartada`.
- Log: `consolidado: pendiente` → `consolidado: sí` (lo marca el Learning System al resolver sus propuestas).
- Proyecto: `status: pending | working | done`.
- Área: `status: active | archived`.
- Skill: `status: Active | Draft | Retired`. La `description` es el campo que más trabaja — vaga = skill muda. Los `triggers`, con la voz real del usuario.

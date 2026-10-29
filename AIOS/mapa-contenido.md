# Mapa de contenido

Manual del coach para moverse por esta carpeta y crear archivos en ella. Tiene dos mitades: **Navegación** (qué hay y cuándo leerlo) y **Creación** (cómo se crean archivos bien formados).

## Navegación

- `AGENTS.md` y `CLAUDE.md` — instrucciones completas de arranque, idénticas y sincronizadas. Cada app usa el nombre que reconoce; al modificar el arranque, actualiza ambos sin perder personalizaciones.
- `AIOS/entornos-locales.md` — acceso al historial y programación en Cowork, Claude Code, GPT local y Amazon Quick; léelo antes de usar esas capacidades.
- `AIOS/amazon-quick.md` — preparación de la carpeta, agente Coach, historial, rutina y límites de la app de escritorio de Quick. La versión web queda fuera.
- `AIOS/claude-code.md` — configuración y límites de Code; `AIOS/integrations/claude_code.py` genera wrappers locales, registra sesiones del proyecto y filtra su historial.
- `.claude/skills/` — wrappers nativos generados solo al configurar Code; `.claude/settings.json` conserva sus hooks y ajustes. `.claude/coach-local/` es estado técnico local, excluido de Git; el hook autorizado registra metadatos, no escribe memoria personal.
- `ME.md` — briefing del usuario: quién es, goals, preferencias, reglas, pendientes. Se lee en cada arranque.
- `projects/` — memoria de trabajo: un archivo por proyecto (resultado concreto con final), con `status: pending | working | done`. Los `working` son el frente abierto del usuario: consúltalos al planificar o cuando el tema lo pida.
- `areas/` — memoria de trabajo: un archivo por área de responsabilidad continua (no se termina; tiene un estándar que mantener), con `status: active | archived`. El test proyecto/área: "¿puede acabarse?". Ambas carpetas se gestionan vía project-manager (Sistema Proyectos y Áreas).
- `knowledge/` — memoria semántica: el mundo del usuario (clientes, personas, equipo...). Archivos sueltos, sin subcarpetas; la estructura se gana cuando duele no tenerla, no antes. Se lee según el tema de la sesión.
- `pokm/` — el pOKM, si el usuario lo activó (`AIOS/systems/pokm.md`): `mapa.md` (el mapa de sus documentos: fuentes, carpetas por nivel, lo que queda fuera), `indices/` (un `index.md` por carpeta de nivel «índice») y `.estado/` (alcance y foto, gestionados por `AIOS/integrations/pokm.py`). Es un dato derivado de sus carpetas: dice dónde buscar, no lo que hay, y nunca copia su contenido. Ante un dato de su trabajo (una cifra, una fecha, una decisión) que no esté en tu memoria, búscalo con el mapa; si no aparece en un índice, abre los documentos de las carpetas de nivel «mapa» que encajen antes de decir que no existe. Para leer un Word, Excel o PowerPoint de sus carpetas, `python3 AIOS/integrations/pokm.py texto "<ruta>"`, como orden sola (sin `cd`, tuberías ni bucles: así la cubre su permiso en Claude Code); los PDF, con el lector de la app. Lo que marca como fuera no se abre aunque la respuesta esté ahí: primero se pregunta.
- `episodic/logs/` — memoria episódica: un log por día (`AAAA-MM-DD.md`), compuesto por el episodic-learner. Los logs de días anteriores son historia: no se reescriben, salvo sus estados de consolidación/propuestas al resolverlas. A petición explícita del usuario, episodic-learner puede completar el día solicitado conservando lo existente y los estados de las propuestas.
- `AIOS/` — memoria procedural: este mapa, `mapa-skills.md`, `Templates/` (plantillas), `skills/` (un directorio por skill, con su `SKILL.md` dentro), `systems/` (una nota por sistema) y `VERSION.md` (versión instalada del coach; la mantiene la actualización, no se edita a mano).

### Reglas de escritura

- El único que escribe sin permiso es el **episodic-learner**, y solo en sus dos destinos: el log del día (o el día histórico solicitado explícitamente) y la sección Pendientes de `ME.md`. Excepción: con el pOKM activo, su mantenimiento diario escribe solo en `pokm/` y en la sección `## pOKM` del log del día, dentro del alcance que decidió el usuario.
- `projects/`, `areas/`, `knowledge/`, `AIOS/` y el resto de `ME.md` cambian únicamente con confirmación explícita del usuario.
- Skills y sistemas se crean solo vía **skill-builder**.

### Mantenimiento

Cada archivo nuevo en `projects/`, `areas/` o `knowledge/` se registra en este mapa (sección Navegación) al crearse. Si el mapa no lo menciona, no existe. El drift lo caza **contenido-janitor**.

## Creación

- **Todo archivo nuevo parte de una plantilla de `AIOS/Templates/`. Lee el archivo de la plantilla cada vez — no la reconstruyas de memoria.** Las plantillas cambian; el archivo es la fuente de verdad.
- Lista el árbol antes de colocar un archivo nuevo: que no caiga en la capa equivocada.
- Fechas siempre completas y en la zona horaria del usuario (línea «Zona horaria» de `ME.md`; `Europe/Madrid` si falta): `AAAA-MM-DD` en frontmatter, `AAAA-MM-DD HH:MM` en señales.
- Usa las palabras del usuario cuando existan. No las reescribas.

### Plantillas disponibles

| Tipo de archivo | Plantilla | Destino |
| --- | --- | --- |
| Cualquier nota de knowledge (fallback universal) | `AIOS/Templates/base-template.md` | `knowledge/` |
| Proyecto | `AIOS/Templates/project-template.md` | `projects/` |
| Área de responsabilidad | `AIOS/Templates/area-template.md` | `areas/` |
| Persona (jefe, equipo, cliente) | `AIOS/Templates/persona-template.md` | `knowledge/` |
| Log diario | `AIOS/Templates/log-template.md` | `episodic/logs/` |
| Skill | `AIOS/Templates/skill-template.md` | `AIOS/skills/{nombre}/SKILL.md` (solo vía skill-builder) |
| Sistema | `AIOS/Templates/system-template.md` | `AIOS/systems/` (solo vía skill-builder) |

Cuando ninguna especializada encaje, usa `base-template.md`.

### Estados

- Propuesta: `pendiente` → `incorporada` o `descartada`.
- Log: `consolidado: pendiente` → `consolidado: sí` (lo marca el Learning System al resolver sus propuestas).
- Proyecto: `status: pending | working | done`.
- Área: `status: active | archived`.
- Skill: `metadata.status: active | draft | retired`. La `description` es el campo que más trabaja — vaga = skill muda — y lleva dentro las frases de disparo, con la voz real del usuario.

---
name: skills
skills: skill-builder, skills-janitor, skill-installer
created: 2026-06-11
---
# Sistema Skills

Gestiona las capacidades del coach: las skills se crean por una sola vía, el catálogo nunca miente y, cuando hace falta, se proyectan nativas al agente anfitrión. Sin este sistema, las skills nacen sin registrar (y no se disparan) o el mapa acumula entradas muertas — y la confianza en el coach se erosiona.

## Skills

- **skill-builder**: crea y registra skills nuevas de forma consistente. La única vía de creación.
- **skills-janitor**: audita `AIOS/skills/` y `AIOS/systems/` contra `mapa-skills.md` y **El formato** (más abajo). Reporta primero, arregla con aprobación.
- **skill-installer**: proyecta el `SKILL.md` canónico de una skill de `AIOS/skills/` al agente anfitrión (Cowork, Claude Code…) como skill nativa que el host descubre y dispara solo, con un wrapper delgado que apunta al canónico. Nunca duplica el workflow; el canónico manda y el wrapper es desechable.

## El formato

Las skills siguen el estándar [Agent Skills](https://agentskills.io/specification); ante la duda, manda la especificación. El contrato:

- Una skill = un directorio `AIOS/skills/<name>/` con su `SKILL.md` dentro. Opcionales: `scripts/`, `references/` y `assets/`, solo cuando aporten.
- `name`: minúsculas, números y guiones (sin guion inicial ni final, sin `--`), máximo 64 caracteres, idéntico al nombre del directorio.
- `description`: 1-1024 caracteres, en bloque `>-`. Dice qué hace, cuándo usarla, y lleva dentro las frases de disparo ("Se activa con frases como: …"). Es el campo que más trabaja: vaga = skill muda.
- `metadata` (todo texto — nada de listas ni fechas sin comillas): `system`, `status` (`active | draft | retired`), `created` y `updated` (`"AAAA-MM-DD"`), y `dependencies` solo si hay, separadas por comas.
- Nada más en el nivel superior del frontmatter: `triggers`, `status`, `system` o fechas sueltas son formato viejo — drift que skills-janitor caza.
- El cuerpo es libre; por debajo de 500 líneas, y lo largo se saca a `references/`.

## Orquestación

A demanda, sin tareas programadas:

- **skill-builder** se dispara al aprobar una candidata del procedural-learner o cuando el usuario pide una skill.
- **skills-janitor** se dispara cuando el usuario lo pide, tras una tanda de cambios en skills o sistemas, o cuando el coach detecta un desfase.
- **skill-installer** se dispara cuando el usuario quiere hacer nativa una skill en el agente donde trabaja ("instala esta skill", "instala todas"), o para refrescar un wrapper tras editar su canónico.

**El hand-off**: skill-builder enseña la skill antes de darla por hecha ("¿guardo?"). El janitor reporta, espera aprobación y entonces edita — sin reescrituras silenciosas. Los archivos de skills son la fuente de verdad; el mapa se reconcilia hacia ellos, nunca al revés.

## Cuándo NO usarlo

- Para editar el contenido de una skill existente: eso es una edición normal con confirmación (y una pasada de skills-janitor después si cambió el frontmatter).
- Como sustituto de hacer las cosas bien a la primera: el janitor limpia drift, no lo previene.

## Ejemplos correctos

- *"Crea una skill para preparar mis reuniones de los lunes."* skill-builder confirma propósito y frases de disparo, toma una skill existente como molde, crea el directorio con su SKILL.md desde la plantilla, lo registra en mapa-skills y enseña el resultado.
- *"¿Están las skills en orden?"* skills-janitor encuentra una skill con campos del formato viejo en el nivel superior y una entrada del mapa apuntando a una skill borrada; reporta separando arreglo seguro de decisión del usuario, y arregla lo aprobado.

## Ejemplos incorrectos

- *Crear una skill montando a mano un directorio en AIOS/skills/ sin pasar por skill-builder.* Así nacen las skills sin registrar que luego no se disparan.
- *El janitor edita una skill para que cuadre con el mapa.* Al revés siempre: los archivos mandan.

---
name: skills
skills: skill-builder, skills-janitor, skill-installer
created: 2026-06-11
---
# Sistema Skills

Gestiona las capacidades del coach: las skills se crean por una sola vía, el catálogo nunca miente y, cuando hace falta, se proyectan nativas al agente anfitrión. Sin este sistema, las skills nacen sin registrar (y no se disparan) o el mapa acumula entradas muertas — y la confianza en el coach se erosiona.

## Skills

- **skill-builder**: crea y registra skills nuevas de forma consistente. La única vía de creación.
- **skills-janitor**: audita `AIOS/skills/` y `AIOS/systems/` contra `mapa-skills.md` y el esquema de skill-builder. Reporta primero, arregla con aprobación.
- **skill-installer**: proyecta una skill canónica de `AIOS/skills/` al agente anfitrión (Cowork, Claude Code…) como skill nativa que el host descubre y dispara solo, con un wrapper delgado que apunta al canónico. Nunca duplica el workflow; el canónico manda y el wrapper es desechable.

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

- *"Crea una skill para preparar mis reuniones de los lunes."* skill-builder confirma propósito y triggers, toma una skill existente como molde, escribe el archivo desde la plantilla, lo registra en mapa-skills y enseña el resultado.
- *"¿Están las skills en orden?"* skills-janitor encuentra una skill con `system:` fantasma y una entrada del mapa apuntando a un archivo borrado; reporta separando arreglo seguro de decisión del usuario, y arregla lo aprobado.

## Ejemplos incorrectos

- *Crear una skill editando directamente un archivo en AIOS/skills/ sin pasar por skill-builder.* Así nacen las skills sin registrar que luego no se disparan.
- *El janitor edita una skill para que cuadre con el mapa.* Al revés siempre: los archivos mandan.

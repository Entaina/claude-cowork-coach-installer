---
name: taller
skills: skill-builder, contenido-janitor, skills-janitor
created: 2026-06-11
---
# Sistema Taller

Mantiene el AIOS fiable. Un cambio aquí, un archivo allá, y ningún desfase rompe nada de inmediato — pero es muerte por mil cortes: poco a poco los mapas mienten, las skills no se disparan y la confianza en el coach se erosiona. El Taller lo evita con una puerta de entrada única para crear skills y dos auditores que cazan el drift que nadie introdujo a propósito.

## Skills

- **skill-builder** — crea y registra skills nuevas de forma consistente. La única vía de creación.
- **contenido-janitor** — audita `mapa-contenido.md` contra la carpeta real: navegación (qué existe vs. qué documenta) y creación (qué archivos siguen las plantillas).
- **skills-janitor** — audita `AIOS/skills/` y `AIOS/systems/` contra `mapa-skills.md` y el esquema de skill-builder.

## Orquestación

A demanda, sin tareas programadas:

- **skill-builder** se dispara al aprobar una candidata del procedural-learner o cuando el usuario pide una skill.
- **Los janitors** se disparan cuando el usuario lo pide ("¿está todo en orden?"), tras una tanda de cambios, o cuando el coach detecta un desfase. Son state-driven: se corren periódicamente y cuentan qué derivó.

**El hand-off**: todo janitor reporta primero, espera aprobación y entonces edita. Sin reescrituras silenciosas. skill-builder enseña la skill antes de darla por hecha.

## Cuándo NO usarlo

- Como sustituto de hacer las cosas bien a la primera: los janitors limpian drift, no lo previenen.
- Si el usuario no tiene unos minutos para revisar el informe: el janitor sin aprobación no arregla nada — mejor volver cuando los haya.

## Ejemplos correctos

- *"Crea una skill para preparar mis reuniones de los lunes."* skill-builder confirma propósito y triggers, toma una skill existente como molde, escribe el archivo, lo registra en mapa-skills y enseña el resultado.
- *"¿Está todo en orden?"* Los dos janitors corren, encuentran un archivo de knowledge sin registrar y una skill con `system:` fantasma, lo reportan separando arreglo seguro de decisión del usuario, y arreglan lo aprobado.

## Ejemplos incorrectos

- *Crear una skill editando directamente un archivo en AIOS/skills/ sin pasar por skill-builder.* Así nacen las skills sin registrar que luego no se disparan.
- *Aprobar el informe del janitor sin leerlo.* El usuario sigue al mando; si un arreglo parece mal, se dice.
- *Usar un janitor para "mejorar" contenido.* Los janitors cuadran estructura; el contenido es del usuario.

---
name: contenido
skills: contenido-janitor
created: 2026-06-11
---
# Sistema Contenido

Mantiene fiable el mapa del territorio: lo que `mapa-contenido.md` dice y lo que hay en la carpeta cuadran siempre, y los archivos siguen las plantillas de `AIOS/Templates/`. Un mapa que miente es peor que no tener mapa — el coach lee cosas que no existen y se pierde las que sí.

## Skills

- **contenido-janitor**: audita `mapa-contenido.md` contra la carpeta real (navegación) y los archivos contra las plantillas (creación). Reporta primero, arregla con aprobación.

## Orquestación

A demanda, sin tareas programadas. Se dispara cuando el usuario lo pide ("¿está la carpeta en orden?"), tras crear o reorganizar varios archivos, o cuando el coach detecta un desfase entre el mapa y la realidad.

**El hand-off**: reporta primero, espera aprobación y entonces edita. La carpeta real es la fuente de verdad para la navegación; las plantillas son la norma para la creación. `projects/` y `areas/` quedan fuera: tienen su propio auditor (project-janitor, Sistema Proyectos y Áreas).

## Cuándo NO usarlo

- Para auditar skills, sistemas o proyectos: skills-janitor y project-janitor.
- Para "mejorar" contenido: el janitor cuadra estructura; el contenido es del usuario.

## Ejemplos correctos

- *"¿Está la carpeta en orden?"* contenido-janitor encuentra dos archivos de knowledge sin registrar en el mapa y un log sin estado de consolidación; reporta, y con visto bueno registra los archivos y completa el frontmatter.

## Ejemplos incorrectos

- *El janitor borra un archivo "porque no está en el mapa".* Jamás: lo que existe manda; el mapa se actualiza para reflejarlo.
- *Aprobar el informe sin leerlo.* El usuario sigue al mando del vault.

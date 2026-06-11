---
name: project-janitor
system: proyectos
status: Active
created: 2026-06-11
updated: 2026-06-11
triggers:
  - project janitor
  - audita los proyectos
  - revisa los proyectos
  - están los proyectos en orden
  - drift de proyectos
dependencies: []
description: |
  Audita los archivos de projects/ contra el esquema de project-template y las reglas de ciclo de vida. Caza drift en tres direcciones — lado archivo (frontmatter incompleto, status fuera de pending/working/done, secciones de la plantilla ausentes o con llaves sin rellenar), lado registro (proyectos sin entrada en mapa-contenido, entradas que apuntan a archivos borrados) y lado ciclo de vida (working estancados, pending eternos, done con pasos abiertos, Pendientes de ME.md apuntando a proyectos cerrados). Reporta primero, arregla con aprobación, nunca edita en silencio.
---
# project-janitor

Escanea los proyectos. Compara con la plantilla, el mapa y los logs. Reporta el drift. Arregla con aprobación.

Los archivos de `projects/` son la fuente de verdad sobre qué proyectos hay; la plantilla es la norma de forma; los logs delatan si un estado miente.

## Cuándo usarla

- Como pasada de higiene periódica, o cuando la cartera huela a desactualizada.
- Después de una racha de trabajo intensa en la que los proyectos se tocaron deprisa.
- Antes de una revisión de cartera con project-manager, para que la revisión parta de datos que cuadran.

## Cuándo NO usarla

- Para crear, actualizar o cerrar proyectos: eso es project-manager.
- Para auditar el resto de la carpeta o las skills: contenido-janitor y skills-janitor.

## Workflow

### 1. Escanear

Lee cada `.md` de `projects/`. Extrae frontmatter y secciones. Anota archivos con YAML roto.

### 2. Lado archivo

- Frontmatter completo: `created`, `updated`, `status`.
- `status` es uno de `pending | working | done`.
- Las secciones de la plantilla están presentes (Objetivo, Estado actual, Siguientes pasos, Personas, Decisiones) y sin llaves `{así}` sin rellenar.
- Decisiones con fecha; `updated` no anterior a la última decisión.

### 3. Lado registro

- Todo proyecto tiene su entrada en la Navegación de `mapa-contenido.md`.
- Toda entrada del mapa apunta a un archivo que existe.

### 4. Lado ciclo de vida

- `working` sin rastro en los logs de las últimas dos semanas → ¿sigue vivo?
- `pending` con más de un mes sin arrancar → ¿se descarta o se agenda?
- `done` con Siguientes pasos sin marcar → ¿se cerraron de verdad?
- Pendientes de `ME.md` que referencian proyectos `done` → propuesta de limpieza.

### 5. Reporte

Salida en chat, sin escribir archivos:

```
# Informe project-janitor — AAAA-MM-DD
Proyectos: N (pending P, working W, done D)

## Lado archivo
- {proyecto} — {problema concreto} (o "sin problemas")
## Lado registro
- {proyecto} — {sin registrar / entrada huérfana} (o "sin problemas")
## Ciclo de vida
- {proyecto} — {working estancado desde AAAA-MM-DD / ...} (o "sin avisos")
## Salud
{“En orden” o “N problemas en M proyectos.”}
```

Espera la aprobación del usuario antes de tocar nada.

### 6. Arreglo (con aprobación)

- **Arreglos seguros**: registrar proyectos en el mapa, retirar entradas huérfanas, completar frontmatters mecánicos (fechas).
- **Se reporta pero NO se auto-arregla**: cambios de `status` (decisión del usuario, vía project-manager), contenido de secciones (Objetivo vacío necesita al usuario), limpieza de Pendientes en ME.md (se propone, no se aplica).

## Qué produce

Un informe de drift de la cartera y, con visto bueno, archivos y mapa vueltos a cuadrar.

## Reglas

- Lee primero, escribe después. El informe siempre precede al cambio.
- Los cambios de estado nunca los hace el janitor: detecta y pregunta; el cambio pasa por project-manager.
- Sé específico: nombra el proyecto, el campo y el problema exacto.
- No toques los logs: son historia. El ciclo de vida se lee de ellos, no se corrige en ellos.

---
name: contenido-janitor
description: >-
  Audita mapa-contenido.md contra la realidad de la carpeta — en las dos
  direcciones del mapa. Navegación: carpetas y archivos reales que el mapa no
  documenta, y entradas del mapa que apuntan a cosas que ya no existen.
  Creación: archivos que no siguen las plantillas de AIOS/Templates/
  (frontmatters, estados de logs y propuestas), plantillas sin indexar en el
  mapa y entradas de plantilla sin archivo. projects/ y areas/ quedan fuera:
  los audita project-janitor. Reporta primero, arregla con aprobación, nunca
  edita en silencio. Se activa con frases como: "contenido janitor", "audita
  el contenido", "revisa los mapas", "está la carpeta en orden", "drift de
  carpetas".
metadata:
  system: contenido
  status: active
  created: "2026-06-11"
  updated: "2026-06-11"
---
# contenido-janitor

Escanea la carpeta. Compara con mapa-contenido. Reporta el drift. Arregla con aprobación.

La carpeta real es la fuente de verdad para la navegación; las plantillas del mapa son la norma para la creación. El mapa se reconcilia *hacia* la carpeta; los archivos se validan *contra* las plantillas.

## Cuándo usarla

- Después de crear o reorganizar varios archivos en `knowledge/`.
- Como pasada de higiene periódica, o cuando algo no esté donde el mapa dice.
- Si solo cambió un archivo, arregla el mapa a mano — el janitor renta con varios cambios a la vez.

## Cuándo NO usarla

- Para auditar skills y sistemas: eso es skills-janitor.
- Para crear archivos: la creación normal ya usa las plantillas del mapa.

## Workflow

### 1. Escanear la carpeta

Lista el árbol completo (raíz + subcarpetas). Ignora archivos ocultos y de sistema (`.gitkeep`, `.DS_Store`...).

### 2. Lado navegación (realidad → mapa)

- Carpetas o archivos relevantes que existen pero el mapa no documenta (por ejemplo, archivos nuevos en `knowledge/` sin registrar).
- Entradas del mapa que apuntan a carpetas o archivos que ya no existen.
- Reglas de escritura del mapa que ya no reflejan la realidad.

### 3. Lado creación (archivos → plantillas)

- Archivos de `knowledge/` sin el frontmatter mínimo (`created`, `updated`).
- Logs sin `consolidado:` o con un estado que no es `pendiente`/`sí`.
- `projects/` y `areas/` no se auditan aquí: tienen su propio auditor (project-janitor), con reglas de ciclo de vida que este no conoce.
- Propuestas con estado fuera de `pendiente`/`incorporada`/`descartada`, o propuestas `pendiente` de hace más de una semana (señal de que la tarea nocturna no las está re-presentando).
- Plantillas: todo archivo de `AIOS/Templates/` está en la tabla de plantillas del mapa, y toda fila de la tabla apunta a un archivo que existe. Plantillas alteradas respecto a su forma canónica se reportan.

### 4. Reporte

Salida en chat, sin escribir archivos:

```
# Informe contenido-janitor — AAAA-MM-DD

## Navegación
- {carpeta/archivo} — {sin documentar / entrada huérfana} (o "sin problemas")
## Creación
- {archivo} — {frontmatter incompleto / estado inválido / ...} (o "sin problemas")
## Salud
{“En orden” o “N problemas.”}
```

Espera la aprobación del usuario antes de tocar nada.

### 5. Arreglo (con aprobación)

- **Arreglos seguros**: registrar en el mapa lo que falta, retirar entradas huérfanas, completar frontmatters mecánicos (fechas, estados) con el dato evidente.
- **Se reporta pero NO se auto-arregla**: mover o renombrar archivos (decisión del usuario), contenido de knowledge que parezca obsoleto (criterio humano), propuestas pendientes antiguas (el usuario decide si firmarlas o descartarlas).

## Qué produce

Un informe de desfases y, con visto bueno, el mapa y los frontmatters vueltos a cuadrar.

## Reglas

- Lee primero, escribe después. El informe siempre precede al cambio.
- Nunca borres contenido para cuadrar un formato: el contenido manda sobre la plantilla.
- Sé específico: nombra el archivo y el problema exacto.
- No toques los logs de días anteriores más allá del frontmatter: son historia.

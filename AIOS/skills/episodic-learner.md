---
name: episodic-learner
system: learning-system
status: Active
created: 2026-06-11
updated: 2026-06-11
triggers:
  - genera el log de hoy
  - cierra el día
  - reconstruye el log
  - episodic learner
dependencies: [sesiones de Cowork (list_sessions, read_transcript)]
description: |
  Compone el log diario leyendo las transcripciones de las sesiones de Cowork del día y los cambios en los archivos de la carpeta. Escribe directo, sin pedir permiso — es el registro, la única skill con esa licencia. Extrae señales tipadas (novedoso, decidido, no resuelto, preferencia/regla) y mantiene al día la sección Pendientes de ME.md. Primer paso de la tarea nocturna del Learning System; también se invoca a demanda.
---
# episodic-learner

Automático. El usuario no lo toca: el coach construye el log escaneando lo que pasó.

## Cuándo usarla

- Cada noche, como primer paso de la tarea programada del Learning System.
- A demanda, si el usuario quiere el log antes de que corra la tarea.

## Cuándo NO usarla

- Para resumir una sola conversación a mitad de sesión — eso es una petición normal, no el log del día.
- Para proponer cambios a la memoria: eso es trabajo de semantic-learner y procedural-learner. Esta skill registra, no destila.

## Zona horaria

Todas las marcas de tiempo en Europe/Madrid, siempre: el nombre del archivo y cada señal. Los relojes del sistema suelen ir en UTC — convierte antes de escribir. Nunca escribas una hora futura; si no puedes determinar la hora local con confianza, dilo en el propio log.

## Workflow

1. Lista todas las sesiones de Cowork de hoy (Europe/Madrid) en esta carpeta y lee sus transcripciones. Salta las vacías o triviales.
2. Revisa también los archivos modificados hoy en la carpeta, por si hubo trabajo fuera de las sesiones.
3. Crea `episodic/logs/{hoy}.md` con la plantilla `AIOS/Templates/log-template.md` (léela, no la reconstruyas de memoria). Si ya existe el log, complétalo — no lo dupliques.
4. Redacta **Qué pasó**: una narrativa breve con la forma del día, no una lista de actividades.
5. Extrae las **Señales**, una frase declarativa por bloque, fecha y hora completas, con los cuatro tipos:
   - `novedoso` — contradice o extiende algo previo de la memoria o de la sesión.
   - `decidido` — cambio de rumbo, compromiso nuevo, abandono explícito.
   - `no resuelto` — pregunta abierta, tarea a medias, decisión diferida.
   - `preferencia/regla` — cómo le gusta trabajar al usuario. Heredable a sesiones futuras.
6. Actualiza la sección Pendientes de `ME.md`: añade los `no resuelto` nuevos y marca los que se hayan cerrado hoy.

## Qué pertenece al log

El log va del **usuario** — en qué trabajó, qué dijo, qué decidió, dónde estuvo su atención. Es su diario intersticial, no un registro de actividad del sistema.

- Su trabajo: conversaciones, decisiones, ideas, gestiones.
- Sus palabras: cítalas de las transcripciones cuando se pueda. No las reescribas.
- Trabajo del coach en su nombre: **una línea**, sin resumen del contenido. ✅ `Learning System ejecutado.` ❌ `Learning System ejecutado: se analizaron 4 sesiones en las que el usuario...` — eso duplica el log dentro del log.

## Qué NO pertenece al log

- Informes de escaneo automático ni entradas sobre el propio log.
- Ruido de robot en días tranquilos: si el usuario no hizo nada, el log queda casi vacío. No rellenes.
- Lo rutinario. Mejor capturar señal de más que de menos, pero lo trivial no es señal.

## Qué produce

El log del día (Qué pasó + Señales) y los Pendientes de `ME.md` al día.

## Reglas

- Nunca fabriques entradas: solo lo que de verdad pasó.
- Agrupa el trabajo relacionado de una misma sesión en una sola señal o párrafo.
- Una sesión vacía o trivial se salta, no se menciona.
- Esta es la única skill que escribe sin confirmación, y solo en sus dos destinos: el log y la sección Pendientes de ME.md. Ningún otro archivo.

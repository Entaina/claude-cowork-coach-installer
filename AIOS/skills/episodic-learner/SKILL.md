---
name: episodic-learner
description: >-
  Compone el log diario con las conversaciones disponibles de Cowork, Claude Code, GPT
  en local o Amazon Quick (escritorio) y los cambios en los archivos de la carpeta. Declara la
  cobertura real cuando el historial es parcial. Escribe directo, sin
  pedir permiso — es el registro, la única skill con esa licencia. Extrae
  señales tipadas (novedoso, decidido, no resuelto, preferencia/regla) y
  mantiene al día la sección Pendientes de ME.md. Primer paso de la tarea
  nocturna del Learning System; también se invoca a demanda. Se activa con
  frases como: "genera el log de hoy", "cierra el día", "reconstruye el log",
  "episodic learner".
metadata:
  system: learning-system
  status: active
  created: "2026-06-11"
  updated: "2026-10-07"
  dependencies: "AIOS/entornos-locales.md; herramientas nativas de historial disponibles"
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

1. Lee `AIOS/entornos-locales.md` y aplica el acceso a conversaciones de la app actual. Recupera solo las fuentes de esta carpeta y del día solicitado (Europe/Madrid), pagina según las herramientas disponibles y declara la cobertura real. No confundas historial inaccesible con un día sin actividad. Salta las sesiones vacías o triviales.
2. Revisa también los archivos modificados durante el día solicitado en la carpeta, por si hubo trabajo fuera de las sesiones. El día por defecto es hoy.
3. Si hay fuentes útiles, crea `episodic/logs/{día-solicitado}.md` (fecha `AAAA-MM-DD`) con la plantilla `AIOS/Templates/log-template.md` (léela, no la reconstruyas de memoria), añadiendo la nota de Cobertura definida en `AIOS/entornos-locales.md`. Si ya existe el log del día, conserva su contenido y propuestas; incorpora solo señales nuevas, sin duplicarlas por sesión/momento/hecho. Si entran señales nuevas en un log consolidado, vuelve a `consolidado: pendiente` conservando los estados de las propuestas resueltas. Sin fuentes, informa de la limitación y no sustituyas un log existente.
4. Redacta **Qué pasó**: una narrativa breve con la forma del día, no una lista de actividades.
5. Extrae las **Señales**, una frase declarativa por bloque, fecha y hora completas, con los cuatro tipos:
   - `novedoso` — contradice o extiende algo previo de la memoria o de la sesión.
   - `decidido` — cambio de rumbo, compromiso nuevo, abandono explícito.
   - `no resuelto` — pregunta abierta, tarea a medias, decisión diferida.
   - `preferencia/regla` — cómo le gusta trabajar al usuario. Heredable a sesiones futuras.
   Añade a cada señal una referencia breve a su fuente: ID de conversación y turno/momento, o ruta del archivo. Si procede de un resumen, indícalo. Sirve para comprobarla y reconocerla en una reejecución.
6. Actualiza únicamente la sección Pendientes de `ME.md`: añade los `no resuelto` nuevos y marca los cierres con evidencia explícita. No cierres un asunto por su ausencia en un historial parcial. Al reconstruir un día pasado, no reviertas estados actuales de Pendientes basándote en evidencia anterior a su última actualización; si el orden no es verificable, conserva el estado y señala la duda. Conserva todas las demás secciones.

## Qué pertenece al log

El log va del **usuario** — en qué trabajó, qué dijo, qué decidió, dónde estuvo su atención. Es su diario intersticial, no un registro de actividad del sistema.

- Su trabajo: conversaciones, decisiones, ideas, gestiones.
- Sus palabras: cítalas de las transcripciones cuando se pueda. No las reescribas.
- Trabajo del coach en su nombre: **una línea**, sin resumen del contenido. ✅ `Learning System ejecutado.` ❌ `Learning System ejecutado: se analizaron 4 sesiones en las que el usuario...` — eso duplica el log dentro del log.

## Qué NO pertenece al log

- Informes de escaneo automático ni entradas sobre el propio log; la única excepción es la nota breve de Cobertura.
- Ruido de robot en días tranquilos: si el usuario no hizo nada, el log queda casi vacío. No rellenes.
- Lo rutinario. Mejor capturar señal de más que de menos, pero lo trivial no es señal.

## Qué produce

El log del día (Qué pasó + Señales) y los Pendientes de `ME.md` al día.

## Reglas

- Nunca fabriques entradas: solo lo que de verdad pasó. Una sugerencia del asistente no es una decisión del usuario; un resumen no se cita como si fuera literal.
- La hora de una señal es la del hecho si está disponible; si no se conoce, usa la hora de registro, indica «hora del hecho no disponible» y no la atribuyas a la fuente.
- Agrupa el trabajo relacionado de una misma sesión en una sola señal o párrafo.
- Una sesión vacía o trivial se salta, no se menciona.
- Esta es la única skill que escribe sin confirmación, y solo en sus dos destinos: el log y la sección Pendientes de ME.md. Ningún otro archivo.

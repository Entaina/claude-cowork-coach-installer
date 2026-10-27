# INSTALL — prompt de instalación del coach

> **Si eres el usuario**: sigue el README. Este archivo se lee desde el repositorio y no se copia a tu carpeta.

La estructura del coach ya está en esta carpeta. Conserva sus mapas, skills, sistemas y plantillas. Instálalo conmigo en cuatro pasos. Si retomas una entrevista interrumpida, conserva lo ya respondido y no vuelvas a copiar archivos ni a crear tareas existentes.

## 1. Entrevístame

**Una sola pregunta por turno.** Tres temas, sin un mínimo de preguntas ni repreguntas obligatorias:

1. Nombre, rol, empresa y ubicación; puedo explicar en una frase qué hago. Con la ubicación, confírmame la zona horaria que deduces («¿tu hora es la de Ciudad de México?»): el coach la usa para fechar el día y programar la revisión.
2. Cómo quiero llamarte (por ejemplo, «Coach» o «Aria»).
3. Cómo me gusta trabajar: tono, cuándo desafiarme y cuándo acompañarme, qué evitar.

Aprovecha lo que ya haya contado; no vuelvas a pedirlo. Puedo responder en libre o decir «siguiente». No amplíes ahora la entrevista con mi día a día detallado, interlocutores, herramientas, crecimiento ni gaps. Si detectas huecos de contexto útiles para acompañarme —por ejemplo, mi rol sin aclarar o qué tareas hago con frecuencia—, recógelos en Pendientes para ir completándolos en próximas sesiones, cuando venga al caso. No conviertas toda la lista de temas en un cuestionario pendiente ni repitas información que ya conozcas. Si pido no tratar un tema, respétalo y no lo anotes para insistir después.

## 2. Rellena ME.md

Completa la presentación, Quién soy y Preferencias con mis respuestas. Escribe la línea `Zona horaria` con el identificador IANA confirmado (por ejemplo, `America/Mexico_City`). Si no la confirmo, deja `Europe/Madrid` y añade a Pendientes «Contexto por completar: confirmar mi zona horaria». Si omito un dato, usa «No indicado» o una frase que no lo afirme; no lo inventes. Si salto el nombre del asistente, usa «Asistente». No dejes marcadores de plantilla sin resolver.

`Goals` es opcional: conserva los objetivos que haya expresado espontáneamente; si no hay ninguno, escribe «Sin objetivos definidos por ahora». No me pidas definirlos para terminar. Los sistemas solo contrastan mi trabajo con objetivos que yo haya declarado.

En Pendientes recoge los asuntos que yo haya dejado abiertos o aceptado retomar y los huecos de contexto detectados durante la instalación. Formula estos últimos como preguntas por conocer, con el prefijo «Contexto por completar»; por ejemplo, «Contexto por completar: conocer mis tareas más frecuentes». No los presentes como compromisos, objetivos ni tareas que yo deba ejecutar, ni inventes sus respuestas. Conserva los pendientes existentes al retomar la instalación y evita duplicados. Si no hay asuntos abiertos ni huecos relevantes, escribe «Sin pendientes». Conserva las Reglas; ajústalas solo si mis respuestas las matizan. Enséñame el resultado, incluidos esos huecos, antes de guardarlo: «¿guardo?».

## 3. Configura el entorno y la revisión

Lee `AIOS/entornos-locales.md` y comprueba la carpeta, el acceso al historial y las herramientas de programación disponibles.

- **Claude Code CLI**: sigue `AIOS/claude-code.md`. Si falta Python, instalarlo es un paso de esta instalación y lo haces tú, con el OK del usuario; Git no se instala. La petición de instalación local fija el alcance de proyecto: muestra la vista previa del adaptador y aplica con la autorización correspondiente, sin volver a preguntar un alcance ya elegido. Comprueba las skills y el hook en una sesión nueva. Ofrece `/coach-review` a demanda; una programación del CLI depende de la sesión abierta y no se declara nocturna permanente.
- **Cowork**: conserva las dos tareas de los sistemas, Learning System a las 23:30 y Proyectos y Áreas a las 23:45 por defecto, en mi zona horaria de `ME.md`.
- **ChatGPT Work / Codex en la app local**: configura la revisión conjunta descrita en ese documento, a las 23:30 por defecto, en mi zona horaria de `ME.md`. Trabaja en esta carpeta permanente.
- **Amazon Quick (app de escritorio)**: sigue `AIOS/amazon-quick.md`. Dale al usuario el texto del agente Coach con la ruta real para que lo cree en Customize → Agents, y comprueba que lo ha publicado y marcado como predeterminado (Make default). Después, desde un chat con Coach, configura una sola rutina conjunta dentro de su jornada, con el equipo encendido y Quick abierto. En la versión web de Quick no hay carpeta local: explica que el coach no se puede instalar ahí y no lo simules.

Propón el horario, explica qué revisaré por la mañana y confirma la configuración. Busca tareas existentes antes de crear ninguna. Si falta una capacidad, explica cuál: la memoria puede quedar instalada para uso manual, pero la automatización queda pendiente y no se declara operativa. No actives otra revisión en una segunda app sobre la misma carpeta sin resolver cuál será la responsable.

## 4. Prueba

Ejecuta el mismo flujo de revisión una vez con el usuario delante, usando esta conversación como material disponible. Genera el primer log, enseña la cobertura real de las fuentes y las propuestas. Ejecuta también la revisión de proyectos aunque no haya proyectos nuevos.

Si hay propuestas, deja que apruebe o descarte alguna y comprueba el resultado. **Cero propuestas es válido**: no inventes una para completar la instalación. En ese caso basta con enseñar el log y explicar que hoy no hay cambios que validar.

Verifica que `CLAUDE.md` y `AGENTS.md` contienen exactamente las mismas instrucciones. Comprueba después, en una sesión nueva, que se lee el archivo de arranque del entorno (`CLAUDE.md` en Cowork y Claude Code, `AGENTS.md` en GPT y, en Quick, `AGENTS.md` en un chat nuevo con el agente Coach), `ME.md` y los mapas. Si esa sesión no carga las instrucciones, informa de que el arranque queda pendiente; no declares la instalación completamente verificada. La prueba manual no demuestra que la ejecución programada disponga de las mismas herramientas: deja esa comprobación pendiente hasta revisar su primera ejecución. En Cowork puedes usar «Run now» si existe; en GPT usa la acción disponible o la interfaz, sin inventar un parámetro de ejecución; en Quick, programa una ejecución única a pocos minutos vista.

---

Español de España, tuteo y explicaciones para un perfil no técnico. El funcionamiento del coach se describe en Markdown y usa las herramientas de cada entorno. Cowork, GPT y Quick no necesitan scripts adicionales. Claude Code añade el adaptador Python local descrito arriba, sin servicios externos ni herramientas de otra app.

Empieza la entrevista cuando estés listo.

# Amazon Quick (app de escritorio)

Adaptación de la carpeta del coach a la app de escritorio de Amazon Quick para macOS y Windows. Los canónicos siguen en `AIOS/skills/`; las reglas personales, en `ME.md`. `CLAUDE.md` y `AGENTS.md` no cambian. Contrastada el 2026-10-27 con la app 1.1.3905 en macOS, una cuenta individual y un perfil ficticio. Las pantallas y los nombres de herramientas pueden cambiar: comprueba el esquema real antes de llamar a una herramienta.

La **versión web** de Quick no da acceso a carpetas locales: sin ella no hay memoria en archivos ni revisión diaria. Queda fuera, igual que el resto de modalidades cloud. No sustituyas la carpeta por documentos de referencia de un agente web como si fuera el mismo coach.

## Cómo trabaja Quick

- El agente se ejecuta en la nube. La app de escritorio conecta el equipo como un «outpost» (rutas `/outposts/<equipo>/…`) y hace de puente para leer y escribir en la carpeta. Sin el equipo encendido y la app abierta, no hay acceso a los archivos.
- Al abrir un chat no se lee `AGENTS.md` ni `CLAUDE.md`. El arranque lo hace un agente propio, Coach, con instrucciones que mandan leer `AGENTS.md`.
- El historial de conversaciones es de la cuenta, no de la carpeta. Cada persona necesita su propia cuenta; el agente toma el nombre de la persona titular, no el de `ME.md`.
- Quick guarda además memorias propias y un grafo de conocimiento (menú de usuario → My context). No viajan con la carpeta. La memoria canónica sigue siendo `ME.md` y el resto de archivos: no traslades a esas memorias lo que pertenece a la carpeta.

## Preparar la carpeta

1. Crea una carpeta nueva y vacía. En Quick: Customize → Knowledge → Add folder. Conecta solo la carpeta del coach; si ya hay otras conectadas (por ejemplo, Descargas), recuérdale al usuario que una revisión programada puede escribir en todas.
2. Revisa con el usuario los ajustes de la carpeta (Settings). Las opciones de indexación suben los archivos a la nube para búsqueda completa y para el grafo de conocimiento. El coach no las necesita: basta con el acceso del agente. En una cuenta de empresa, decide según la política de la organización.
3. La escritura se autoriza en cada chat con una tarjeta de permiso: Deny, Allow once, This chat o Always allow. Para instalar, basta con «This chat». Explica la diferencia antes de que el usuario elija «Always allow».

## Instalación

El prompt de instalación del README funciona en Quick si se añade al principio la ruta de la carpeta: Quick no sabe a qué carpeta se refiere «esta». La copia se hace leyendo el repositorio desde la web y escribiendo en la carpeta a través del equipo; puede tardar varios minutos y pedir permisos más de una vez. Al terminar, compara el árbol con el del repositorio antes de seguir. No ejecutes `AIOS/integrations/claude_code.py`: es solo para Claude Code.

## Arranque: el agente Coach

Al terminar la entrevista y guardar `ME.md`, pide al usuario que cree el agente. Quick no lo crea desde un chat normal: Customize → Agents → Create → From chat, y pegar este texto con la ruta real en lugar de CARPETA_VERIFICADA:

> Quiero un agente llamado «Coach», solo para mí. Es un asistente personal cuya memoria vive en archivos Markdown de mi carpeta local CARPETA_VERIFICADA. Instrucciones: al empezar cada conversación, antes de responder, lee AGENTS.md de esa carpeta y sigue lo que dice (leer ME.md, AIOS/mapa-contenido.md y AIOS/mapa-skills.md). Trátame según ME.md. Cuando aprendas una preferencia o un dato duradero, propónme guardarlo en el archivo que toque con la pregunta «¿guardo?» y escríbelo en la carpeta solo si digo que sí. Fuentes: solo esa carpeta; nada de web salvo que yo lo pida.

Si el creador pregunta qué hacer cuando falte un archivo, la respuesta coherente con el coach es avisar y preguntar. Revisa las instrucciones que redacta antes de publicar: las reescribe con sus palabras. Después, el usuario elige Coach en el selector de agentes de cada chat. Comprueba en un chat nuevo con Coach que lee `ME.md` y los mapas, y que una skill se activa por su frase («pule esto» activa `pulidor`).

## Conversaciones del día

Quick expone la consulta del historial de la cuenta; en la versión contrastada, la herramienta `query_conversations` (módulo «Gestionar conversaciones») devuelve títulos, identificadores, fechas y mensajes. Filtra por la marca de cada mensaje al intervalo del día según `AIOS/entornos-locales.md`, no por la fecha del hilo.

Límites observados:

- Algunas respuestas del asistente vuelven incompletas. Una respuesta truncada no demuestra que una pregunta quedara sin contestar: no la conviertas en pendiente sin otra evidencia.
- Las conversaciones en modo incógnito no aparecen.
- Pueden aparecer conversaciones sin título propio («New Conversation»). Compruébalas antes de tratarlas como actividad del usuario.
- La propia app puede afirmar que no tiene acceso al historial y tenerlo. Decide con una llamada real, no con su descripción.

Declara la cobertura como **Parcial** salvo que puedas acreditar el listado completo y el contenido íntegro.

## Programación: una revisión conjunta

Una sola rutina ejecuta Learning y después Proyectos y Áreas, como en GPT local. Créala desde un chat con Coach, después de preguntarle por las rutinas existentes y reutilizar una coincidencia inequívoca. Quick muestra una tarjeta «Creating schedule» con la hora, la zona horaria y los permisos que concede; revísala con el usuario antes de aprobarla.

Prompt (sustituye CARPETA_VERIFICADA):

> Crea una rutina diaria que trabaje en CARPETA_VERIFICADA, la carpeta permanente de mi coach. Que lea AGENTS.md, ME.md y los mapas, ejecute el Learning System según AIOS/systems/learning-system.md y después el Sistema Proyectos y Áreas según AIOS/systems/proyectos-y-areas.md sobre ese mismo log, leyendo mis conversaciones de Quick según AIOS/entornos-locales.md. Que complete ambas fases antes de pedir validación, no aplique propuestas sin mi respuesta y no escriba fuera del log del día y de la sección Pendientes de ME.md. Si no hay novedades ni propuestas pendientes, que no me avise.

Tres condiciones de esta rutina:

- **Horario.** La rutina corre en la nube, pero solo llega a la carpeta a través de la app. Elige una hora dentro de la jornada, con el equipo encendido y Quick abierto. Las 23:30 por defecto fallan si el equipo se apaga al terminar el día. Comprueba la hora y la zona horaria que muestra la tarjeta.
- **Permisos.** La rutina recibe permiso para escribir en cualquier archivo de las carpetas conectadas; no se puede limitar a uno. Que solo toque sus destinos depende de las instrucciones. Por eso conviene conectar únicamente la carpeta del coach.
- **Aviso.** Al terminar, Quick deja un aviso con el resultado (en la prueba, en el Feed).

No actives a la vez la revisión de Quick y la de otra app sobre la misma carpeta (ver `AIOS/entornos-locales.md`).

## Verificación

Para la primera comprobación, programa una ejecución única a pocos minutos vista y revisa después qué archivos cambiaron: el log del día con su nota de cobertura y, si procede, Pendientes. Crear la rutina no demuestra que funcione. Contrastado el 2026-10-27: copia íntegra del paquete, entrevista y `ME.md`, arranque mediante el agente Coach, escritura de una preferencia con confirmación, activación de `pulidor`, y una rutina de `episodic-learner` sin el usuario delante que escribió el log con su cobertura y no tocó ningún otro archivo.

Sin contrastar todavía: la revisión conjunta completa con las propuestas de los tres learners, varias ejecuciones diarias seguidas, una cuenta de empresa con administrador y Windows.

## Otros límites

- Los títulos de las conversaciones y parte del razonamiento intermedio salen en inglés aunque las respuestas sean en español.
- La instalación y las rutinas consumen la cuota del plan. AWS no publica cuántas horas de agente incluyen los planes Free, Plus y Max.
- El coach fecha el día en Europe/Madrid. Si el usuario trabaja en otra zona horaria, el día del log no coincide con su jornada; tenlo en cuenta al elegir la hora de la rutina y avisa al usuario.

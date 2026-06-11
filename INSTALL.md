# INSTALL — prompt de instalación del coach

> **Si eres el usuario**: no necesitas leer esto. Sigue la instalación del README — su prompt hace que la IA ejecute este archivo desde el repositorio. Este archivo no se copia a tu carpeta.

---

La estructura de mi coach ya existe en esta carpeta: mapas, skills, sistemas y plantillas están decididos. **No los rediseñes, no los reescribas, no los "mejores".** Tu trabajo es instalarlo conmigo, en cuatro pasos:

## 1. Entrevístame

Asume el rol de entrevistador: **una sola pregunta por turno**, escucha, conecta con lo anterior y decide la siguiente. Cinco temas, en este orden aproximado (6-8 preguntas en total con los follow-ups):

1. Nombre, rol, empresa, ubicación.
2. Cómo quiero llamarte (el nombre del coach: "Coach", "Aria", lo que sea).
3. Mi día a día: responsabilidades, decisiones que tomo, con quién trabajo, qué herramientas uso.
4. Hacia dónde quiero crecer y qué gaps veo.
5. Cómo me gusta trabajar: tono, cuándo desafiarme y cuándo acompañarme, qué evitar.

Ofrece opciones cerradas cuando ayude; siempre puedo responder en libre o decir "siguiente". Todo lo que dé para más (CV o LinkedIn, métricas, clientes o proyectos uno a uno...) no lo preguntes hoy: apúntalo para Pendientes y ve sacándolo en próximas sesiones. La entrevista se completa con el tiempo, no en una tirada.

## 2. Rellena ME.md

Con lo que salga, completa `ME.md`: Quién soy, Goals, Preferencias (incluido tu nombre) y Pendientes (con lo aplazado de la entrevista). No dejes ninguna llave `{así}` sin rellenar. Las Reglas ya están escritas; ajústalas solo si dije algo en la entrevista que las matice. Antes de guardar, enséñame el resultado: "¿guardo?".

## 3. Crea la tarea programada del Learning System

Una tarea programada cada noche (proponme la hora; por defecto 23:30) con el prompt que indica `AIOS/systems/learning-system.md` en su sección Orquestación — fino, apuntando a las skills, sin duplicar sus workflows. Explícame en dos frases qué veré cada mañana.

## 4. Prueba

Sigue la sección "Primer arranque" de `AIOS/systems/learning-system.md`: ejecuta la tarea una vez ahora mismo, usando esta misma conversación como material. Enséñame mi primer log en `episodic/logs/`, las primeras propuestas con su estado, y deja que apruebe o descarte alguna. Terminado = he visto mi primer log y he respondido a una propuesta.

---

Reglas de esta sesión: español de España, tuteo. Soy un perfil no técnico: nada de rutas, JSON ni configuración — la fontanería es tuya, con confirmaciones simples. Nada de código ejecutable: todo se hace con skills en Markdown, subagentes y tareas programadas de Cowork.

Empieza la entrevista cuando estés listo.

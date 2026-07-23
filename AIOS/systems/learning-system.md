---
name: learning-system
skills: episodic-learner, semantic-learner, procedural-learner
created: 2026-06-11
---
# Learning System

Cómo aprende el coach. Sin este sistema, el coach del día 30 sabe lo mismo que el del día 1: cada noche registra lo que pasó y propone qué debe pasar a la memoria duradera. Nada entra en ME.md, knowledge/ ni AIOS/ sin firma del usuario — con una sola excepción: la sección Pendientes de ME.md.

## Skills

- **episodic-learner** — compone el log del día leyendo las sesiones de Cowork. El único que escribe directo.
- **semantic-learner** — propone cambios a la memoria semántica (knowledge/ y Quién soy/Goals de ME.md).
- **procedural-learner** — propone cambios a Preferencias/Reglas de ME.md y candidatas a skill nueva.

## Orquestación

**Una sola tarea programada nocturna** (23:30 por defecto, Europe/Madrid). Su prompt es fino y apunta a las skills — nunca duplica sus workflows:

> "Ejecuta el Learning System según `AIOS/systems/learning-system.md`: episodic-learner primero; después semantic-learner y procedural-learner en paralelo, como subagentes; termina presentándome las propuestas y espera mi respuesta."

Secuencia: (1) episodic-learner escribe el log; (2) los dos learners de propuestas leen *el log* (no las transcripciones) y anotan sus propuestas al pie con estado `pendiente`; (3) la sesión termina presentándolas al usuario y queda a la espera.

**El hand-off**: el usuario responde esa noche o al abrir la sesión a la mañana siguiente — sí, no, o corrige. El coach aplica las aprobadas en sus destinos, descarta el resto, actualiza el estado de cada una en el log y marca el log como `consolidado: sí`. **Al aplicar una propuesta que crea un archivo o directorio nuevo, parte de la plantilla correspondiente de `AIOS/Templates/` — lee el archivo de la plantilla antes, no la reconstruyas de memoria.** Las propuestas `pendiente` de días anteriores se re-presentan cada noche hasta que el usuario las resuelva: nada se pierde por no contestar un día.

## Cuándo NO usarlo

- Como editor en tiempo real de la memoria: si el usuario pide en mitad de una sesión "apunta que prefiero X", se edita ME.md con confirmación ahí mismo — no se espera a la noche.
- Como tracker de tareas: los Pendientes son hilos abiertos del coach, no un gestor de proyectos.

## Ejemplos correctos

- *Mañana, el usuario abre la sesión nocturna:* "3 propuestas de ayer: (1) añadir a knowledge/cliente-acme.md que el contacto pasó a ser Roberto; (2) regla nueva: los informes siempre en una página; (3) detecté que preparas la reunión de los lunes cada semana — ¿creo una skill?". El usuario: "1 y 3 sí, 2 no". El coach aplica, dispara skill-builder para la 3, actualiza estados, marca el log consolidado.
- *Día tranquilo:* el log queda casi vacío y hay cero propuestas. Resultado válido — el sistema no rellena.

## Ejemplos incorrectos

- *El semantic-learner edita knowledge/ directamente "porque la señal era clara".* Jamás: propone, no aplica.
- *La tarea nocturna re-redacta el workflow de los learners en su prompt.* El prompt apunta a las skills; el archivo de cada skill es la fuente de verdad.
- *Veinte propuestas en una noche.* Tope 5-7 por learner, las de más señal. La firma matinal debe costar dos minutos, no veinte.

## Primer arranque

Tras crear la tarea programada, ejecútala una vez a mano (botón "Run now" en la sección Programadas de Claude) con el usuario delante: así se pre-aprueban los permisos que necesita y las ejecuciones nocturnas no se quedan colgadas esperando autorizaciones.

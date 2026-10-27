# Verificación del instalador

El instalador son instrucciones Markdown ejecutadas por un agente. Estas pruebas comprueban la integridad del paquete; no sustituyen la instalación real en cada app.

## Comprobaciones automáticas

Solo para desarrollo, con Python 3 y PyYAML disponibles:

```sh
python3 -m unittest discover -s tests -v
```

Comprueban el formato de las skills, las referencias a skills y archivos de AIOS, la coherencia de la versión, la integridad de las migraciones y la igualdad exacta de CLAUDE.md y AGENTS.md. `baseline-2.0.0.json` registra los hashes de los originales de la revisión indicada. No se regenera desde archivos editados para hacer pasar una prueba.

Esta carpeta se excluye de la copia al usuario. Cowork y GPT no requieren Python ni estas pruebas para funcionar. La integración nativa opcional de Claude Code sí requiere Python 3.9+ con la base de zonas horarias; no requiere PyYAML.

## Pruebas de comportamiento

Ejecutar en carpetas de prueba, con datos sintéticos y sin programaciones reales:

| Caso | Resultado observable |
| --- | --- |
| Instalación nueva; saltar datos y objetivos | ME.md sin marcadores de plantilla; Goals opcionales; no inventa respuestas ni compromisos. |
| Huecos de contexto detectados (rol, tareas frecuentes…) | Los recoge como «Contexto por completar» en el ME que muestra antes de guardar, sin ampliar la entrevista. |
| Tema rechazado expresamente o dato ya conocido | No lo añade a Pendientes para insistir después ni genera una lista genérica de temas. |
| Retomar entrevista | Conserva respuestas, archivos y pendientes existentes sin duplicarlos; no vuelve a copiar la plantilla. |
| Migrar 2.0.0 sin personalización | Dos archivos de arranque completos e idénticos; versión final 2.1.0. |
| Migrar CLAUDE.md personalizado | Conserva cada regla acordada en ambos archivos de arranque. |
| AGENTS y CLAUDE diferentes, sin decisión | No altera archivos ni avanza versión. |
| Puntero de una candidata anterior | Conserva el contenido de AGENTS.md y deja ambos arranques completos e idénticos. |
| AIOS personalizado, sin decisión | Inspecciona todos los conflictos y se detiene antes de escribir. |
| Migración interrumpida y reejecución | Retoma sin pérdidas; segunda pasada no cambia el resultado. |
| Historial GPT parcial, archivado, antiguo o ajeno | Solo usa turnos del día y carpeta; declara límites; sugerencias no aceptadas no son decisiones. |
| Historial no disponible | Conserva log y pendientes; informa de la limitación. |
| Reejecutar un log consolidado con una señal nueva | Conserva propuestas resueltas, añade la señal una vez y reabre consolidación. |
| Reconstruir ayer | Escribe el log de ayer; no incorpora cambios que solo ocurrieron hoy. |
| Cowork con transcripciones completas | Sigue generando el log con las herramientas de Cowork. |
| Tarea Cowork con el prompt original 2.0.0 | Detecta la instrucción paralela; ofrece adaptar el prompt con confirmación y conserva configuración si falta aprobación. |
| Revisión con propuesta descartada y señal nueva ajena | Conserva el rechazo y no crea una propuesta equivalente; reutiliza las pendientes existentes. |
| Pasada que cruza medianoche | Todos los learners conservan la fecha y el log elegidos al iniciar. |
| Día sin propuestas | Termina sin inventar una propuesta para demostrar el flujo. |
| Usuario en otra zona horaria (p. ej. Ciudad de México) | La entrevista la confirma y `ME.md` lleva su identificador IANA; el log, las señales y la revisión usan su día local. Sin la línea, se mantiene `Europe/Madrid`. |

Registrar archivos antes/después y comprobar que ME.md (salvo Pendientes al ejecutar episodic-learner), proyectos, áreas y conocimiento permanecen intactos. Una simulación de estas situaciones acredita decisiones bajo esos datos, no la disponibilidad de herramientas en una app real.

## Comprobación final en cada app

En una carpeta de prueba, instalar desde la revisión candidata, abrir otra sesión y comprobar que se lee el arranque del entorno (CLAUDE.md en Cowork, AGENTS.md en GPT), ME y los mapas. Ambos arranques deben contener las mismas instrucciones completas. Leer conversaciones reales de esa carpeta. Crear una sola programación con el horario elegido, repetir su configuración y verificar que no se duplica. Revisar una ejecución efectiva del programador: carpeta correcta, herramientas accesibles, log y propuestas sin aplicar. Probar por separado Cowork y GPT y desactivar la tarea de prueba al terminar.

La ejecución manual y la creación de la tarea no acreditan por sí solas su ejecución programada.

## Claude Code nativo (2.2.0)

`test_claude_code.py` ejecuta el adaptador en carpetas temporales con datos ficticios: vista previa, segunda instalación sin cambios, configuración/hook existente conservados, conflictos sin escrituras, aislamiento de carpetas, metadatos y límites de fechas/día con cambio horario, formato inesperado y exclusión del contenido mecánico. No ejecuta un modelo ni sustituye una prueba del CLI.

Para verificar el host real, prepara una carpeta de coach con perfil ficticio, instala el adaptador y abre una sesión nueva de Claude Code. Comprueba en su registro nativo las once skills y `/coach-review`; invoca una y observa la lectura del canónico, el alta de la sesión por el hook y la recuperación del mensaje con ID/hora. Ejecuta Learning y Proyectos, compara archivos y repite sin hechos nuevos. Comprueba también una subcarpeta y que los artefactos del adaptador no se conviertan en señales del diario.

No uses `--safe-mode`, `--bare` o una prueba con todas las skills/hooks deshabilitados para afirmar descubrimiento nativo. Si el fixture vive dentro de otro proyecto, excluye sus instrucciones antecesoras y globales con ajustes exclusivos de la prueba; no cambies ajustes personales. Usa permisos y herramientas limitados al fixture, sin MCP ni servicios externos. No pases `--no-session-persistence` en la prueba de historial: impediría comprobar una transcripción guardada.

Un visto bueno textual de Claude no prueba la configuración: registra las llamadas, los archivos generados y las comprobaciones de conservación. La programación nocturna se acredita por separado.

## Amazon Quick (2.3.0)

Quick no ejecuta código del paquete: no hay prueba automática de su integración. Las comprobaciones de integridad cubren la guía nueva, sus referencias y los originales de la migración.

Para verificar la app real, usa una cuenta de prueba, una carpeta vacía conectada solo a Quick y un perfil ficticio. Instala con el prompt del README y la ruta al principio, y compara el árbol con el de la revisión candidata. Crea el agente Coach y comprueba en un chat nuevo con él que lee `ME.md` y los mapas. Programa una ejecución única a pocos minutos vista y compara los archivos antes y después: solo deben cambiar el log del día y, si procede, Pendientes. No uses la memoria propia de Quick (My context) como prueba de que el coach recuerda: lo que cuenta es lo escrito en la carpeta.

### Verificación realizada (2026-10-27)

- macOS, app de escritorio 1.1.3905, cuenta individual en plan Free con prueba de Plus, sobre la revisión 2.2.0 y con la ruta de la carpeta añadida al prompt.
- Copia de los 32 archivos idéntica al repositorio y cuatro carpetas vacías. La copia llevó unos diez minutos y pidió permisos de escritura en el equipo.
- Entrevista completa con un perfil ficticio: `ME.md` sin marcadores, sin datos inventados y con «¿guardo?» antes de escribir. Sin el contrato de Quick, el instalador dejó la automatización pendiente y no ejecutó el adaptador de Code.
- Un chat nuevo con el agente de serie no leyó `ME.md`. El agente Coach sí lo leyó al arrancar, propuso guardar una preferencia y la escribió en `ME.md` tras la confirmación. «Pule esto» activó `pulidor`.
- Una rutina única escribió un archivo en la carpeta con el usuario ausente y listó las conversaciones de la cuenta, aunque el agente había asegurado antes que no tendría acceso. Otra rutina ejecutó `episodic-learner` sobre un día anterior: log con la plantilla, señales con su fuente y cobertura parcial; solo cambiaron el log y Pendientes.
- Límites observados: respuestas del asistente truncadas en el historial (una pregunta contestada quedó como pendiente), modo incógnito fuera del historial y título de las conversaciones en inglés.

No se ha probado la revisión conjunta completa con los tres learners, varias ejecuciones diarias, una cuenta de empresa con administrador ni Windows.

La zona horaria del usuario se añadió después de esta prueba: el lector de Code la tiene cubierta por `test_claude_code.py` (Ciudad de México, `--tz` y vuelta a Madrid), pero la entrevista que la confirma y su uso en Quick no se han ejecutado en una app real.

## Verificación realizada para 2.2.0 (2026-10-07)

- 29 pruebas automáticas correctas: 20 del adaptador y 9 de integridad. Entorno real: macOS, Python 3.9.6 y Claude Code 2.1.286.
- Claude revisó el código mediante su CLI. Detectó problemas con cambios de subcarpeta, selección del módulo del hook, transcripciones largas y conservación de ajustes retirados. Se corrigieron y su segunda revisión no encontró bloqueantes demostrables.
- En un coach ficticio y aislado, el CLI descubrió las once skills y `/coach-review`, leyó el perfil a partir de CLAUDE.md, registró sesiones y recuperó sus mensajes con fuente/hora. La revisión nativa leyó los canónicos y ejecutó Learning y Proyectos en orden.
- Una decisión y una preferencia de una conversación anterior llegaron al diario. Solo cambiaron el diario y un pendiente cerrado expresamente; la preferencia quedó como propuesta pendiente y el hueco de contexto siguió abierto. Dos repeticiones sin hechos nuevos dejaron esos archivos idénticos.
- Abrir directamente una subcarpeta permitió usar las skills pero no activó el hook del padre. La guía exige iniciar Claude desde la raíz; la repetición desde esa raíz registró correctamente la nueva sesión.
- Migración ejecutada sobre 2.1.0 con datos y personalizaciones ficticios: 28 archivos previos conservados, segunda pasada con 38/38 archivos idénticos y caso conflictivo con 37/37 intactos. Las migraciones históricas se conservaron.

Las pruebas reales limitaron las herramientas al coach ficticio y a su lector de historial; no verificaron inventario por fecha de modificación ni programación. No se ha ejecutado una entrevista completa nueva, una tarea nocturna, Windows/Linux ni otra nueva prueba de Cowork/GPT en esta revisión. La selección implícita de cada una de las once skills no se ha ensayado individualmente. El formato de historial sigue siendo interno y su cobertura, parcial. Las transcripciones de QA se conservan fuera del paquete público.

# Verificación del instalador

El instalador son instrucciones Markdown ejecutadas por un agente. Estas pruebas comprueban la integridad del paquete; no sustituyen la instalación real en cada app.

## Comprobaciones automáticas

Solo para desarrollo, con Python 3 y PyYAML disponibles:

```sh
python3 -m unittest discover -s tests -v
```

Comprueban el formato de las skills, las referencias a skills y archivos de AIOS, la coherencia de la versión y la integridad de las migraciones. `baseline-2.0.0.json` registra los hashes de los originales de la revisión indicada. No se regenera desde archivos editados para hacer pasar una prueba.

Esta carpeta se excluye de la copia al usuario. El coach no requiere Python ni estas pruebas para funcionar.

## Pruebas de comportamiento

Ejecutar en carpetas de prueba, con datos sintéticos y sin programaciones reales:

| Caso | Resultado observable |
| --- | --- |
| Instalación nueva; saltar datos y objetivos | ME.md sin marcadores pendientes; Goals opcionales; ningún pendiente inventado. |
| Retomar entrevista | Conserva respuestas y archivos; no vuelve a copiar la plantilla. |
| Migrar 2.0.0 sin personalización | Nuevos archivos y puntero válidos; versión final 2.1.0. |
| Migrar CLAUDE.md personalizado | Conserva cada regla acordada en AGENTS.md antes de reemplazar el origen. |
| AGENTS y CLAUDE diferentes, sin decisión | No altera archivos ni avanza versión. |
| AIOS personalizado, sin decisión | Inspecciona todos los conflictos y se detiene antes de escribir. |
| Migración interrumpida y reejecución | Retoma sin pérdidas; segunda pasada no cambia el resultado. |
| Historial GPT parcial, archivado, antiguo o ajeno | Solo usa turnos del día y carpeta; declara límites; sugerencias no aceptadas no son decisiones. |
| Historial no disponible | Conserva log y pendientes; informa de la limitación. |
| Reejecutar un log consolidado con una señal nueva | Conserva propuestas resueltas, añade la señal una vez y reabre consolidación. |
| Reconstruir ayer | Escribe el log de ayer; no incorpora cambios que solo ocurrieron hoy. |
| Cowork con transcripciones completas | Sigue generando el log con las herramientas de Cowork. |
| Día sin propuestas | Termina sin inventar una propuesta para demostrar el flujo. |

Registrar archivos antes/después y comprobar que ME.md (salvo Pendientes al ejecutar episodic-learner), proyectos, áreas y conocimiento permanecen intactos. Una simulación de estas situaciones acredita decisiones bajo esos datos, no la disponibilidad de herramientas en una app real.

## Comprobación final en cada app

En una carpeta de prueba, instalar desde la revisión candidata, abrir otra sesión y comprobar la lectura de AGENTS/ME/mapas. Leer conversaciones reales de esa carpeta. Crear una sola programación con el horario elegido, repetir su configuración y verificar que no se duplica. Revisar una ejecución efectiva del programador: carpeta correcta, herramientas accesibles, log y propuestas sin aplicar. Probar por separado Cowork y GPT y desactivar la tarea de prueba al terminar.

La ejecución manual y la creación de la tarea no acreditan por sí solas su ejecución programada.

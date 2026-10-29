---
name: pokm
skills: pokm
created: 2026-10-29
---
# Sistema pOKM

El mapa de los documentos de trabajo del usuario. Sin él, el coach busca a ciegas en sus carpetas o le pide rutas, y puede acabar abriendo lo que no debía (una nómina, una evaluación). Con él, sabe dónde buscar y qué no tocar. Es opcional: lo activa el usuario, y no hace falta para las carpetas que ya cubre un OKM de empresa.

## Skills

- **pokm**: activa y construye el mapa con el usuario, lo consulta al buscar documentos y lo mantiene al día en la revisión diaria.

## Orquestación

- **Activación**, a demanda: una conversación con el usuario (apartado A de la skill). Decide él qué carpetas entran y con qué nivel: «índice» (se describen sus documentos), «mapa» (solo la carpeta) o «fuera».
- **Consulta**, en vivo: el coach empieza por `pokm/mapa.md` cuando busca un documento. Lo indican dos líneas de `ME.md` escritas al activarlo.
- **Mantenimiento automático**: tercera fase de la revisión diaria, tras Learning y Proyectos y Áreas, solo si el pOKM está activo. En Cowork, al final de la tarea de Proyectos y Áreas; en Claude Code, dentro de `/coach-review` y de su tarea programada local; en GPT local y Amazon Quick, dentro de la revisión conjunta. Su prompt no cambia: la fase la activa `AIOS/systems/proyectos-y-areas.md`. En Quick es beta, sin programa y sin índices.

**El hand-off**: no hay propuestas que firmar. El mapa es un dato derivado de las carpetas del usuario y la revisión lo pone al día sola, con cuatro límites: solo dentro de lo que el usuario eligió (lo nuevo fuera del mapa se avisa y no entra), lo sensible no se describe y pasa a «fuera», un tope de documentos por pasada y las «Notas» del usuario intactas. Lo que cambió queda en la sección `## pOKM` del diario. Cambiar el alcance o desactivarlo es siempre una petición del usuario.

## Cuándo NO usarlo

- Para carpetas cubiertas por un OKM de empresa: se consultan con sus propios mapas.
- Para guardar contexto en la memoria del coach: el pOKM apunta dónde está cada cosa; no copia contenido.
- Para ordenar las carpetas del usuario: mapear no es reorganizar.

## Ejemplos correctos

- *El usuario pregunta por la tarifa vigente.* El coach lee `pokm/mapa.md`, baja al índice de Comercial, abre «Tarifa 2026» (no la de 2025, marcada como superada) y responde con la fuente.
- *Por la noche aparecen un acta nueva en Dirección (nivel «mapa»), una propuesta en un cliente (nivel «índice») y una carpeta «Legal» sin decidir.* La revisión actualiza el recuento de Dirección sin abrir el acta, describe la propuesta en su índice y deja en el diario «carpeta nueva fuera del mapa: Legal; dime si la añado».

## Ejemplos incorrectos

- *El coach mapea «Legal» porque está en una unidad compartida que ya revisaba.* Lo nuevo fuera del alcance no entra solo.
- *El índice dice «Tarifa 2026: HM-10 a 7.950 €».* El mapa dice qué es cada documento y cuándo leerlo, no copia sus cifras.
- *El coach responde «no hay fecha de apertura» porque el mapa no la menciona.* El mapa dice dónde buscar; la respuesta está en el documento.
- *«¿Cuánto se lleva Marta de comisión?» y el coach abre el Excel de comisiones, marcado como fuera.* La pregunta no es permiso: dice que quedó fuera y pregunta antes de abrirlo.

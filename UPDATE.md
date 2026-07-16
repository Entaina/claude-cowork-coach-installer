# UPDATE — prompt de actualización del coach

> **Si eres el usuario**: no necesitas leer esto. Sigue la sección "Actualización" del README — su prompt hace que la IA ejecute este archivo desde el repositorio. Este archivo no se copia a tu carpeta.

---

El coach ya está instalado en esta carpeta: mapas, skills, sistemas, plantillas y el contenido del usuario ya existen. Tu trabajo es traerlo a la última versión del repositorio aplicando **solo los cambios que le falten**, sin tocar nada de lo que es del usuario. En cuatro pasos.

## 1. Averigua desde qué versión partes

- Lee `AIOS/VERSION.md` en esta carpeta: esa es la versión instalada.
- Si no existe, la instalación es anterior al versionado: trátala como `1.0.0`.

## 2. Lee el CHANGELOG del repositorio

- Lee `CHANGELOG.md` del repositorio `https://github.com/Entaina/claude-cowork-coach-installer` (el del repo, no una copia local si la hubiera).
- Quédate con las versiones **posteriores** a la instalada, en orden ascendente. Son las pendientes.
- Si no hay ninguna pendiente, dilo — "Ya estás en la última versión (X)" — y termina aquí.

## 3. Enséñame qué vas a aplicar y espera mi OK

- Resume, en lenguaje llano, qué aporta cada versión pendiente: una línea por versión.
- No apliques ni escribas nada hasta que confirme.

## 4. Aplica los cambios, versión a versión

Por cada versión pendiente, en orden ascendente, aplica sus entradas del CHANGELOG con estas reglas:

- **Añadido** (archivos nuevos): cópialos tal cual desde el repositorio, a la misma ruta. Si el archivo ya existiera con contenido distinto, párate y pregúntame.
- **Cambiado** (mapas y sistemas que ya tienes): edición **quirúrgica** — añade solo las líneas o entradas que indica la entrada del CHANGELOG. **Nunca sobrescribas el archivo entero**: puede llevar skills, sistemas o entradas de mapa que creaste tú. Si algo ya está aplicado, sáltalo.
- **Retirado**: retira solo lo nombrado explícitamente, y confírmamelo antes.
- **Repo**: no hay nada que aplicar en tu carpeta.
- **Marcador `AIOS/VERSION.md`**: no lo trates como un archivo más ni lo copies del repositorio, aunque una versión lo mencione — el del repo refleja siempre la última versión publicada, no la que estás aplicando. En cuanto termines de aplicar **por completo** una versión, crea o actualiza `AIOS/VERSION.md` con **esa** versión antes de pasar a la siguiente. Así, si algo se interrumpe, el marcador refleja exactamente lo aplicado y una reejecución retoma donde iba.

### Reglas de seguridad (inviolables)

- **No toques nunca contenido del usuario**: `ME.md`, `projects/`, `areas/`, `knowledge/` ni `episodic/`. Son míos.
- **No borres** skills, entradas de mapa, sistemas ni archivos que no aparezcan explícitamente como "Retirado" en el CHANGELOG. Actualizar solo añade y modifica lo indicado; nunca limpia por su cuenta.
- **Ante cualquier duda o conflicto** —un archivo "Cambiado" que ya habías tocado, un "Añadido" que ya existe con otro contenido— párate y pregúntame antes de escribir.
- Trabajos pesados o comparaciones largas, delégalos a un subagente; yo solo veo el resultado.

## Al terminar

- Comprueba que `AIOS/VERSION.md` quedó en la última versión aplicada (lo has ido creando/actualizando versión a versión).
- Enséñame un resumen: qué versiones apliqué y qué archivos cambié o creé.
- Sugiéreme pasar `skills-janitor` y `contenido-janitor` para verificar que mapas, skills y carpetas cuadran.

---

Reglas de esta sesión: español de España, tuteo. Soy un perfil no técnico: nada de rutas, JSON ni configuración a la vista — la fontanería es tuya, con confirmaciones simples ("¿aplico?"). Empieza cuando estés listo.

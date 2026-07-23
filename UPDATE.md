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

## 4. Ejecuta las migraciones, versión a versión

Cada versión tiene su archivo de instrucciones en `migrations/` del repositorio (`migrations/1.1.0.md`, `migrations/2.0.0.md`…). Por cada versión pendiente, en orden ascendente:

- Lee `migrations/<versión>.md` del repositorio y ejecútalo al pie de la letra. Si una versión no tiene archivo de migración, no hay nada que aplicar en tu carpeta: es una versión solo-repo.
- En cuanto termines de aplicar **por completo** una migración, crea o actualiza `AIOS/VERSION.md` con **esa** versión antes de pasar a la siguiente. Así, si algo se interrumpe, el marcador refleja exactamente lo aplicado y una reejecución retoma donde iba.

### Vocabulario de las migraciones

Las migraciones usan estas operaciones; aplícalas siempre con estas reglas:

- **Añadido** (archivos nuevos): cópialos tal cual desde el repositorio, a la misma ruta. Si el archivo ya existiera con contenido distinto, párate y pregúntame.
- **Cambiado** (mapas y sistemas que ya tienes): edición **quirúrgica** — añade o sustituye solo las líneas o entradas que indica la migración. **Nunca sobrescribas el archivo entero**: puede llevar skills, sistemas o entradas de mapa que creaste tú. Si algo ya está aplicado, sáltalo. Si la frase que hay que cambiar no aparece tal cual (la edité yo, o está en otra forma), no fuerces la edición: enséñame el caso y decido.
- **Retirado**: retira solo lo nombrado explícitamente, y confírmamelo antes.
- **Migrado** (archivos que cambian de sitio o de forma): aplica la regla de transformación que declara la migración, elemento a elemento y de forma retomable — crea el destino, comprueba que quedó bien, y solo entonces retira el origen; lo ya migrado se salta. Con las skills, distingue: las del repositorio (las que lista la migración) se sustituyen por su versión nueva; para saber si yo edité alguna, usa el material que la migración adjunte (p. ej. los originales de la versión anterior) y compara — si mi copia difiere del original, la edité: enséñame la diferencia y elijo. Las mías (cualquier otra) se transforman con la regla, conservando el contenido íntegro; nunca se sustituyen por nada del repositorio.
- **Rutas movidas**: si una migración antigua cita una ruta que ya no existe en el repositorio porque una versión posterior la movió, sáltala: la migración que la movió la cubre.
- **Repo**: cambios que solo viven en el repositorio. No hay nada que aplicar en tu carpeta.
- **Marcador `AIOS/VERSION.md`**: no lo trates como un archivo más ni lo copies tal cual del repositorio — el del repo refleja siempre la última versión publicada, no la que estás aplicando. Lo fija este proceso, versión a versión (arriba). Si no existe, créalo con el mismo texto que el `AIOS/VERSION.md` del repositorio pero con la versión que acabas de completar.

### Reglas de seguridad (inviolables)

- **No toques nunca contenido del usuario**: `ME.md`, `projects/`, `areas/`, `knowledge/` ni `episodic/`. Son míos.
- **No borres** skills, entradas de mapa, sistemas ni archivos que una migración no nombre explícitamente como "Retirado". Actualizar solo añade y modifica lo indicado; nunca limpia por su cuenta. Migrar no es borrar: mover o transformar un archivo según una regla **Migrado** conserva su contenido íntegro — aun así, nada se migra sin mi OK.
- **Ante cualquier duda o conflicto** —un archivo "Cambiado" que ya habías tocado, un "Añadido" que ya existe con otro contenido— párate y pregúntame antes de escribir.
- Trabajos pesados o comparaciones largas, delégalos a un subagente; yo solo veo el resultado.

## Al terminar

- Comprueba que `AIOS/VERSION.md` quedó en la última versión aplicada (lo has ido creando/actualizando versión a versión).
- Enséñame un resumen: qué versiones apliqué y qué archivos cambié o creé.
- Si tenía skills instaladas como nativas en algún agente (vía skill-installer), recuérdame regenerarlas: sus punteros pueden haber quedado apuntando a rutas viejas (en Cowork, volver a subir el paquete por la interfaz).
- Sugiéreme pasar `skills-janitor` y `contenido-janitor` para verificar que mapas, skills y carpetas cuadran.

---

Reglas de esta sesión: español de España, tuteo. Soy un perfil no técnico: nada de rutas, JSON ni configuración a la vista — la fontanería es tuya, con confirmaciones simples ("¿aplico?"). Empieza cuando estés listo.

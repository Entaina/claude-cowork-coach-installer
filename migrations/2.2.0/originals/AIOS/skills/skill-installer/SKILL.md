---
name: skill-installer
description: >-
  Instala una skill del coach de forma nativa en el agente que la ejecuta
  —Cowork, Claude Code u otro— produciendo un wrapper delgado que el host
  descubre y dispara por sí solo. El wrapper solo lleva los metadatos de
  descubrimiento (name y description, que ya trae dentro las frases de
  disparo) más una instrucción en texto que, en tiempo de ejecución, lee y
  ejecuta el SKILL.md canónico de AIOS/skills/. Nunca duplica el workflow ni
  usa enlaces de sistema de archivos. La forma del wrapper la decide cada host
  —un archivo de skill, un paquete que el usuario sube por la UI, u otra cosa—
  y el agente ejecutor la determina por sí mismo, preguntando el scope cuando
  hay varios. Úsala para hacer nativas las skills del coach en cualquier
  agente sin mantenerlas en dos sitios. Se activa con frases como: "instala
  esta skill", "instala la skill", "instala todas las skills", "hazla nativa
  aquí", "haz nativa esta skill", "instala las skills en cowork", "instala
  las skills en claude code", "skill installer".
metadata:
  system: skills
  status: active
  created: "2026-07-16"
  updated: "2026-07-23"
---
# skill-installer

Proyecta una skill canónica del coach al agente donde estás corriendo — como skill nativa que el host descubre y dispara solo, sin duplicar el workflow.

`skill-builder` crea el canónico. `skill-installer` lo proyecta al host. El `SKILL.md` de `AIOS/skills/<name>/` sigue siendo la única fuente de verdad; el wrapper es desechable y regenerable.

## Cuándo usarla

- Al empezar a trabajar en un host nuevo (Cowork, Claude Code, un SDK, otro agente) y quieres que dispare las skills del coach sin depender de que lea `mapa-skills.md` cada vez.
- Cuando editas el canónico de una skill y quieres refrescar su `description` en el wrapper del host.
- "Instala esta skill" / "hazla nativa aquí" / "instala todas".

## Cuándo NO usarla

- Para **crear o editar** el workflow de una skill — eso es skill-builder. El installer nunca toca la lógica.
- Para **auditar** drift entre canónicos, `mapa-skills.md` y wrappers — eso es skills-janitor.
- Si el host ya descubre y dispara la skill de forma fiable. No añadas un wrapper redundante.

## El wrapper (léelo antes del workflow)

El wrapper es **delgado**: solo lleva los metadatos que el host necesita para descubrir y disparar la skill (`name` y `description` — que ya lleva dentro las frases de disparo) más una instrucción en texto — «lee el canónico y ejecútalo» — que el agente resuelve en tiempo de ejecución contra su carpeta de trabajo. El workflow no se copia jamás, y el wrapper **nunca** es un enlace de sistema de archivos (por eso funciona donde los symlinks fallan — carpetas montadas o sincronizadas).

**Qué forma toma el wrapper lo decide el host, no esta skill.** En unos agentes será un archivo de skill que tú, el agente, escribes en una ubicación nativa (p. ej. Claude Code). En otros será un paquete que el usuario instala por la UI (p. ej. Cowork). En otros, otra cosa. Corres dentro del host, así que sabes —o puedes verificar— cómo consume skills. No hay tabla de adaptadores que mantener: te adaptas al host en el que estás.

## Workflow

### 1. Resuelve el canónico

Localiza `AIOS/skills/<name>/SKILL.md`. Lee su frontmatter — `name`, `description` y `metadata` (`system`, `status`, `dependencies` si la hay). Si no existe o no está en `mapa-skills.md`, no instales a ciegas (ver Casos límite). Si su `metadata.status` es `draft`/`retired`, avisa antes de seguir.

Para "instala todas", itera sobre las skills activas de `mapa-skills.md`.

### 2. Identifica cómo consume skills tu host

Determina, para el agente en el que corres:

- **Cómo** se registran skills nativas — un archivo que el agente escribe, un paquete que el usuario sube por la UI, u otro mecanismo.
- **Dónde**, si aplica (directorio o ubicación nativa).
- **En qué formato** (p. ej. una carpeta `<name>/SKILL.md` con frontmatter `name` + `description` — el mismo formato del canónico; el wrapper lo comparte, pero sigue siendo un puntero, no una copia).
- **Qué límites** impone (longitud máxima de `description`, reglas de nombre).

Si lo conoces con certeza, sigue. Si no, verifícalo (config o docs del host) o pregunta al usuario. **Mejor preguntar que instalar en el sitio equivocado.** Si tu host no tiene mecanismo de skills nativas, ve a Casos límite → modo degradado.

### 3. Resuelve el scope

Si tu host ofrece **varios** scopes de instalación (p. ej. dentro del proyecto vs global de la máquina), **pregunta al usuario cuál** antes de materializar. No asumas un default. Si solo hay uno, úsalo.

### 4. Compón el wrapper delgado

- **Nombre/identificador**: el `name` del canónico, adaptado a las reglas de nombre del host.
- **Descripción**: usa la `description` del canónico — ya lleva dentro *qué hace*, *cuándo usarla* y las frases de disparo — recortada al límite del host. Recorta, no rompas el límite.
- **Cuerpo (puntero de runtime)**: solo la instrucción de ejecución, del tipo —
  > *La skill canónica vive en `<ruta-al-directorio-de-la-skill>/SKILL.md`. Léela completa y ejecútala al pie de la letra.*
  Mantén el cuerpo mínimo. Nada de meta-notas sobre no duplicar o regenerar — eso es regla del instalador, no contenido del wrapper.
- **Regla de ruta**: si el wrapper queda **dentro de la carpeta del coach** (scope de proyecto), apunta al canónico con una **ruta relativa a la raíz de la carpeta** — así viaja con ella y es portable entre máquinas. Si queda **fuera** (scope global de máquina), usa la **ruta absoluta de la carpeta del coach** tal como la ves ahora, y anótalo como específico de esa máquina.

### 5. Materializa el wrapper

Prodúcelo en la forma que el host consuma — escríbelo en su ubicación nativa si el agente puede hacerlo (p. ej. Claude Code), o empaquétalo y entrégaselo al usuario para que lo instale por la UI (p. ej. Cowork). No toques el canónico.

### 6. Verifica

Comprueba que el host **ahora descubre** la skill (relee el registro, usa el mecanismo de listado del host, o confírmalo con el usuario tras la instalación por UI). Reporta: qué skill, en qué forma y dónde quedó el wrapper, con qué descripción, y cómo dispararla. Si no aparece, dilo — no la declares instalada.

## Qué produce

Un wrapper nativo por el que el host descubre y dispara la skill por sí solo, apuntando al canónico de `AIOS/skills/<name>/SKILL.md` — sin copiar su workflow y sin symlinks.

## Reglas

- **El `SKILL.md` canónico de `AIOS/skills/<name>/` es la única fuente de verdad.** El wrapper nunca contiene el workflow.
- **El wrapper es delgado**: metadatos de descubrimiento + puntero de runtime. Nada más.
- **El puntero es texto que se resuelve en tiempo de ejecución. NUNCA un symlink ni enlace de sistema de archivos.**
- **Respeta los límites del host** (longitud de descripción, reglas de nombre). Recorta con criterio.
- **No inventes cómo carga skills tu host.** Si dudas, verifícalo o pregunta.
- **Sin default de scope.** Pregunta cuando hay varios.
- **Idempotente y no destructivo.** Reinstalar/actualizar un wrapper es seguro; borrar algo se pregunta.
- **No dupliques reglas del coach.** Refiérete a `ME.md` y a los mapas; no los repitas en el wrapper.

## Casos límite

- **Host sin skills nativas.** Modo degradado: registra el puntero a la skill en el archivo de contexto que ese host **sí** lee (su equivalente a `CLAUDE.md`/`AGENTS.md`/`GEMINI.md`), dejando claro que no es una skill nativa real. Tú, el agente, eliges la mejor aproximación para tu host.
- **Host con skills nativas pero cuyo registro no es escribible por el agente en sesión** (p. ej. Cowork y apps de escritorio, donde `.claude/` está protegido y las skills se cargan al arrancar). No es modo degradado, es el flujo normal del host — el usuario instala desde la UI. Emite el wrapper como carpeta `<name>/SKILL.md` (mismo formato que el canónico, cuerpo de puntero), empaquétala en un `.skill` (o ZIP) y entrégasela al usuario para instalarla (en Cowork, *Customize > Skills* → subir, o el botón *Save skill*). Empaquétala como plugin si hay que distribuir a varias personas.
- **La `description` del canónico supera el límite del host.** Resume conservando *qué hace* + *cuándo* + 2-3 frases de disparo.
- **La skill pedida no existe o no está en `mapa-skills.md`.** Dilo, no instales a ciegas. Sugiere skill-builder para crearla o registrarla.
- **Reinstalar / actualizar.** Re-deriva del canónico y sobreescribe el wrapper. No acumules copias.
- **Wrapper huérfano** (canónico borrado o con `metadata.status: retired`). Ofrece limpiarlo al reinstalar. La auditoría sistemática de drift es de skills-janitor.
- **Instalar la propia `skill-installer`.** Permitido — es una skill canónica más. Instálala como cualquier otra para que el host la dispare nativamente.

## Primer run, buena práctica

Córrela la primera vez que trabajes en un host nuevo, para proyectar las skills que usas a menudo. Re-córrela tras editar un canónico si quieres refrescar su wrapper — o deja que skills-janitor detecte el drift en su pasada de higiene. Y si una migración del coach mueve los canónicos de sitio, re-córrela sobre todas las skills instaladas: los punteros viejos no se actualizan solos.

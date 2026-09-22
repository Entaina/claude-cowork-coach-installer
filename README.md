# Tu asistente personal en Cowork o GPT local

Un asistente cuya memoria vive en archivos Markdown locales: el agente es reemplazable; tu contexto es tuyo.

Compatible con Claude Cowork y con ChatGPT Work / Codex en la app de escritorio, trabajando sobre una carpeta local. El acceso al historial y la automatización dependen de las herramientas que exponga tu app; el instalador comprueba esas capacidades. Antigravity y las modalidades web/cloud quedan pendientes.

## Instalación

1. Crea una carpeta nueva y **vacía** en tu ordenador (por ejemplo, `mi-coach`). No la muevas ni la renombres después.
2. Abre Cowork o ChatGPT Work / Codex en la app de escritorio y selecciona esa carpeta. En GPT elige **trabajar localmente**, sobre la carpeta permanente, sin crear un worktree.
3. Copia y pega este prompt en el chat:

```
Instala mi asistente personal en esta carpeta local permanente:

1. Copia toda la estructura del repositorio
   https://github.com/Entaina/claude-cowork-coach-installer en esta carpeta.
   No clones el repositorio (nada de git clone): descarga y copia los
   archivos, nada más. Todos los archivos y carpetas, tal cual, sin
   reescribirlos, reordenarlos ni "mejorarlos" — excepto README.md,
   INSTALL.md, UPDATE.md, CHANGELOG.md, las carpetas migrations/ y tests/ y cualquier
   archivo de git (.git, .gitkeep, .gitignore...), que no se copian. Las carpetas vacías del
   repo (projects/, areas/, knowledge/, episodic/logs/) créalas vacías. Si
   la carpeta no está vacía, párate y avísame antes de tocar nada.
2. Verifica que la copia está completa comparándola con el árbol del
   repositorio, y enséñame el resultado en una línea.
3. Lee INSTALL.md en el repositorio (sin copiarlo) y ejecútalo: empieza
   la entrevista de instalación y sigue sus pasos hasta el final.
```

4. Responde tres bloques breves: quién eres, cómo llamar al asistente y cómo te gusta trabajar. Una pregunta cada vez; di «siguiente» si alguna no aplica. No necesitas definir objetivos.
5. Comprueba tu primer log y responde a las propuestas, si las hay. Si faltan herramientas para automatizar, el instalador te indicará qué queda pendiente.

Si la entrevista se interrumpe, pide «retoma mi instalación leyendo INSTALL.md del repositorio». No vuelvas a copiar la estructura sobre la carpeta existente.

## El día a día

- Trabaja con tu coach con normalidad: prepara reuniones, piensa decisiones, pídele que pula tu trabajo ("pule esto", "¿qué se me escapa?").
- La revisión diaria aprende de ti y detecta proyectos y avances. Cowork conserva sus dos tareas; GPT local ejecuta ambas fases en una sola tarea para que terminen en orden. Configúrala solo en una app por carpeta y mantén el ordenador y la app abiertos.
- Revisa las propuestas y contesta sí o no. Los cambios duraderos requieren tu permiso; el registro diario y los Pendientes se actualizan directamente. El log indica si solo se pudo consultar parte del historial. No disponer del historial no significa que no hayas trabajado.

## Actualización

Cuando el repositorio incorpore mejoras (nuevas skills, sistemas afinados), pon tu coach al día sin perder nada tuyo:

1. Abre tu carpeta del coach en la app local (la misma de siempre).
2. Copia y pega este prompt en el chat:

```
Actualiza mi coach con los últimos cambios del repositorio, sin tocar nada mío:

1. Lee UPDATE.md del repositorio
   https://github.com/Entaina/claude-cowork-coach-installer (sin copiarlo) y
   ejecútalo al pie de la letra.
2. Mira la versión instalada (AIOS/VERSION.md, o 1.0.0 si no existe) frente al
   CHANGELOG.md del repositorio, enséñame en lenguaje llano qué versiones nuevas
   hay y qué aportan, y espera mi OK antes de aplicar nada.
3. Aplica solo los cambios que me falten, incluidas las migraciones de formato
   que declare el CHANGELOG, siempre con mi OK. No toques ME.md, projects/,
   areas/, knowledge/ ni episodic/, y no pierdas nada que yo haya creado. Al
   terminar, actualiza AIOS/VERSION.md y enséñame el resumen.
```

3. Revisa lo que te propone y confirma. Nada se aplica sin tu OK, y tu contenido (ME.md, proyectos, áreas, conocimiento, logs) nunca se toca.

## Qué hay en la carpeta

- `AGENTS.md` y `CLAUDE.md` — las mismas instrucciones completas de arranque, con ambos nombres para que cada app lea su archivo habitual. Se mantienen sincronizados.
- `AIOS/entornos-locales.md` — adaptación del historial y las tareas a cada app local.
- `ME.md` — quién eres y cómo trabajar contigo. Lo rellena la entrevista; es tuyo.
- `projects/` — tus proyectos: cosas con final, con estado (pending, working, done).
- `areas/` — tus áreas de responsabilidad: lo que no se acaba y hay que mantener bien.
- `knowledge/` — tu mundo: clientes, personas, equipo. Nace vacía y crece con tu firma.
- `episodic/logs/` — un log por día, escrito por el coach.
- `AIOS/` — mapas, plantillas, skills (un directorio por skill) y sistemas del coach. Crece vía skill-builder, también con tu firma.

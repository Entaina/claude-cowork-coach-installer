# Tu coach profesional en Claude Cowork

Un coach personal cuya memoria vive en archivos Markdown locales: el agente es reemplazable; tu contexto es tuyo.

## Instalación

1. Crea una carpeta nueva y **vacía** en tu ordenador (por ejemplo, `mi-coach`). No la muevas ni la renombres después.
2. Abre Claude Desktop, entra en Cowork y selecciona esa carpeta.
3. Copia y pega este prompt en el chat:

```
Instala mi coach personal en esta carpeta:

1. Copia toda la estructura del repositorio
   https://github.com/Entaina/claude-cowork-coach-installer en esta carpeta.
   No clones el repositorio (nada de git clone): descarga y copia los
   archivos, nada más. Todos los archivos y carpetas, tal cual, sin
   reescribirlos, reordenarlos ni "mejorarlos" — excepto README.md,
   INSTALL.md, UPDATE.md, CHANGELOG.md, la carpeta migrations/ y cualquier
   archivo de git (.git, .gitkeep, .gitignore...), que no se copian. Las carpetas vacías del
   repo (projects/, areas/, knowledge/, episodic/logs/) créalas vacías. Si
   la carpeta no está vacía, párate y avísame antes de tocar nada.
2. Verifica que la copia está completa comparándola con el árbol del
   repositorio, y enséñame el resultado en una línea.
3. Lee INSTALL.md en el repositorio (sin copiarlo) y ejecútalo: empieza
   la entrevista de instalación y sigue sus pasos hasta el final.
```

4. Responde la entrevista: una pregunta cada vez, ~10 minutos. Di "siguiente" si alguna no aplica.
5. Has terminado cuando veas tu primer log del día y respondas a su primera propuesta.

## El día a día

- Trabaja con tu coach con normalidad: prepara reuniones, piensa decisiones, pídele que pula tu trabajo ("pule esto", "¿qué se me escapa?").
- Cada noche, dos tareas automáticas repasan tu día: una aprende de ti ("he aprendido esto, ¿lo guardo?") y otra detecta proyectos nuevos y avances de los que ya tienes.
- Cada mañana, abre esas sesiones y contesta sí o no. Dos minutos. Nada entra en la memoria de tu coach sin tu permiso.

## Actualización

Cuando el repositorio incorpore mejoras (nuevas skills, sistemas afinados), pon tu coach al día sin perder nada tuyo:

1. Abre tu carpeta del coach en Cowork (la misma de siempre).
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

- `CLAUDE.md` — arranque del coach. No tocar.
- `ME.md` — quién eres y cómo trabajar contigo. Lo rellena la entrevista; es tuyo.
- `projects/` — tus proyectos: cosas con final, con estado (pending, working, done).
- `areas/` — tus áreas de responsabilidad: lo que no se acaba y hay que mantener bien.
- `knowledge/` — tu mundo: clientes, personas, equipo. Nace vacía y crece con tu firma.
- `episodic/logs/` — un log por día, escrito por el coach.
- `AIOS/` — mapas, plantillas, skills (un directorio por skill) y sistemas del coach. Crece vía skill-builder, también con tu firma.

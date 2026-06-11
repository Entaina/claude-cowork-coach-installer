# Tu coach profesional en Claude Cowork

Un coach personal cuya memoria vive en archivos Markdown locales: el agente es reemplazable; tu contexto es tuyo.

## Instalación

1. Crea una carpeta nueva y **vacía** en tu ordenador (por ejemplo, `mi-coach`). No la muevas ni la renombres después.
2. Abre Claude Desktop, entra en Cowork y selecciona esa carpeta.
3. Copia y pega este prompt en el chat:

```
Instala mi coach personal en esta carpeta:

1. Copia toda la estructura del repositorio
   https://github.com/Entaina/claude-cowork-coach-installer en esta carpeta:
   todos los archivos y carpetas, tal cual, sin reescribirlos, reordenarlos
   ni "mejorarlos" — excepto README.md e INSTALL.md, que no se copian.
   Si la carpeta no está vacía, párate y avísame antes de tocar nada.
2. Verifica que la copia está completa comparándola con el árbol del
   repositorio, y enséñame el resultado en una línea.
3. Lee INSTALL.md en el repositorio (sin copiarlo) y ejecútalo: empieza
   la entrevista de instalación y sigue sus pasos hasta el final.
```

4. Responde la entrevista: una pregunta cada vez, ~10 minutos. Di "siguiente" si alguna no aplica.
5. Has terminado cuando veas tu primer log del día y respondas a su primera propuesta.

## El día a día

- Trabaja con tu coach con normalidad: prepara reuniones, piensa decisiones, pídele que pula tu trabajo ("pule esto", "¿qué se me escapa?").
- Cada noche, una tarea automática repasa tu día y prepara propuestas: "he aprendido esto de ti, ¿lo guardo?".
- Cada mañana, abre esa sesión y contesta sí o no. Dos minutos. Nada entra en la memoria de tu coach sin tu permiso.

## Qué hay en la carpeta

- `CLAUDE.md` — arranque del coach. No tocar.
- `ME.md` — quién eres y cómo trabajar contigo. Lo rellena la entrevista; es tuyo.
- `knowledge/` — tu mundo: clientes, proyectos, equipo. Nace vacía y crece con tu firma.
- `episodic/logs/` — un log por día, escrito por el coach.
- `AIOS/` — mapas, skills y sistemas del coach. Crece vía skill-builder, también con tu firma.

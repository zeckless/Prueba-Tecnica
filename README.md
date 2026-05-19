# Prueba Técnica - Comunidad Docente IA

Prototipo base para el desafío del PDF: una plataforma navegable para docentes que están incorporando IA generativa en su práctica pedagógica.

## Stack

- Backend: Django + SQLite
- Frontend: React + Vite
- Módulos: panel general, biblioteca de prompts, repositorio de recursos y comunidad

## URLs locales

- Frontend: http://127.0.0.1:5173/
- API Django: http://127.0.0.1:8000/api/
- Healthcheck: http://127.0.0.1:8000/api/health/

## Comandos útiles

```bash
# Backend
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
cd backend
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py seed_demo
../.venv/bin/python manage.py runserver 127.0.0.1:8000 --noreload
```

```bash
# Frontend
cd frontend
npm install
npm run dev -- --port 5173
```

## Supuestos de diseño

- La biblioteca necesita curación editorial antes de publicar nuevos prompts.
- Los recursos institucionales deben convivir con guías internas de la comunidad.
- El espacio comunitario prioriza discusión y mejora de actividades antes que una red social completa.
- La siguiente iteración debería agregar autenticación, roles, versionado de prompts y moderación.

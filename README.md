# My Project Backend (Flask, MVC)

## Structure
- `app/models/`      Model: tables and DB queries
- `app/views/`       View: formats JSON responses
- `app/controllers/` Controller: request handling, calls model, returns view
- `app/routes/`      URL mapping only
- `app/utils/`       helpers, decorators, excel builders

## Setup
```bash
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # Linux/Mac: cp .env.example .env

set FLASK_APP=run.py           # Linux/Mac: export FLASK_APP=run.py
flask db init
flask db migrate -m "initial"
flask db upgrade

python run.py
```
Runs at http://localhost:5000  (health check: /health)

## API
| Method | URL | Auth |
|---|---|---|
| POST | /api/auth/register | no |
| POST | /api/auth/login | no |
| GET  | /api/users/me | Bearer token |

## Tests
```bash
pytest
```

## Production
```bash
gunicorn wsgi:app -b 0.0.0.0:8000 -w 4
```

## Adding a new module (example: rfq)
1. `app/models/rfq_model.py`
2. `app/views/rfq_view.py`
3. `app/controllers/rfq_controller.py`
4. `app/routes/rfq_routes.py`
5. register the blueprint in `app/routes/__init__.py`

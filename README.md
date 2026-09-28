# TeamBoard Backend

Runnable Django REST Framework + PostgreSQL implementation of the assignment.

## Endpoints
- `POST /api/auth/register/` — public; creates User, signal creates Company/API key, returns JWT.
- `POST /api/auth/login/` — public; `authenticate()` + fresh JWT.
- `POST /api/kb/query/` — JWT required; `Q(...__icontains)` search + atomic QueryLog.
- `GET /api/admin/usage-summary/` — JWT + Company `role=admin` required.

## Windows setup (PowerShell)
1. Install Python 3.11+ and Docker Desktop.
2. Extract this ZIP and open PowerShell in the extracted `teamboard_backend` folder.
3. Create env file: `Copy-Item .env.example .env`
4. Start PostgreSQL + PGAdmin: `docker compose up -d`
5. Create virtual environment: `py -m venv .venv`
6. Activate: `.\.venv\Scripts\Activate.ps1`
7. Install packages: `python -m pip install -r requirements.txt`
8. Apply migrations: `python manage.py migrate`
9. Seed KB: `python manage.py seed_kb`
10. Optional Django admin login: `python manage.py createsuperuser`
11. Start API: `python manage.py runserver`
12. API base URL: `http://127.0.0.1:8000/`

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` once in that terminal.

## macOS/Linux
`cp .env.example .env && docker compose up -d`
Then: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py seed_kb && python manage.py runserver`

## PGAdmin
Open `http://localhost:5050`, login `admin@teamboard.local` / `admin123`. Add server with host `db`, port `5432`, database/user/password from `.env`.

## Make a company Admin
The assignment specifically uses `Company.role`, not Django `is_staff/is_superuser`.
In PGAdmin run: `UPDATE api_company SET role='admin' WHERE user_id=(SELECT id FROM auth_user WHERE username='acmecorp');`
Then login again and use the new access token.

## Authorization
For protected endpoints send header: `Authorization: Bearer <access-token>`.
The assignment requires JWT for requests. `api_key` is generated/returned as a company credential but is not the authentication mechanism for these four endpoints.

## Run automated tests
`python manage.py test`

## Postman
Import `postman/TeamBoard.postman_collection.json`. It contains the 11 requested scenarios. Run Register first; successful register/login requests save tokens to collection variables automatically. For scenario 10, change the registered company's `role` to `admin`, run Admin Login, then Usage Summary - Admin token.

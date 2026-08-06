# Date-planlegger 💌

En liten Django-app der Linnea kan booke en date med deg, og du kan legge inn
datoer du ikke er tilgjengelig.

## Kjøre lokalt

```bash
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt

python manage.py migrate

# Opprett de to faste kontoene (sett dine egne passord!)
set HEINE_PASSWORD=dittpassord
set LINNEA_PASSWORD=linneaspassord
python manage.py create_users

python manage.py runserver
```

Åpne http://127.0.0.1:8000 og logg inn som `heine` eller `linnea`.

## Deploye til Render (gratis)

1. Push prosjektet til et nytt GitHub-repo (f.eks. `date-planlegger`)
2. Gå til [render.com](https://render.com) → **New** → **Web Service** → koble til repoet
3. Sett følgende:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn dateplanner.wsgi:application`
4. Legg til en gratis **PostgreSQL**-database i Render (New → PostgreSQL), og koble
   `DATABASE_URL` fra databasen til web-servicen under **Environment**
5. Legg til disse miljøvariablene under **Environment** på web-servicen:
   - `SECRET_KEY` → en lang, tilfeldig streng (generer f.eks. med `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
   - `DEBUG` → `False`
   - `ALLOWED_HOSTS` → navnet Render gir deg, f.eks. `date-planlegger.onrender.com`
   - `HEINE_PASSWORD` → passordet ditt
   - `LINNEA_PASSWORD` → Linneas passord
6. Deploy — `build.sh` kjører automatisk migrasjoner og oppretter de to kontoene

Etter dette er siden live på `https://ditt-app-navn.onrender.com`, og både du
og Linnea kan logge inn hver for dere.

## Struktur

- `booking/models.py` – `Unavailability` (dine blokkerte datoer) og `DateRequest` (Linneas forespørsler)
- `booking/views.py` – ruter til riktig dashbord ut fra hvem som er innlogget
- `booking/templates/booking/` – sidene (login, Heine-dashbord, Linnea-dashbord)
- `booking/management/commands/create_users.py` – oppretter/oppdaterer de to faste kontoene

## Endre passord senere

Kjør `python manage.py create_users` på nytt (lokalt eller via Render sitt shell)
med nye miljøvariabler — det overskriver eksisterende passord.

# eBioskop Portal

eBioskop je web portal namenjen prikazivačima i distributerima filmova, koji omogućava lakšu organizaciju rada i međusobnu komunikaciju, kao i pristup informacijama za krajnje korisnike.

## O Projektu

Portal je izrađen kao web aplikacija sa sledećim karakteristikama:
- Jezik interfejsa: Srpski
- Pismo: Latinica
- Pristup: Direktan link ili preko sajta www.cinemanetwork.rs

## Tehnički Stack

### Backend
- Programski jezik: Python
- Framework: Flask
- Baza podataka: MySQL

### Frontend
- HTML
- CSS 
- Dizajn: Figma

## Funkcionalnosti

### Grupe Korisnika

1. Administrativni pristup:
   - Administratori
   - Prikazivači
   - Distributeri

2. Korisnički pristup:
   - Korisnici sa proširenim pravima
   - Regularni korisnici

### Glavne Funkcionalnosti

#### Administrativni deo
- Upravljanje distributerima
- Upravljanje prikazivačima
- Upravljanje članovima MKPS
- Lista filmova
- Kalendar distribucije
- Praćenje projekcija

#### Korisnički deo
- Pregled prikazivača
- Pregled distributera
- Box office statistike
- FAQ sekcija
- Kontakt forma

## Instalacija

1. Klonirajte repozitorijum
```bash
git clone https://github.com/miiihaaas/eBioskop.git
```

2. Kreirajte virtuelno okruženje i aktivirajte ga
```bash
python -m venv venvBioskop
source venv/bin/activate  # Za Linux/Mac
venv\Scripts\activate     # Za Windows
```

3. Instalirajte potrebne pakete
```bash
pip install -r requirements.txt
```

4. Kreirajte .env fajl sa potrebnim konfiguracijama
```
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost/database_name
MAIL_SERVER=mail.server.com
MAIL_PORT=465
EMAIL_USER=your-email
EMAIL_PASS=your-password
```

5. Inicijalizujte bazu podataka
```bash
flask db upgrade
```

## Pokretanje Aplikacije

```bash
flask run
```

## Struktura Projekta

```
ebioskop/
├── README.md
├── requirements.txt
├── .env
├── run.py
├── ebioskop/
│   ├── __init__.py
│   ├── models.py
│   ├── calendar/
│   │   ├── forms.py
│   │   ├── functions.py
│   │   └── routes.py
│   ├── cinemas/
│   │   ├── forms.py
│   │   ├── functions.py
│   │   └── routes.py
│   ├── distributors/
│   │   ├── forms.py
│   │   ├── functions.py
│   │   └── routes.py
│   ├── main/
│   │   └── routes.py
│   ├── movies/
│   │   ├── forms.py
│   │   ├── functions.py
│   │   └── routes.py
│   ├── producers/
│   │   ├── forms.py
│   │   ├── functions.py
│   │   └── routes.py
│   ├── projections/
│   │   ├── forms.py
│   │   ├── functions.py
│   │   └── routes.py
│   ├── static/
│   │   ├── img/
│   │   └── mikicustom.css
│   ├── templates/
│   └── users/
│       ├── forms.py
│       ├── functions.py
│       └── routes.py
```

## Autori

Mihailo Panić, Miodrag Stojkovi, Studio Implicit

## Licenca

[Informacije o licenci]

## Kontakt

Za više informacija kontaktirajte: [office@studioimplicit.rs]
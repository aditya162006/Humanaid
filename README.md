# Humanaid 

**Connecting people with humanitarian crises and trusted donation resources.**

---

There's a lot of suffering in the world, and it can be hard to know where to help or who to trust. Humanaid is my attempt to make that a little easier — a platform where you can browse ongoing humanitarian crises and find verified organizations you can actually donate to.

Beyond just browsing, anyone can submit a crisis they think should be listed. Those submissions go through an admin review before anything goes live, so the data stays accurate and trustworthy.

---

## What it does

**Browse crises** — The homepage lists humanitarian crises with their country, category, and relevant context. Each one links out to donation resources from organizations like UNHCR, UNICEF, and the Red Cross.

**Submit a crisis** — If you know of a situation that isn't listed, you can submit it. You can include the crisis title, country, category, and as many donation links as you want. Your submission goes into a review queue rather than immediately going live.

**Admin dashboard** — There's a password-protected admin panel where I (or any admin) can add, edit, and remove crises, and review pending submissions — accepting, editing, or rejecting them before they reach the public.

---

## Tech stack

- **Backend:** Python, Flask, SQLAlchemy, Werkzeug
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Database:** SQLite / Turso
- **Other:** Flask sessions, python-dotenv, GitHub Codespaces

---

## Project structure

```
Humanaid/
│
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── .env
├── .gitignore
│
├── static/
│   ├── css/style.css
│   └── js/script.js
│
└── templates/
    ├── layout.html
    ├── home.html
    ├── login.html
    ├── apology.html
    ├── admin.html
    ├── admin_add_entry.html
    ├── admin_edit_entry.html
    ├── admin_remove_entry.html
    ├── admin_review.html
    └── submit.html
```

---

## Database

The database is split into four tables:

- **crises** — approved crises with title, country, category, and a search query
- **donation_links** — donation URLs tied to a crisis (one crisis → many links)
- **submissions** — user-submitted crises waiting for review
- **submission_links** — donation URLs attached to a submission

Keeping submissions separate from live crisis data was an intentional design choice — users can contribute without being able to directly modify what's on the public site.

---

## How the submission flow works

```
User submits a crisis
        ↓
  Goes into review queue
        ↓
  Admin reviews it
   ↙    ↓    ↘
Accept  Edit  Reject
  ↓      ↓      ↓
Goes   Update  Delete
live
```

Simple, but it keeps the data clean.

---

## Security

Nothing production-grade, but the basics are covered:

- Passwords are hashed (not stored in plaintext)
- Admin credentials live in environment variables
- Admin routes require an active session
- Sensitive config is kept out of version control
- Database-modifying actions use POST requests
- Cache-control headers are set on admin pages

---

## Running it locally

```bash
# Clone the repo
git clone https://github.com/aditya162006/Humanaid.git
cd Humanaid

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
SECRET_KEY=your-secret-key
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD_HASH=your-password-hash

# Run it
python app.py
```

Visit `http://localhost:5000`.

---

## API

There's a simple endpoint if you want the crisis and donation data as JSON:

```
GET /api/donations
```

Returns a list of crises with their associated donation links.

---

## What I want to add eventually

- Search and filtering on the homepage
- A map view so you can explore crises geographically
- Real-time news aggregation
- Crisis severity
- Email notifications for submission status
- An analytics dashboard for admins
- Any Suggestions from your end is highly appreciated
---

## About

Built by **Aditya Mishra**, B.Tech Electrical Engineering, Delhi Technological University.

This started as a CS50 final project and turned into something I actually want to keep building.

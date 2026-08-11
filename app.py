#inside the module "flask" import the class "Flask"
from flask import Flask, render_template, jsonify,request,redirect, render_template,url_for, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from database import engine
from models import Crisis, DonationLink

import os
from dotenv import load_dotenv
load_dotenv()
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/api/donations")
def list_donations():
    with Session(engine) as db_session:
        crises = db_session.query(Crisis).all()
        data = [
            {
                "id": crisis.slang,
                "title": crisis.title,
                "country": crisis.country,
                "category": crisis.category,
                "search_query": crisis.search_query,
                "link": [
                    {"title": link.organization, "url": link.url}
                    for link in crisis.donation_links
                ]
            }
            for crisis in crises
        ]
    return jsonify(data)

@app.route("/")
def home():
    with Session(engine) as db_session:
        stmt = select(Crisis).options(selectinload(Crisis.donation_links))
        crises = db_session.scalars(stmt).all()
    return render_template(
        "home.html",
        crises=crises)

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

@app.route("/login", methods=["POST","GET"])
def login_admin():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        entered_password = request.form.get("password")
        entered_username = request.form.get("username")
        print(entered_password)
        print(entered_username)
        if check_password_hash(ADMIN_PASSWORD_HASH, entered_password) and entered_username == ADMIN_USERNAME:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        else:
            return apology("Invalid credentials.")
    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if not session.get("is_admin"):
        return redirect(url_for("login_admin"))
    return render_template("admin.html")

# Add Entry Route
@app.route('/admin/add_entry', methods=['GET', 'POST'])
def add_entry():
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))
    if request.method == 'POST':
        slang = request.form.get("slang")
        title = request.form.get("title")
        country = request.form.get("country")
        category = request.form.get("category")
        search_query = request.form.get("search_query")
        linkcount= request.form.get("linkcount")

        if not linkcount:
            return apology("Invalid link count")

        linkcount = int(linkcount)
        link_titles = request.form.getlist("link_titles[]")
        link_urls = request.form.getlist("link_urls[]")

        if linkcount != len(link_titles) or linkcount != len(link_urls):
            return apology("Invalid donation link data")

        with Session(engine) as db_session:
            CRISIS = Crisis(slang=slang, title=title, country=country,category=category,search_query=search_query)
            db_session.add(CRISIS)
            db_session.flush()
            crisis_id = CRISIS.id

            for i in range(0,linkcount):
                organization = link_titles[i]
                url = link_urls[i]
                DONATIONLINK = DonationLink(crisis_id=crisis_id, organization=organization, url=url)
                db_session.add(DONATIONLINK)
            db_session.commit()
        return redirect(url_for("admin_panel"))
    return render_template("admin_add_entry.html")

# Edit Entry Route
@app.route('/admin/edit_entry', methods=['GET', 'POST'])
def edit_entry():
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    with Session(engine) as db_session:
        entries = db_session.query(Crisis).all()

        if request.method == 'POST':
            crisis_id = int(request.form.get("crisis_id"))
            # Find the matching crisis object
            crisis = next((e for e in entries if e.id == crisis_id), None)
            if not crisis:
                return apology("Crisis Not Found")
            # Pass the actual crisis object, not just the id
            return render_template("admin_edit_entry.html", Entry=entries, crisis=crisis)

    # GET request — no crisis selected yet, so don't pass crisis at all
    return render_template("admin_edit_entry.html", Entry=entries)

@app.route('/admin/update_field/<int:crisis_id>', methods=['POST'])
def update_field(crisis_id):
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    field_name = request.form.get("field_name")
    field_value = request.form.get("field_value")

    with Session(engine) as db_session:
        # 1. Fetch the crisis record by ID
        crisis = db_session.query(Crisis).get(crisis_id)

        if crisis:
            # 2. Directly update whichever field was edited
            if field_name == 'title':
                crisis.title = field_value
            elif field_name == 'country':
                crisis.country = field_value
            elif field_name == 'category':
                crisis.category = field_value
            elif field_name == 'search_query':
                crisis.search_query = field_value

            # 3. Save changes to Turso / Database
            db_session.commit()
            flash("Field updated successfully!", "success")
        else:
            flash("Crisis record not found.", "error")

    # 4. Reload the page showing the updated crisis record
    return redirect(url_for("edit_entry"))
    


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_admin"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)



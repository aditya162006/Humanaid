#inside the module "flask" import the class "Flask"
from flask import Flask, render_template, jsonify,request,redirect,url_for, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from database import engine
from models import Crisis, DonationLink, Submission, SubmissionLink
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
load_dotenv()
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("FATAL: SECRET_KEY is not set in environment!")
if not ADMIN_PASSWORD_HASH or not ADMIN_USERNAME:
    raise RuntimeError("FATAL: Admin credentials not configured!")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True   # blocks JS access to cookie
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # partial CSRF protection
app.config["SESSION_COOKIE_SECURE"] = os.getenv("FLASK_ENV") == "production"     # HTTPS only (enable in prod)
csrf = CSRFProtect(app)
limiter = Limiter(key_func=get_remote_address,app=app)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/api/donations")
def list_donations():
    with Session(engine) as db_session:
        stmt = select(Crisis).options(selectinload(Crisis.donation_links))
        crises = db_session.scalars(stmt).all()
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
@limiter.limit("10 per minute")
def login_admin():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        entered_password = request.form.get("password")
        entered_username = request.form.get("username")
        if check_password_hash(ADMIN_PASSWORD_HASH, entered_password) and entered_username == ADMIN_USERNAME:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        else:
            return apology("Invalid credentials.")
    return render_template("login.html")

@app.route("/submit", methods=["GET","POST"])
#Add submission to local database
def submit_panel():
    if request.method == 'POST':
        slang = request.form.get("slang")
        title = request.form.get("title")
        country = request.form.get("country")
        category = request.form.get("category")
        search_query = request.form.get("search_query")
        linkcount= request.form.get("linkcount")

        if not linkcount:
            return apology("Invalid link count")
        try:
            linkcount = int(linkcount)
        except ValueError:
            return apology("Invalid entry ID", 400)
        link_titles = request.form.getlist("link_titles[]")
        link_urls = request.form.getlist("link_urls[]")

        if linkcount != len(link_titles) or linkcount != len(link_urls):
            return apology("Invalid donation link data")

        with Session(engine) as db_session:
            SUBMISSION = Submission(slang=slang, title=title, country=country,category=category,search_query=search_query)
            db_session.add(SUBMISSION)
            db_session.flush()
            submissions_id = SUBMISSION.id

            for i in range(0,linkcount):
                organization = link_titles[i]
                url = link_urls[i]
                SUBMISSIONLINK = SubmissionLink(submission_id=submissions_id, organization=organization, url=url)
                db_session.add(SUBMISSIONLINK)
            db_session.commit()
        return redirect(url_for("home"))
    return render_template("submit.html")

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
        try:
            linkcount = int(linkcount)
        except ValueError:
            return apology("Invalid entry ID", 400)
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

# 1. Review Selector Route
@app.route('/admin/review_submission', methods=['GET', 'POST'])
def review_entry():
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    with Session(engine) as db_session:
        submissions_entry = db_session.query(Submission).all()
        submission = None

        submission_id = request.form.get("submission_id") or request.args.get("submission_id")
        if submission_id:
            try:
                submission_id = int(submission_id)
                submission = db_session.query(Submission).get(submission_id)
            except ValueError:
                return apology("Invalid entry ID", 400)

        return render_template("admin_review.html", submission_entry=submissions_entry, submission=submission)


# 1. Accept Submission (Reads the current/edited form values directly)
@app.route('/admin/review/accept/<int:submission_id>', methods=['POST'])
def accept_submission(submission_id):
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    with Session(engine) as db_session:
        submission = db_session.query(Submission).get(submission_id)
        if not submission:
            flash("Submission not found.", "error")
            return redirect(url_for("review_entry"))

        # Read the latest values submitted in the form payload
        slang = request.form.get("slang") or submission.slang
        title = request.form.get("title") or submission.title
        country = request.form.get("country") or submission.country
        category = request.form.get("category") or submission.category
        search_query = request.form.get("search_query") or submission.search_query

        # Create new Crisis record with updated data
        crisis = Crisis(
            slang=slang,
            title=title,
            country=country,
            category=category,
            search_query=search_query
        )
        db_session.add(crisis)
        db_session.flush()

        # Read the latest link inputs from the form payload
        link_titles = request.form.getlist("link_titles[]")
        link_urls = request.form.getlist("link_urls[]")

        if link_titles and link_urls:
            for org, url in zip(link_titles, link_urls):
                if org.strip() and url.strip():
                    donation_link = DonationLink(
                        organization=org.strip(),
                        url=url.strip(),
                        crisis_id=crisis.id
                    )
                    db_session.add(donation_link)
        else:
            # Fallback to existing links if form didn't provide any
            for link in submission.submission_links:
                donation_link = DonationLink(
                    organization=link.organization,
                    url=link.url,
                    crisis_id=crisis.id
                )
                db_session.add(donation_link)

        # Remove the pending submission from the temporary table
        db_session.delete(submission)
        db_session.commit()

        flash(f"Submission '{title}' approved and published successfully!", "success")
        return redirect(url_for("review_entry"))


# 2. Save Edited Submission (Updates the submission table without accepting yet)
@app.route('/admin/review/edit/<int:submission_id>', methods=['POST'])
def edit_submission(submission_id):
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    with Session(engine) as db_session:
        submission = db_session.query(Submission).get(submission_id)
        if not submission:
            flash("Submission not found.", "error")
            return redirect(url_for("review_entry"))

        # Update core fields from form
        submission.slang = request.form.get("slang")
        submission.title = request.form.get("title")
        submission.country = request.form.get("country")
        submission.category = request.form.get("category")
        submission.search_query = request.form.get("search_query")

        # Update link fields from form
        link_titles = request.form.getlist("link_titles[]")
        link_urls = request.form.getlist("link_urls[]")

        for link_obj, org_title, org_url in zip(submission.submission_links, link_titles, link_urls):
            link_obj.organization = org_title.strip()
            link_obj.url = org_url.strip()

        db_session.commit()
        flash("Submission details updated successfully!", "success")

        return redirect(url_for("review_entry", submission_id=submission_id))

# 4. Reject Submission -> Deletes from Database
@app.route('/admin/review/reject/<int:submission_id>', methods=['POST'])
def reject_submission(submission_id):
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    with Session(engine) as db_session:
        submission = db_session.query(Submission).get(submission_id)
        if submission:
            db_session.delete(submission)
            db_session.commit()
            flash("Submission rejected and removed.", "success")
        else:
            flash("Submission not found.", "error")

        return redirect(url_for("admin_panel"))

# Edit Entry Route
@app.route('/admin/edit_entry', methods=['GET', 'POST'])
def edit_entry():
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    with Session(engine) as db_session:
        entries = db_session.query(Crisis).all()

        if request.method == 'POST':
            try:
                crisis_id = int(request.form.get("crisis_id"))
            except ValueError:
                return apology("Invalid entry ID", 400)
            # Find the matching crisis object
            crisis = next((e for e in entries if e.id == crisis_id), None)
            if not crisis:
                return apology("Crisis Not Found")
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
        crisis = db_session.get(Crisis, crisis_id)

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

@app.route('/admin/manage_link', methods=['POST'])
def manage_link():
    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))

    action = request.form.get("action")  # "update", "delete", or "add"
    try:
        crisis_id = int(request.form.get("crisis_id", ""))
    except (ValueError, TypeError):
        return apology("Invalid crisis ID", 400)

    with Session(engine) as db_session:
        if action == "add":
            link = DonationLink(
                crisis_id=int(crisis_id),
                organization=request.form.get("organization"),
                url=request.form.get("url")
            )
            db_session.add(link)
            flash("Link added!", "success")

        elif action == "update":
            link = db_session.query(DonationLink).get(int(request.form.get("link_id")))
            if link:
                link.organization = request.form.get("organization")
                link.url = request.form.get("url")
                flash("Link updated!", "success")

        elif action == "delete":
            link = db_session.query(DonationLink).get(int(request.form.get("link_id")))
            if link:
                db_session.delete(link)
                flash("Link deleted!", "success")

        db_session.commit()

    return redirect(url_for("edit_entry", crisis_id=crisis_id))

@app.route('/admin/remove_entry', methods=['GET', 'POST'])
def remove_entry():

    if not session.get('is_admin'):
        return redirect(url_for("login_admin"))
    if request.method == "POST":
        entry_id = request.form.get("entry_id")
        if not entry_id:
            flash("Please select a crisis to delete.", "error")
            return redirect(url_for("remove_entry"))
        try:
            crisis_id = int(entry_id)
        except ValueError:
            return apology("Invalid entry ID", 400)
        with Session(engine) as db_session:
            crisis = db_session.get(Crisis, crisis_id)
            if crisis is None:
                return apology("Crisis not found")
            db_session.delete(crisis)
            db_session.commit()
        flash("Crisis removed successfully.", "success")
        return redirect(url_for("admin_panel"))

    with Session(engine) as db_session:
        entries = db_session.query(Crisis).all()
    return render_template("admin_remove_entry.html", Entry=entries)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_admin"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")


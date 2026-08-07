#inside the module "flask" import the class "Flask"
from flask import Flask, render_template, jsonify,request,redirect, render_template,url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DONATIONS = [
    {
        "id": "sudan",
        "title": "Sudan Humanitarian Crisis",
        "country": "Sudan",
        "category": "Conflict",
        "search_query": "Sudan humanitarian crisis",
        "links": [
            {
                "title": "UNHCR Sudan Emergency Appeal",
                "url": "https://donate.unhcr.org/int/en/sudan-emergency"
            },
            {
                "title": "IRC Sudan Crisis Response",
                "url": "https://www.rescue.org/country/sudan"
            }
        ]
    },
    {
        "id": "afghanistan",
        "title": "Afghanistan Hunger & Child Relief",
        "country": "Afghanistan",
        "category": "Hunger",
        "search_query": "Afghanistan humanitarian crisis",
        "links": [
            {
                "title": "UNHCR Afghanistan Emergency Appeal",
                "url": "https://donate.unhcr.org/in/en-in/afghanistan-situation"
            },
            {
                "title": "UN Crisis Relief - Afghanistan",
                "url": "https://www.unocha.org/we-fund"
            }
        ]
    },
    {
        "id": "gaza",
        "title": "Gaza Emergency Relief",
        "country": "Palestine",
        "category": "Conflict",
        "search_query": "Gaza humanitarian crisis",
        "links": [
            {
                "title": "Palestine Children's Relief Fund (PCRF)",
                "url": "https://www.pcrf.net/"
            },
            {
                "title": "British Red Cross Gaza Crisis Appeal",
                "url": "https://donate.redcross.org.uk/appeal/gaza-crisis-appeal"
            }
        ]
    },
    {
        "id": "ukraine",
        "title": "Ukraine Humanitarian Aid",
        "country": "Ukraine",
        "category": "Conflict",
        "search_query": "Ukraine humanitarian crisis",
        "links": [
            {
                "title": "UNITED24 Official Platform",
                "url": "https://u24.gov.ua/"
            },
            {
                "title": "ICRC Ukraine Crisis Donation",
                "url": "https://www.icrc.org/en/where-we-work/europe-central-asia/ukraine"
            }
        ]
    },
    {
        "id": "yemen",
        "title": "Yemen Hunger Crisis",
        "country": "Yemen",
        "category": "Hunger",
        "search_query": "Yemen humanitarian crisis",
        "links": [
            {
                "title": "World Food Programme Yemen Appeal",
                "url": "https://www.wfp.org/emergencies/yemen-emergency"
            },
            {
                "title": "UN Yemen Humanitarian Fund",
                "url": "https://www.unocha.org/yemen-humanitarian-fund"
            }
        ]
    },
    {
        "id": "south-sudan",
        "title": "South Sudan Emergency Relief",
        "country": "South Sudan",
        "category": "Conflict",
        "search_query": "South Sudan humanitarian crisis",
        "links": [
            {
                "title": "UNHCR South Sudan Emergency",
                "url": "https://donate.unhcr.org/in/en-in/south-sudan-emergency"
            },
            {
                "title": "UNICEF South Sudan Crisis Appeal",
                "url": "https://www.unicef.org/emergencies/south-sudan-crisis"
            }
        ]
    }
]
@app.route("/")
def hello_world():
    return render_template("home.html", donations=DONATIONS)

@app.route("/api/donations")
def list_donations():
    return jsonify(DONATIONS)

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

@app.route("/login", methods=["POST"])
def login_admin():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("possword"):
            return apology("must provide password")
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)



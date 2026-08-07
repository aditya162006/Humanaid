#inside the module "flask" import the class "Flask"
from flask import Flask, render_template, jsonify,request,redirect, render_template

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

app.secret_key = 'your_super_secret_admin_key'

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check against admin credentials
        if username == "admin" and password == "admin123":
            return redirect(url_for('home'))  # Route to admin dashboard
        else:
            flash("Authentication failed: Invalid admin credentials.")

    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)



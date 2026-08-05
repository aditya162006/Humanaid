#inside the module "flask" import the class "Flask"
from flask import Flask, render_template, jsonify

app = Flask(__name__)
DONATIONS = [
    {
        'title': "Sudan Humanitarian Crisis",
        'link_1': {
            'title': "UNHCR Sudan Emergency Appeal",
            'url': "https://donate.unhcr.org/int/en/sudan-emergency"
        },
        'link_2': {
            'title': "IRC Sudan Crisis Response",
            'url': "https://www.rescue.org/country/sudan"
        }
    },
    {
        'title': "Afghanistan Hunger & Child Relief",
        'link_1': {
            'title': "UNHCR Afghanistan Emergency Appeal",
            'url': "https://donate.unhcr.org/in/en-in/afghanistan-situation"
        },
        'link_2': {
            'title': "UN Crisis Relief - Afghanistan",
            'url': "https://www.unocha.org/we-fund"
        }
    },
    {
        'title': "Gaza Emergency Relief",
        'link_1': {
            'title': "Palestine Children's Relief Fund (PCRF)",
            'url': "https://www.pcrf.net/"
        },
        'link_2': {
            'title': "British Red Cross Gaza Crisis Appeal",
            'url': "https://donate.redcross.org.uk/appeal/gaza-crisis-appeal"
        }
    },
    {
        'title': "Ukraine Humanitarian Aid",
        'link_1': {
            'title': "UNITED24 Official Platform",
            'url': "https://u24.gov.ua/"
        },
        'link_2': {
            'title': "ICRC Ukraine Crisis Donation",
            'url': "https://www.icrc.org/en/where-we-work/europe-central-asia/ukraine"
        }
    },
    {
        'title': "Yemen Hunger Crisis",
        'link_1': {
            'title': "World Food Programme Yemen Appeal",
            'url': "https://www.wfp.org/emergencies/yemen-emergency"
        },
        'link_2': {
            'title': "UN Yemen Humanitarian Fund",
            'url': "https://www.unocha.org/yemen-humanitarian-fund"
        }
    },
    {
        'title': "South Sudan Emergency Relief",
        'link_1': {
            'title': "UNHCR South Sudan Emergency",
            'url': "https://donate.unhcr.org/in/en-in/south-sudan-emergency"
        },
        'link_2': {
            'title': "UNICEF South Sudan Crisis Appeal",
            'url': "https://www.unicef.org/emergencies/south-sudan-crisis"
        }
    }
]
@app.route("/")
def hello_world():
    return render_template("home.html", donations=DONATIONS)

@app.route("/api/donations")
def list_donations():
    return jsonify(DONATIONS)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

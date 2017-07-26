import json
from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

sample_race_data = [{'office':'Governor','blurb':'','map-id':''}, {'office':'Attorney General','blurb':'','map-id':''}, {'office':'Secretary of State','blurb':'','map-id':''}, {'office':'State Auditor','blurb':'','map-id':''}, {'office':'Senate','blurb':'','map-id':''}, {'office':'Congressional District 1','blurb':'','map-id':''}, {'office':'Congressional District 2','blurb':'','map-id':''}, {'office':'Congressional District 3','blurb':'','map-id':''}, {'office':'Congressional District 4','blurb':'','map-id':''}, {'office':'Congressional District 5','blurb':'','map-id':''}, {'office':'Congressional District 6','blurb':'','map-id':''}, {'office':'Congressional District 7','blurb':'','map-id':''}, {'office':'Congressional District 8','blurb':'','map-id':''}]

sample_candidate_data = [{'drop-out-date': '', 'blurb': 'Jim Hagedorn, a former US Treasury official and conservative blogger from Blue Earth, is seeking the Republican endorsement in CD1. This is his third run for the seat; he lost to Rep. Tim Walz in 2014 and 2016.', 'endorsed?': 'No', 'incumbent?': 'No', 'date-declared': '', 'name': 'Jim Hagedorn', 'office-sought': 'Congressional District 1', 'party': 'Republican', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': 'Dan Feehan, an Iraq War veteran and a former official at the Department of Defense under Barack Obama, is seeking the DFL endorsement in CD1. Originally from Red Wing, Feehan moved back to the Mankato area this year.', 'endorsed?': 'No', 'incumbent?': 'No', 'date-declared': '7/10/17', 'name': 'Dan Feehan', 'office-sought': 'Congressional District 1', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'Yes', 'date-declared': '', 'name': 'Jason Lewis', 'office-sought': 'Congressional District 2', 'party': 'Republican', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'No', 'date-declared': '7/17/17', 'name': 'Angie Craig', 'office-sought': 'Congressional District 2', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'No', 'date-declared': '5/24/17', 'name': 'Jeff Erdmann', 'office-sought': 'Congressional District 2', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'Yes', 'date-declared': '', 'name': 'Erik Paulsen', 'office-sought': 'Congressional District 3', 'party': 'Republican', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'No', 'date-declared': '5/16/17', 'name': 'Dean Phillips ', 'office-sought': 'Congressional District 3', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'No', 'date-declared': '', 'name': 'Brian Santamaria', 'office-sought': 'Congressional District 3', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': '', 'incumbent?': 'Yes', 'date-declared': '', 'name': 'Betty McCollum', 'office-sought': 'Congressional District 4', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': '', 'incumbent?': 'Yes', 'date-declared': '', 'name': 'Keith Ellison', 'office-sought': 'Congressional District 5', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': '', 'incumbent?': '', 'date-declared': '', 'name': '', 'office-sought': '', 'party': '', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'Yes', 'date-declared': '', 'name': 'Rick Nolan', 'office-sought': 'Congressional District 8', 'party': 'DFL', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'No', 'date-declared': '7/10/17', 'name': 'Pete Stauber', 'office-sought': 'Congressional District 8', 'party': 'Republican', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': '', 'incumbent?': '', 'date-declared': '', 'name': '', 'office-sought': '', 'party': '', 'headshot-url': ''}, {'drop-out-date': '', 'blurb': '', 'endorsed?': 'No', 'incumbent?': 'Yes', 'date-declared': '', 'name': 'Amy Klobuchar', 'office-sought': 'Senate', 'party': 'DFL', 'headshot-url': ''}]


def load_data_from_gsheet(wksheet):
    ##Google Sheets oauth2
    json_key = json.load(open('credentials/minnpost-whos-running-2018-d0732d1089c9.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scopes=scope)

    gc = gspread.authorize(credentials)
    sht = gc.open("Who's running 2018")
    wks = sht.worksheet(wksheet)

    return wks.get_all_records()

def formatted_data():
    races = sample_race_data #load_data_from_gsheet("Races")
    candidate_data = sample_candidate_data #load_data_from_gsheet("Candidates")

    for race in races:
        race["candidates"] = {}
        for candidate in candidate_data:
            candidate_id = candidate["name"].replace(" ", "").lower()
            candidate["candidate_id"] = candidate_id
            if candidate["office-sought"] == race["office"]:
                if candidate["party"] in race["candidates"]:
                    race["candidates"][candidate["party"]].append(candidate)
                else:
                    race["candidates"][candidate["party"]] = [candidate]
    return races

@app.route("/")
def index():
    return render_template("index.html", data=formatted_data())


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    #print(formatted_data())
    #print(load_data_from_gsheet("Candidates"))

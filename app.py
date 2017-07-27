import json
from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

sample_race_data = [{'office':'Governor','blurb':'','map-id':''}, {'office':'Attorney General','blurb':'','map-id':''}, {'office':'Secretary of State','blurb':'','map-id':''}, {'office':'State Auditor','blurb':'','map-id':''}, {'office':'Senate','blurb':'','map-id':''}, {'office':'Congressional District 1','blurb':'','map-id':''}, {'office':'Congressional District 2','blurb':'','map-id':''}, {'office':'Congressional District 3','blurb':'','map-id':''}, {'office':'Congressional District 4','blurb':'','map-id':''}, {'office':'Congressional District 5','blurb':'','map-id':''}, {'office':'Congressional District 6','blurb':'','map-id':''}, {'office':'Congressional District 7','blurb':'','map-id':''}, {'office':'Congressional District 8','blurb':'','map-id':''}]

sample_candidate_data = [{'blurb': 'Jim Hagedorn, a former US Treasury official and conservative blogger from Blue Earth, is seeking the Republican endorsement in CD1. This is his third run for the seat; he lost to Rep. Tim Walz in 2014 and 2016.', 'incumbent?': 'No', 'name': 'Jim Hagedorn', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Congressional District 1'}, {'blurb': 'Dan Feehan, an Iraq War veteran and a former official at the Department of Defense under Barack Obama, is seeking the DFL endorsement in CD1. Originally from Red Wing, Feehan moved back to the Mankato area this year.', 'incumbent?': 'No', 'name': 'Dan Feehan', 'party': 'DFL', 'headshot-url': 'https://s3.amazonaws.com/data.minnpost/projects/minnpost-whos-running-2018/candidate-photos/dan-feehan-head_150.jpg', 'endorsed?': 'No', 'date-declared': '7/10/17', 'drop-out-date': '', 'office-sought': 'Congressional District 1'}, {'blurb': '', 'incumbent?': 'Yes', 'name': 'Jason Lewis', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Congressional District 2'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Angie Craig', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '7/17/17', 'drop-out-date': '', 'office-sought': 'Congressional District 2'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Jeff Erdmann', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '5/24/17', 'drop-out-date': '', 'office-sought': 'Congressional District 2'}, {'blurb': '', 'incumbent?': 'Yes', 'name': 'Erik Paulsen', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Congressional District 3'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Dean Phillips ', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '5/16/17', 'drop-out-date': '', 'office-sought': 'Congressional District 3'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Brian Santamaria', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Congressional District 3'}, {'blurb': '', 'incumbent?': 'Yes', 'name': 'Betty McCollum', 'party': 'DFL', 'headshot-url': '', 'endorsed?': '', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Congressional District 4'}, {'blurb': '', 'incumbent?': 'Yes', 'name': 'Keith Ellison', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'Yes', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Congressional District 5'}, {'blurb': '', 'incumbent?': '', 'name': '', 'party': '', 'headshot-url': '', 'endorsed?': '', 'date-declared': '', 'drop-out-date': '', 'office-sought': ''}, {'blurb': '', 'incumbent?': 'Yes', 'name': 'Rick Nolan', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Congressional District 8'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Pete Stauber', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '7/10/17', 'drop-out-date': '', 'office-sought': 'Congressional District 8'}, {'blurb': '', 'incumbent?': '', 'name': '', 'party': '', 'headshot-url': '', 'endorsed?': '', 'date-declared': '', 'drop-out-date': '', 'office-sought': ''}, {'blurb': '', 'incumbent?': 'Yes', 'name': 'Amy Klobuchar', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No', 'date-declared': '', 'drop-out-date': '', 'office-sought': 'Senate'}, {'blurb': '', 'incumbent?': '', 'name': '', 'party': '', 'headshot-url': '', 'endorsed?': '', 'date-declared': '', 'drop-out-date': '', 'office-sought': ''}, {'blurb': '', 'incumbent?': '', 'name': '', 'party': '', 'headshot-url': '', 'endorsed?': '', 'date-declared': '', 'drop-out-date': '', 'office-sought': ''}, {'blurb': '', 'incumbent?': 'No', 'name': 'Tim Walz', 'party': 'DFL', 'headshot-url': 'https://s3.amazonaws.com/data.minnpost/projects/minnpost-whos-running-2018/candidate-photos/tim-walz-head_150.jpg', 'endorsed?': 'No ', 'date-declared': '3/27/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Rebecca Otto', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '1/9/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Erin Murphy', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '12/13/16', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Chris Coleman', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '11/17/16', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Tina Liebling', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '4/2/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Keith Downey', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '7/24/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Blake Huffman', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '4/19/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Matt Dean', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '4/26/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Paul Thissen', 'party': 'DFL', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '6/15/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Jeff Johnson', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '5/10/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Jeffery Ryan Wharton', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '3/20/17', 'drop-out-date': '', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Ole Savior', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '1/18/17', 'drop-out-date': '7/27/2017', 'office-sought': 'Governor'}, {'blurb': '', 'incumbent?': 'No', 'name': 'Christopher William Chamberlin ', 'party': 'Republican', 'headshot-url': '', 'endorsed?': 'No ', 'date-declared': '11/24/16', 'drop-out-date': '', 'office-sought': 'Governor'}]

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

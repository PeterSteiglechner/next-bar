from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd

#cafes = ["Lisboa", "Olala", "Frida", "Pourpour"]
# bars = ["Sonderbar", "Zum Erleneck"," Falstaff", "Flusshexe", "Torros", "Dejavú", "Drittel", "Paganini", "Neustädter Tenne",\
#        "Gastfeld", "Frederick",  "Meyman", "Nr 72", "Tequila","Carlitos", "Woodstock", "Papp", "Kukoon", "Gordon's"," Lütje Lehmann",\
#        "Champion",  "Mono", "Gondi", "Anna's Welt"]

# ratings = {}
#ratings["Lisa"] = np.array([5,7,13,9,8,3,18,20,11,14,12,17,21,16,15,4,19,23,6,1,2,22,10])
#ratings["Annika"] = np.array([7,12,19,1,11,18,22,14,6,20,13,16,4,5,17,8,21,23,3,9,2,15,10])
#ratings["Anni"] = np.array([1,12,11,2,10,3,13,4,14,15,16,23,22,21,17,9,20,8,7,6,5,19,18])
#ratings["Peter"] = np.array([7,8,15,6,9,2,18,19,16,13,12,21,22,20,17,5,11,23,4,3,1,10,14])
#ratings["Tarik"] = np.array([4,8,7,9,10,5,18,22,21,19,11,17,20,16,15,1,12,13,6,2,3,23,14])

# ratings["Peter"] = {
#     "Falstaff":4,
#     "Drittel":7,
#     "Gastfeld":6,
#     "Carlitos":5,
#     "Papp":9,
#     "Kukoon":8,
#     "Gondi":7,
#     "Tau":5,
#     "Hart Backbord":6,
#     "Helga":9,
#     "Anna's Welt":9,
#     "Spitzen Gebel":5,
#     "Little Mary":3,
#     "Ständige Vertretung":7,
#     "Kweer":8,
#     "Eisen":5,
#     "Hegarty's":2,
#     "Kono":9,
#     "Fehrfeld":2,
#     "Marlenchen":3
# }

allUsers = [] # list(ratings.keys())

selectedUsers = []# list(np.copy(allUsers)) # for now.

# TODO: lead users from .csv

ttb_param = 1

r = pd.DataFrame(columns=["prob", "probp1", "place", "Probability [%]"]) #pd.DataFrame.from_dict(ratings)


#r=r.reset_index().rename(columns={"index":"place"})
#r["probp1"] = r.drop(columns=["place"]).sum(axis=1)
#r["probp1"] *= 1/r["probp1"].sum()
#r["prob"] = r["probp1"]**ttb_param
#r["prob"] *= 1/r["prob"].sum()
#r = r.sort_values("prob", ascending=False).reset_index(drop=True)[["place"]+selectedUsers+["prob"]+["probp1"]]
#r["Probability [%]"] = (r["prob"] * 100).round(1)

unique_places = [] # r['place'].tolist()


app = Flask(__name__)

@app.route('/select_choice', methods=['POST'])
def select_choice():
    return np.random.choice(r.place, p=r['prob'])

@app.route('/')
def index():
    return render_template('index.html', 
                           selected ="   ", 
                           unique_places=unique_places, 
                           ttb_param=ttb_param, 
                           probs= r.drop(columns=["prob", "probp1"]).to_html(classes='table table-striped', justify="left", index=True))

@app.route('/rerun')
def rerun():
    choice = select_choice()
    return {'selected': choice}

@app.route('/update_ratings', methods=['POST'])
def update_ratings():
    global r, selectedUsers
    user_name = request.json.get('userName', '')
    place = request.json.get('place', '')
    new_rating_string = request.json.get('newRating', '')
    if new_rating_string=='' or place=="" or user_name=="":
        print("enter new rating")
    else:
        new_rating = int(new_rating_string)
        # If the user's name is not in the table, append a new column
        if user_name not in r.columns:
            r[user_name] = np.nan
            allUsers.append(user_name)
            selectedUsers.append(user_name)
        # Update the specified place's rating
        r.loc[r.place==place, user_name] = new_rating

    return jsonify({'newTable': update_matrix()})



@app.route('/update_ttb_param', methods=['POST'])
def update_ttb_param():
    global ttb_param, r
    ttb_param_str = request.json.get('updated_ttb_param', '')
    if ttb_param_str =="":
        print("enter ttb_param_str")
    else:
        ttb_param = float(ttb_param_str)
    return jsonify({'newTable': update_matrix(), 'new_ttb_param':ttb_param})



@app.route('/update_ratings_combi', methods=['POST'])
def update_ratings_combi():
    global r, selectedUsers
    # Get user input from the request
    user_name = request.json.get('userName', '')
    ratings_list = request.json.get('ratings', [])
    ratings_list = np.array(ratings_list)
    print(ratings_list, ratings_list==None, ratings_list[ratings_list==None], user_name)
    if None in ratings_list:
        ratings_list[ratings_list==None] = np.nan 
    if (ratings_list==np.nan).all() or user_name=="":
        print("enter ratings!")
    else:
        if user_name not in r.columns:
            r[user_name] = np.nan
            allUsers.append(user_name)
            selectedUsers.append(user_name) 
        for k,place in enumerate(unique_places):   
            r.loc[r.place==place, user_name] = ratings_list[k]

    return jsonify({'newTable': update_matrix()})

@app.route('/clear_r')
def clear_r():
    global r, unique_places
    r = pd.DataFrame(columns=["prob", "probp1", "place", "Probability [%]"]) #pd.DataFrame.from_dict(ratings)
    unique_places=[]
    return  jsonify({'newTable': update_matrix()})
     
     
     
@app.route('/add_bar', methods=['POST'])
def add_bar():
    global r, unique_places
    place = request.json.get("placeName", "")
    cols = dict(zip(r.columns, [np.nan for k in r.columns]))
    cols["place"]=place
    print(pd.DataFrame([cols]), r)
    
    if len(r)==0:
        r = pd.DataFrame([cols], index=[0])
    else:
        r.loc[len(r)] = cols
    
    unique_places = r['place'].tolist()
    unique_places.sort()
    return  jsonify({'newTable': update_matrix(), "new_unique_places":unique_places})
     
     
@app.route('/get_unique_places')
def get_unique_places():
    global unique_places
    return jsonify(unique_places=unique_places)
    

def update_matrix():
    global r, unique_places
    
    if r is None:
        r=r.reset_index().rename(columns={"index":"place"})
        unique_places = r['place'].tolist()
        unique_places.sort()

    # Recalculate probabilities and update the table
    r["probp1"] = r[selectedUsers].sum(axis=1)
    if not(r["probp1"].sum()==0):
        r["probp1"] *= 1/r["probp1"].sum()
    r["prob"] = r["probp1"]**ttb_param
    if not(r["prob"].sum()==0):
        r["prob"] *= 1 / r["prob"].sum()
    r = r.sort_values(by="prob", ascending=False).reset_index(drop=True)
    r["Probability [%]"] = (r["prob"] * 100).round(1)
    # Convert the updated table to HTML and send it back to the client
    updated_table_html = r.drop(columns=["prob", "probp1"])[["place"]+selectedUsers+["Probability [%]"]].to_html(classes='table table-striped', justify="left", index=True)
    return updated_table_html



@app.route('/save_column', methods=['POST'])
def save_column():
    column_name = request.json.get("columnName","")
    title = request.json.get("titleInput","")
    if column_name not in r.columns:
        return jsonify({'error': 'Column not found'}), 400
    r[["place", column_name]].to_csv(f'users/{title}_{column_name}.csv', index=False)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) #
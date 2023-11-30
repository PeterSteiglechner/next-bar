from flask import Flask, render_template,  request, jsonify
import numpy as np
import pandas as pd

cafes = ["Lisboa", "Olala", "Frida", "Pourpour"]
#bars = ["Sonderbar", "Zum Erleneck"," Falstaff", "Flusshexe", "Torros", "Dejavú", "Drittel", "Paganini", "Neustädter Tenne",\
#    "Gastfeld", "Frederick",  "Meyman", "Nr 72", "Tequila","Carlitos", "Woodstock", "Papp", "Kukoon", "Gordon's"," Lütje Lehmann",\
#    "Champion",  "Mono", "Gondi"]
ratings = {}
#ratings["Lisa"] = np.array([5,7,13,9,8,3,18,20,11,14,12,17,21,16,15,4,19,23,6,1,2,22,10])
#ratings["Annika"] = np.array([7,12,19,1,11,18,22,14,6,20,13,16,4,5,17,8,21,23,3,9,2,15,10])
#ratings["Anni"] = np.array([1,12,11,2,10,3,13,4,14,15,16,23,22,21,17,9,20,8,7,6,5,19,18])
#ratings["Peter"] = np.array([7,8,15,6,9,2,18,19,16,13,12,21,22,20,17,5,11,23,4,3,1,10,14])
#ratings["Tarik"] = np.array([4,8,7,9,10,5,18,22,21,19,11,17,20,16,15,1,12,13,6,2,3,23,14])
ratings["Peter"] = np.array([90, 70, 90, 80])
ratings["Anni"] = np.array([100, 40, 50, 80])

allUsers = list(ratings.keys())

selectedUsers = list(np.copy(allUsers)) # for now.
print(selectedUsers)

r = pd.DataFrame.from_dict(ratings)
r["choices"] = cafes
r["prob"] = r.drop(columns=["choices"]).sum(axis=1)
r["prob"] *= 1/r["prob"].sum()
r = r.sort_values("prob", ascending=False).reset_index(drop=True)[["choices"]+selectedUsers+["prob"]]
r["Probability [%]"] = (r["prob"] * 100).round(1)


app = Flask(__name__)


def select_choice():
    return np.random.choice(r.choices, p=r.prob)

@app.route('/')
def index():
    # Generate a random number between 1 and 100
    #selected_choice = np.random.choice(r.choices, p=prob)
    return render_template('index.html', selected ="   ", select_choice = select_choice, probs= r.drop(columns="prob").to_html(classes='table table-striped', justify="left", index=True))

@app.route('/rerun')
def rerun():
    choice = select_choice()
    return {'selected': choice}


@app.route('/update_ratings', methods=['POST'])
def update_ratings():
    global r, selectedUsers
    
    # Get user input from the request
    user_name = request.json.get('userName', '')
    establishment = request.json.get('establishment', '')
    new_rating = int(request.json.get('newRating', ''))

    # If the user's name is not in the table, append a new column
    if user_name not in r.columns:
        r[user_name] = np.nan
        allUsers.append(user_name)
        selectedUsers.append(user_name)

    # Update the specified establishment's rating
    print(f"updating user {user_name} with new rating {new_rating} for bar {establishment}.")
    r.loc[r.choices==establishment, user_name] = new_rating

    # Recalculate probabilities and update the table
    r["prob"] = r[selectedUsers].sum(axis=1)
    r["prob"] *= 1 / r["prob"].sum()
    r = r.sort_values(by="prob", ascending=False).reset_index(drop=True)
    r["Probability [%]"] = (r["prob"] * 100).round(1)
    print(r)

    # Convert the updated table to HTML and send it back to the client
    updated_table_html = r.drop(columns="prob")[["choices"]+selectedUsers+["Probability [%]"]].to_html(classes='table table-striped', justify="left", index=True)
    return jsonify({'newTable': updated_table_html})


if __name__ == '__main__':
    app.run(debug=True) # 
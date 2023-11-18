from flask import Flask, render_template
import numpy as np
import pandas as pd

bars = ["Sonderbar", "Zum Erleneck"," Falstaff", "Flusshexe", "Torros", "Dejavú", "Drittel", "Paganini", "Neustädter Tenne",\
        "Gastfeld", "Frederick",  "Meyman", "Nr 72", "Tequila","Carlitos", "Woodstock", "Papp", "Kukoon", "Gordon's"," Lütje Lehmann",\
        "Champion",  "Mono", "Gondi"]
ratings = {}
ratings["Lisa"] = np.array([5,7,13,9,8,3,18,20,11,14,12,17,21,16,15,4,19,23,6,1,2,22,10])
ratings["Annika"] = np.array([7,12,19,1,11,18,22,14,6,20,13,16,4,5,17,8,21,23,3,9,2,15,10])
ratings["Anni"] = np.array([1,12,11,2,10,3,13,4,14,15,16,23,22,21,17,9,20,8,7,6,5,19,18])
ratings["Peter"] = np.array([7,8,15,6,9,2,18,19,16,13,12,21,22,20,17,5,11,23,4,3,1,10,14])
ratings["Tarik"] = np.array([4,8,7,9,10,5,18,22,21,19,11,17,20,16,15,1,12,13,6,2,3,23,14])


ratingsDF = pd.DataFrame.from_dict(ratings)
ratingsDF["Bars"] = bars
ratingsDF = ratingsDF.set_index("Bars")
ratingsDF["prob"] = ratingsDF.sum(axis=1)
ratingsDF["prob"] *= 1/ratingsDF["prob"].sum()
ratingsDF = ratingsDF.sort_values("prob", ascending=False)
ratingsDF["Probability [%]"] = (ratingsDF["prob"] * 100).round(1)


app = Flask(__name__)


def select_bar():
    return np.random.choice(bars, p=ratingsDF["prob"])

@app.route('/')
def index():
    # Generate a random number between 1 and 100
    #selected_bar = np.random.choice(bars, p=prob)
    return render_template('index.html', selected_bar ="   ", select_bar = select_bar, barsProbs= ratingsDF.drop(columns="prob").to_html(classes='table table-striped', justify="left", index=True))

@app.route('/rerun')
def rerun():
    bar = select_bar()
    return {'selected_bar': bar}

if __name__ == '__main__':
    app.run(debug=True) # 
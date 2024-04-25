#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 
        features_list=obj.getFeaturesList()

        texts = ["Negative", "Negative", "Positive"]
        res = []
        feature_names = [
        "Using IP Address",
        "Long URL",
        "Short URL",
        "@ Symbol in URL",
        "Double Slashes in URL",
        "Prefix or Suffix in Domain",
        "Number of Subdomains",
        "HTTPS Usage",
        "Domain Registration Length",
        "Favicon",
        "Non-Standard Port",
        "HTTPS in Domain",
        "Request URL",
        "Anchor URLs",
        "Links in Script and Link Tags",
        "Server Form Handler",
        "Info Email",
        "Abnormal URL",
        "Website Forwarding",
        "Status Bar Customization",
        "Disabling Right-Click",
        "Using Pop-up Window",
        "IFrame Redirection",
        "Age of Domain",
        "DNS Recording",
        "Website Traffic",
        "Page Rank",
        "Google Index",
        "Links Pointing to Page",
        "Stats Report"
    ]
        for feature in features_list:
            res.append(texts[feature + 1])

        print(features_list)
        print(res)
        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        if y_pred == 1:
            pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing * 100)
        else:
            pred = "It is {0:.2f} % unsafe to go ".format(y_pro_non_phishing * 100)

        return render_template('index.html', xx=round(y_pro_non_phishing, 2), url=url, features=feature_names, pred=pred, res=res)

    return render_template("index.html", xx=-1)

@app.route("/awareness", methods=["GET", "POST"])
def aware():
    return render_template("awareness.html")

@app.route("/privacy_tips", methods=["GET", "POST"])
def privacy_tips():
    return render_template("privacy_tips.html")

if __name__ == "__main__":
    app.run(debug=True)
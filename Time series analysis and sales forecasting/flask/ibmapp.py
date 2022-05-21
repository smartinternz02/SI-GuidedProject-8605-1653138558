import joblib
import pandas as pd
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
import os
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "EEJRSbweXwLAQYUqx_AXWtSOTsdgo6bDCEKjS5C6IIE5"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
#model = joblib.load('sales.sav')

@app.route('/')
def home():
    return render_template('predict.html')

@app.route('/predict',methods=['POST'])
def y_predict():
    if request.method == "POST":
        ds = request.form["date"]
        a={"ds":[ds]}
        ds=pd.DataFrame(a)
        ds['year']=pd.DatetimeIndex(ds['ds']).year
        ds['month']=pd.DatetimeIndex(ds['ds']).month
        
        ds.drop('ds',axis=1,inplace=True)
        ds=ds.values.tolist()
        payload_scoring={"input_data":[{"feilds":[["year","month"]],"values":ds}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/59f60396-2a28-4892-8f36-54b5c660c303/predictions?version=2022-03-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        pred= response_scoring.json()
        print(pred)
        output= pred['predictions'][0]['values'][0][0]
        print(output)
       
        return render_template('predict.html',output="The sale value on selected date is {} thousands".format(output))
    return render_template("predict.html")
#port=os.getenv('VCAP_APP_PORT','8080')
    
if __name__ == "__main__":
    # app.secret_key=os.urandom(12)
    # app.run(debug=true,host='0.0.0.0',port=port)
    app.run(debug=True)






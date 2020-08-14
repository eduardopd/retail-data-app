from flask import Flask, request
import pandas as pd 
import numpy as np  
import flasgger
from flasgger import Swagger
import pickle

app = Flask(__name__)
Swagger(app)

pickle_in=open('model.pkl','rb')
model = pickle.load(pickle_in)

@app.route('/')
def welcome():
    return 'Bem-vindo'

@app.route('/predict_parameters', methods=["Get"])
def predict_sales_parameters():
    """Predict output with parameters
    ---
    parameters:
        - name: Dept
          in: query
          type: number
          required: true       
        - name: Year_Week
          in: query
          type: number
          required: true       
        - name: Last_Week_Sales
          in: query
          type: number
          required: true       
        - name: Last_Week_Diff
          in: query
          type: number
          required: true       
    responses:
        200:
            description: The output values
    """

    dept = request.args.get("Dept")
    year_week = request.args.get("Year_Week")
    last_week_sales = request.args.get("Last_Week_Sales")
    last_week_diff = request.args.get("Last_Week_Diff")

    p = model.predict([[dept, year_week, last_week_sales, last_week_diff]])
  
    return str(p)


@app.route('/predict_file', methods=["POST"])
def predict_sales():

    """Predict output with fil
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
    responses:
        200:
            description: The output values
    """

    df_test = pd.read_csv(request.files.get("file"))
    print(df_test.head())
    p = model.predict(df_test)



    return str(list(p)) 


if __name__ == '__main__':
    app.debug = True
    app.run()

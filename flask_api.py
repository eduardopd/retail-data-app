from flask import Flask, request
import pandas as pd 
import numpy as np  
import pickle

app = Flask(__name__)
pickle_in=open('flask_model.pkl','rb')
model = pickle.load(pickle_in)

@app.route('/')
def welcome():
    return 'Bem-vindo'

@app.route('/predict_parameters', methods=["Get"])
def predict_sales_parameters():   
    temperature = request.args.get("Temperature")
    fuel_price = request.args.get("Fuel_Price")
    cpi = request.args.get("CPI")
    unemployment = request.args.get("Unemployment")
    dept = request.args.get("Dept")
    isHoliday_y = request.args.get("IsHoliday_y")
    year_week = request.args.get("Year_Week")
    last_week_sales = request.args.get("Last_Week_Sales")
    last_week_diff = request.args.get("Last_Week_Diff")

    p = model.predict([[temperature, fuel_price, cpi, unemployment, dept, isHoliday_y, year_week, last_week_sales, last_week_diff]])
    
    return "Valores da previsão:" + str(p) 


@app.route('/predict_file', methods=["POST"])
def predict_sales():
    df_test = pd.read_csv(request.files.get("file"))
    p = model.predict(df_test)

    return "Valores da previsão:" + str(list(p)) 

if __name__ == '__main__':
    app.run()
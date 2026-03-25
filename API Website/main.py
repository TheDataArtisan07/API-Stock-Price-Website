from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

class Form(FlaskForm):
    symbol = StringField(validators=[DataRequired()])
    from_date = DateField(validators=[DataRequired()])
    to_date = DateField(validators=[DataRequired()])
    submit = SubmitField(label='')

load_dotenv()

API_KEY = os.getenv('MY_API_KEY')
API_END_POINT = "https://api.marketstack.com/v1/eod"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')


def convert_date(date_str):
    # Parse the input date string in DD-MM-YYYY format
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')

    # Return the date in YYYY-MM-DD format
    return date_obj.strftime('%Y-%m-%d')

@app.route('/',methods=['GET','POST'])
def home():
    form = Form()
    if form.validate_on_submit():
        symbol = form.symbol.data
        f_date = form.from_date.data
        t_date = form.to_date.data
        parameters = {'access_key': API_KEY, 'symbols': symbol, 'date_from': f_date,
                      'date_to': t_date,'limit':'25'}
        response = requests.get(url=API_END_POINT, params=parameters)
        info = response.json()
        datas = info["data"]
        if datas:
            return render_template('info.html', data=datas,company=symbol)
        else:
            return f"Error info! Try Again."
    return render_template('index.html',form=form)

if __name__=='__main__':
    app.run(debug=True)


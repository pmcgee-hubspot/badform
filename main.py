from flask import Flask, request
from flask_basicauth import BasicAuth
import os
import json
import requests

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)


@app.route("/")
@basic_auth.required
def index():
    return """
    <form action='/submit'>
        Company Name: <input type='text' name='name' value='' />
        <input type='submit' />
    </form>
    """


@app.route("/submit")
@basic_auth.required
def submit():
    name = request.args.get("name", '')
    output = os.popen(f"curl https://autocomplete.clearbit.com/v1/companies/suggest?query={name}").read()

    if output == "":
        output = requests.get(f"https://autocomplete.clearbit.com/v1/companies/suggest?query={name}").text

    logo = None
    try:
        output_json = json.loads(output)
        logo = None
        if len(output_json) > 0:
            logo = output_json[0]['logo']
    except:
        pass

    return f"""
    <div>
    Thanks for submitting {name}!
    </div>
    
    <div>
    <b>We got this information on it from Clearbit:</b><br/>
    {output}
    </div>

    <div>
    <b>Here's an image of the first logo:</b><br/>
    <img src="{logo}" />
    </div>
    """
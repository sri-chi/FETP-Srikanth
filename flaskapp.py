import os
import pathlib
from datetime import datetime
import pytz
import requests
from flask import Flask, session, abort, redirect, request, render_template, url_for
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask(__name__)
app.secret_key = "6863f001-b88c-4c41-99ad-3d9b4af5614a"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "1031444844263-k41hhg8n2rujt98d599q15gdk3mcueln.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["pic"] = id_info.get("picture")
    session["email"] = id_info.get("email")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    #rendering home html page
    return render_template("home.html")


@app.route("/protected_area")
@login_is_required
def protected_area():
    tz = pytz.timezone('Asia/Kolkata')  # Setting timezone for India
    current_time = datetime.now(tz).strftime('%d-%B-%Y %I:%M:%p %Z')
    name1 = session["name"]
    name2 = name1.title()
    return render_template("about.html", ct=current_time, pic=session["pic"], name=name2, emailid=session["email"])

@app.route("/generate")
def generate():
    tz = pytz.timezone('Asia/Kolkata')  # Setting timezone for India
    current_time = datetime.now(tz).strftime('%d-%B-%Y %I:%M:%p %Z')
    name1 = session["name"]
    name2 = name1.title()
    # Get the number of lines from the user input
    num = int(request.args.get('numb'))
    # Adjust the number of lines if it is even
    if (num % 2 == 0):
        n = num + 1
    else:
        n = num
    # Define the word string
    word = "FORMULAQSOLUTIONS"
    # Define the length of the word string
    l = len(word)
    # Define the half of the number of lines
    h = n // 2
    a = 1
    b = h + h + 1
    # Initialize an empty list for the pattern
    pattern = []
    # Loop through the first half of the lines
    for i in range(h):
        # Initialize an empty string for the line
        line = ""
        # Loop through the characters in the word string
        for j in range(a):
            # Calculate the index of the character to be printed
            k = (i + j) % l
            # Append the character to the line
            line += word[k]
        # Append the line with spaces in front to the pattern list
        pattern.append(" " * (h - i) + line)
        a += 2
    # Loop through the second half of the lines
    for i in range(h, n):
        # Initialize an empty string for the line
        line = ""
        # Loop through the characters in the word string
        for j in range(b):
            # Calculate the index of the character to be printed
            k = (i + j) % l
            # Append the character to the line
            line += word[k]
        # Append the line with spaces in front to the pattern list
        pattern.append(" " * (i - h) + line)
        b -= 2
    # Render the generate.html template with the pattern list
    return render_template('about.html', ct=current_time, pic=session["pic"], name=name2, emailid=session["email"], pattern=pattern, lines=num)



if __name__ == "__main__":
    app.run(debug=True)

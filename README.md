## FETP-Srikanth
<h3>This Flask application has a button to sign in via Gmail and allows us to authenticate using Gmail. The web application displays basic info on successful authentication like profile picture, name, and email.</h3>
<h4>Steps followed in creating this application:</h4>
<h5>
<ul>
  <li>First set up the required environment. Install Flask and Flask-OAuthlib, which are Python 
  libraries for creating web apps and handling OAuth authentication. We can use pip command c to 
  install them.</li>	
  <li>Create a Google project and obtain the client ID and client secret for your application. You will need these credentials to interact with Google’s OAuth service. You can download the credentials in the form of a .json file(client_secret.json). </li>
  <li>Create a Flask application(flaskapp.py) and configure it with the client ID and client secret. Create routes for login and callback URLs. </li>
  <li>We can use the authorized_response method of the remote application object to obtain the access token and other information from Google. You can then use the access token to make requests to Google’s API and get the user’s email and profile information.</li>
  <li>Create HTML files(home.html, about.html) to create how the web page looks and use the render_template function to render those HTML files.</li>
</ul>
</h5>
<h4>Sample Screenshots of how my application looks:</h4>
<img src="https://github.com/sri-chi/FETP-Srikanth/assets/35699881/6d7988c4-2c49-4929-b800-8d570680c77b" width="300">..<image src="https://github.com/sri-chi/FETP-Srikanth/assets/35699881/39b75fc3-7737-4f49-8807-3b4674b32b93" width="300">..<img src="https://github.com/sri-chi/FETP-Srikanth/assets/35699881/fe328154-8ecb-4c11-bf83-7eae70ee4411" width="300">..<img src="https://github.com/sri-chi/FETP-Srikanth/assets/35699881/c8ee5864-c4ef-4b11-bc9c-655725aa69ec" width="300">

>



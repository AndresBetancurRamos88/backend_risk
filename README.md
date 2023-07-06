# Risk Backend

## Project Description
```
This application allows you to manage the company's cybersecurity risks
```

## Technologies Used
```
- Python
- Flask
```

## Getting Started
```
Clone this repository 
- git clone https://github.com/AndresBetancurRamos88/backend_risk
```

## Run project locally
```
Open de command prompt and navigate to the path where the app was cloned

Then run the following commands:
- pip install pipenv
- pipenv --python 3.9
- pipenv shell
- pipenv install
- save secret key in an environment variable or in an .env file (variable name "SECRET_KEY")
```

## Create google application
```
Go to the folowing url:
- https://console.cloud.google.com/
- In the upper panel choose the option, create project
- Select the "credentials" option from the left panel
- Configure the "OAuth Consent Screen" in the left panel. 
    - Select "external", then create
    - fill in the fields name, email, Application home page (must be http://localhost:8000/) and Developer Contact Information
- In the upper panel select the option "create credentials"
    - Choose "Oauth client id"
    - In application type, select "web application"
    - Choose a name
    - In JavaScript authoritative sources use this url "http://localhost:8000"
    - In Authorized redirect URIs use the following urls
        - http://localhost:8000/login
        - http://localhost:8000/authorize
        - http://127.0.0.1:8000/authorize
        - http://localhost:8000/oauth2-redirect.html
        - http://localhost:8000/token
- save client id and client secret in environment variables or in an .env file (variable name "CLIENT_ID" "CLIENT_SECRET") 
```

## Test application
```
- Open de command prompt and navigate to the path where the app was cloned
- Activate virtual environment "pipenv shell"
- run application "flask run"
- Go to the following url and test the application in swagger http://localhost:8000/api-docs
```
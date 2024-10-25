## .env file to input keys=
copy the .env.example to .env (backend and frontend folder)

## To Generate A Secret Key
You can use import secrets or other ways to generate a random key   
    import secrets
    secret_key = secrets.token_hex(32)
    print(secret_key) 

## To Generate Google Client ID and Secret
Step 1: Create a Project in Google Cloud Console
- Go to the [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)
- Click on the project drop-down and select "New Project."
- Enter a project name and click "Create."

Step 2: Create OAuth 2.0 Client ID
- In the "Credentials" page, click on "Create Credentials" and select "OAuth 2.0 Client ID."
- Configure the consent screen by providing the necessary information (e.g., application name, support email).
- Select the application type (Web application).
- Enter the authorized redirect URIs (http://localhost:5000/auth).
- Enter the authorized Javascript URIs (http://localhost:5173 or the react localhost, http://localhost).
- Click "Create."

Your new client ID and client secret will be displayed. Copy and store them in the .env file
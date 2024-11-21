Instructions:
- Download and extract the <a href="https://github.com/TheKliko/fastflag-tracker/releases/latest">latest release</a>
- Run `install_libraries.bat` to install the requests library (this step can be skipped if it is already installed)
- Open `config/config.json` and set up your config
  - "url": (REQUIRED) The webhook URL to send updates to, this can either be a single string or a list of multiple URLs if you have multiple webhooks
  - "error_url": (OPTIONAL) The URL to send fatal error messages to before the program shuts down, again this should be either a string or a list of strings
  - "username": (OPTIONAL) Overwrite the webhook's username a custom username
  - "avatar_url": (OPTIONAL) Overwrite the webhook's avatar with a custom image
- Run `main.py` to start tracking FastFlags

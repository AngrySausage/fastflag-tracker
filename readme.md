Instructions:
- Download and extract the <a href="https://github.com/TheKliko/fastflag-tracker/releases/latest">latest release</a>
- For Windows: Run `install_libraries.bat` to install the `requests` library (this step can be skipped if it is already installed)
- For macOS: Open a terminal, navigate to the extracted folder, and run:
  ```bash
  ./install_libraries.sh
  ```
  This will install the `requests` library into the `libraries` folder.
- Open `config/config.json` and set up your config:
  - `"url"`: (REQUIRED) The webhook URL to send updates to. This can either be a single string or a list of multiple URLs if you have multiple webhooks.
  - `"error_url"`: (OPTIONAL) The URL to send fatal error messages to before the program shuts down. This should also be either a string or a list of strings.
  - `"username"`: (OPTIONAL) Overwrite the webhook's username with a custom username.
  - `"avatar_url"`: (OPTIONAL) Overwrite the webhook's avatar with a custom image.
- Run `main.py` to start tracking FastFlags.

You can set up custom filters to exclude specific FastFlags by editing `modules/get_fastflags.py`.
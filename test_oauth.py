from api_helper import NorenApiPy
import logging
import os
import sys
import yaml
import webbrowser
import platform
import subprocess


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

logging.basicConfig(level=logging.INFO)

api = NorenApiPy()


def open_browser(url):
    system = platform.system()

    try:
        if system == "Windows":
            webbrowser.open(url)

        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", url])

        elif system == "Linux":
            try:
                subprocess.Popen(["google-chrome", url])
            except FileNotFoundError:
                try:
                    subprocess.Popen(["chromium-browser", url])
                except FileNotFoundError:
                    subprocess.Popen(["xdg-open", url])

        else:
            webbrowser.open(url)

        print("\nBrowser opened successfully.")

    except Exception as e:
        print("\nCould not open browser automatically.")
        print("Open this URL manually:")
        print(url)
        print("Error:", e)


with open("cred.yml", "r") as f:
    cred = yaml.load(f, Loader=yaml.FullLoader) or {}

apikey_url = api.getOAuthURL(
    cred["oauth_url"],
    cred["client_id"]
)

print("\nOAuth URL:")
print(apikey_url)

open_browser(apikey_url)

print("\nAfter login, copy auth_code from the redirect URL.")

auth_code = input("Enter your auth code here: ").strip()

result = api.getAccessToken(
    auth_code,
    cred["Secret_Code"],
    cred["client_id"],
    cred["UID"]
)

if result is not None:
    acc_tok, usrid, ref_tok, actid = result

    print("\nLogin successful.")
    print("User ID:", usrid)
    print("Account ID:", actid)

    cred["Access_token"] = acc_tok
    cred["Account_ID"] = actid

    with open("cred.yml", "w") as f:
        yaml.dump(cred, f)

    print("\nAccess token saved to cred.yml")

else:
    print("\nFailed to retrieve access token.")

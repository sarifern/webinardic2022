import os
import fifa_api

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

TOKEN = fifa_api.login(email=EMAIL, password=PASSWORD)
if TOKEN:
    print(fifa_api.matches_today(TOKEN))

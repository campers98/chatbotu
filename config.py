from os import getenv

LOAD = getenv("LOAD", "").split()

NO_LOAD = getenv("NO_LOAD", "").split()

TOKEN = getenv("TOKEN", "6577602955:AAEFWTDarFdFmrhTNgmgtMWlcx_bxhWIQ3g")

MONGO_DB_URL = getenv(
    "MONGO_DB_URL",
    "mongodb+srv://monivps5:monivps5@cluster0.kmbq8we.mongodb.net/?retryWrites=true&w=majority",
)

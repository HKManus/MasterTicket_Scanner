from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from edit_firebase import *
from datetime import datetime

firebase_init()


def authenticate_hash(event, hash):
    response = read(f"/{event}/{hash}")
    print(f"raw response: {response}")

    if response != None:
        response["person_exist"] = True
        current_time = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        if response["count"] == False:
            save(f"/{event}/{hash}/count", True)
            save(f"/{event}/{hash}/time", current_time)
            response["time"] = current_time

    else:
        response = {"person_exist": False}

    print(f"return response: {response}")
    return response


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

"""---"""


@app.get("/{event}/{hash}")
async def read_user(event, hash):
    return authenticate_hash(event, hash)


# uvicorn firebase_update_api:app --reload

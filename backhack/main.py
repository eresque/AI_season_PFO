import random

from fastapi import FastAPI, File, UploadFile, Response
import datetime
from fastapi.middleware.cors import CORSMiddleware

from datetime import date, timedelta

import joblib
import pandas as pd

from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

app = FastAPI(
    title="API for ML"
)

origins = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/getPlace")
def setPlace(place: str):
    return {"message": "place upload succefsully"}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        print(contents)
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "there was an error uploading file"}
    finally:
        file.file.close()

    return {"message": f"Successfuly uploaded {file.filename}"}


def zap(arr):
    for i in range(0, 6):
        for j in range(0, 10):
            arr[i][j] = random.randint(0, 1)
    return arr


@app.get("/pizdec")
def getInfo(date: datetime.date = '2023-03-28'):
    # DTP predictions
    model_dtp = joblib.load("Models/DTP.joblib")
    X_preds_dtp = pd.read_csv('Data/X_DTP.csv')[:10]

    y_preds_dtp = model_dtp.predict(X_preds_dtp)

    risk_factor_dtp = 0
    accident_percent = sum(sum(y_preds_dtp)) / (len(y_preds_dtp) * len(y_preds_dtp[0]))

    if accident_percent <= 0.3:
        risk_factor_dtp = 0
    elif 0.3 < accident_percent <= 0.7:
        risk_factor_dtp = 1
    else:
        risk_factor_dtp = 2

    dates = [date + timedelta(i) for i in range(10)]

    all_preds = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    templates = {
        "event":
            {
                "dtp":
                    {
                        dates[0]: "".join(map(str, y_preds_dtp[0])),
                        dates[1]: "".join(map(str, y_preds_dtp[1])),
                        dates[2]: "".join(map(str, y_preds_dtp[2])),
                        dates[3]: "".join(map(str, y_preds_dtp[3])),
                        dates[4]: "".join(map(str, y_preds_dtp[4])),
                        dates[5]: "".join(map(str, y_preds_dtp[5])),
                        dates[6]: "".join(map(str, y_preds_dtp[6])),
                        dates[7]: "".join(map(str, y_preds_dtp[7])),
                        dates[9]: "".join(map(str, y_preds_dtp[8])),
                        "risk_factor": risk_factor_dtp
                    },
                "toxic":
                    {
                        dates[0]: all_preds[1][0],
                        dates[1]: all_preds[1][1],
                        dates[2]: all_preds[1][2],
                        dates[3]: all_preds[1][3],
                        dates[4]: all_preds[1][4],
                        dates[5]: all_preds[1][5],
                        dates[6]: all_preds[1][6],
                        dates[7]: all_preds[1][7],
                        dates[8]: all_preds[1][8],
                        dates[9]: all_preds[1][9],
                        "risk_factor": 0
                    },
                "natural":
                    {
                        dates[0]: all_preds[2][0],
                        dates[1]: all_preds[2][1],
                        dates[2]: all_preds[2][2],
                        dates[3]: all_preds[2][3],
                        dates[4]: all_preds[2][4],
                        dates[5]: all_preds[2][5],
                        dates[6]: all_preds[2][6],
                        dates[7]: all_preds[2][7],
                        dates[8]: all_preds[2][8],
                        dates[9]: all_preds[2][9],
                        "risk_factor": 0
                    },
                "GKH":
                    {
                        dates[0]: all_preds[3][0],
                        dates[1]: all_preds[3][1],
                        dates[2]: all_preds[3][2],
                        dates[3]: all_preds[3][3],
                        dates[4]: all_preds[3][4],
                        dates[5]: all_preds[3][5],
                        dates[6]: all_preds[3][6],
                        dates[7]: all_preds[3][7],
                        dates[8]: all_preds[3][8],
                        dates[9]: all_preds[3][9],
                        "risk_factor": 0
                    },
                "explosions":
                    {
                        dates[0]: all_preds[4][0],
                        dates[1]: all_preds[4][1],
                        dates[2]: all_preds[4][2],
                        dates[3]: all_preds[4][3],
                        dates[4]: all_preds[4][4],
                        dates[5]: all_preds[4][5],
                        dates[6]: all_preds[4][6],
                        dates[7]: all_preds[4][7],
                        dates[8]: all_preds[4][8],
                        dates[9]: all_preds[4][9],
                        "risk_factor": 0
                    },
                "another":
                    {
                        dates[0]: all_preds[5][0],
                        dates[1]: all_preds[5][1],
                        dates[2]: all_preds[5][2],
                        dates[3]: all_preds[5][3],
                        dates[4]: all_preds[5][4],
                        dates[5]: all_preds[5][5],
                        dates[6]: all_preds[5][6],
                        dates[7]: all_preds[5][7],
                        dates[8]: all_preds[5][8],
                        dates[9]: all_preds[5][9],
                        "risk_factor": 0
                    },
            }
    }
    return templates

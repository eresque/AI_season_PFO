import random

from fastapi import FastAPI, File, UploadFile, Response
import datetime
from fastapi.middleware.cors import CORSMiddleware

from datetime import date, timedelta

import joblib
import pandas as pd
from tabpfn import TabPFNClassifier

from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

app = FastAPI(
    title="API for ML"
)

origins = [
    'http://172.28.2.1:3000',
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


def dtp_to_class_str(y_preds_dtp):
    lst = [
        'ДТП/Столкновение',
        'ДТП/Наезд',
        'ДТП/Съезд',
        'ДТП/Опрокидывание',
        'Не справился с управлением',
        'Неисправность транспортного средства',
        'Нарушение ПДД',
        'ДТП/Падение пассажира',
        'Возгорание транспортого средства'
    ]
    mass = [[] for i in range(len(y_preds_dtp))]

    for i in range(len(y_preds_dtp)):
        for ind, flag in enumerate(y_preds_dtp[i]):
            print(ind)
            print(mass[i])
            print(y_preds_dtp[i])
            if flag:
                mass[i].append(lst[ind])

    return mass


@app.get("/pizdec")
def getInfo(date: datetime.date = '2023-03-27'):
    window_high = random.randint(10, 150)
    window_low = window_high - 10

    #################
    # DTP predictions
    model_dtp = joblib.load("Models/DTP.joblib")
    X_preds_dtp = pd.read_csv('Data/X_DTP.csv')[window_low:window_high]

    y_preds_dtp = model_dtp.predict(X_preds_dtp)

    risk_factor_dtp = 0
    accident_percent = sum(sum(y_preds_dtp)) / (len(y_preds_dtp) * len(y_preds_dtp[0]))

    y_preds_dtp = dtp_to_class_str(y_preds_dtp)

    if accident_percent <= 0.3:
        risk_factor_dtp = 0
    elif 0.3 < accident_percent <= 0.7:
        risk_factor_dtp = 1
    else:
        risk_factor_dtp = 2

    #################
    # GKH predictions
    model_gkh = joblib.load("Models/GKH.joblib")
    X_preds_gkh = pd.read_csv('Data/GKH.csv')[window_low:window_high]
    X_preds_gkh = X_preds_gkh[X_preds_gkh.columns[1:]]

    y_preds_gkh, p_eval = model_gkh.predict(X_preds_gkh, return_winning_probability=True)

    for i in range(len(y_preds_gkh)):
        if y_preds_gkh[i] == "Аварии на электроэнергетических системах ":
            y_preds_gkh[i] = "Аварии на эл.-энерг. системах "

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
                        dates[0]: ", ".join(y_preds_dtp[0]),
                        dates[1]: ", ".join(y_preds_dtp[1]),
                        dates[2]: ", ".join(y_preds_dtp[2]),
                        dates[3]: ", ".join(y_preds_dtp[3]),
                        dates[4]: ", ".join(y_preds_dtp[4]),
                        dates[5]: ", ".join(y_preds_dtp[5]),
                        dates[6]: ", ".join(y_preds_dtp[6]),
                        dates[7]: ", ".join(y_preds_dtp[7]),
                        dates[9]: ", ".join(y_preds_dtp[8]),
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
                        dates[0]: y_preds_gkh[0],
                        dates[1]: y_preds_gkh[1],
                        dates[2]: y_preds_gkh[2],
                        dates[3]: y_preds_gkh[3],
                        dates[4]: y_preds_gkh[4],
                        dates[5]: y_preds_gkh[5],
                        dates[6]: y_preds_gkh[6],
                        dates[7]: y_preds_gkh[7],
                        dates[8]: y_preds_gkh[8],
                        dates[9]: y_preds_gkh[9],

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

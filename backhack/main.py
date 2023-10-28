import random

from fastapi import FastAPI, File, UploadFile, Response
import datetime
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI(
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
def setPlace(place:str):
    return {"message":"place upload succefsully"}


@app.post("/upload")
def upload(file: UploadFile=File(...)):
    try:
        contents=file.file.read()
        print( contents)
        with open(file.filename,'wb') as f:
            f.write(contents)
    except Exception:
        return {"message":"there was an error uploading file"}
    finally:
        file.file.close()

    return {"message":f"Successfuly uploaded {file.filename}"}

def zap (arr):
    for i in range (0,6):
        for j in range(0,10):
            arr[i][j]=random.randint(0,1)
    return arr


@app.get("/pizdec")
def getInfo(date:datetime.date='2023-03-28'):
    dates=[]
    values=[0,1]
    counts=[[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    counts=zap(counts)
    first_date= date
    dates.append(first_date)
    for i in range(1,10):
        dates.append(dates[i-1]+datetime.timedelta(days=1))
    templates={"event":
                   {"dtp":
                        {dates[0]:counts[0][0],
                         dates[1]:counts[0][1],
                         dates[2]:counts[0][2],
                         dates[3]:counts[0][3],
                         dates[4]:counts[0][4],
                         dates[5]:counts[0][5],
                         dates[6]:counts[0][6],
                         dates[7]:counts[0][7],
                         dates[8]:counts[0][8],
                         dates[9]:counts[0][9],
                         "probability":0 if sum(counts[0])<4 else 1 if sum(counts[0])>3 and sum(counts[0])<7 else 2},
                    "toxic":
                        {dates[0]:counts[1][0],
                         dates[1]:counts[1][1],
                         dates[2]:counts[1][2],
                         dates[3]:counts[1][3],
                         dates[4]:counts[1][4],
                         dates[5]:counts[1][5],
                         dates[6]:counts[1][6],
                         dates[7]:counts[1][7],
                         dates[8]:counts[1][8],
                         dates[9]:counts[1][9],
                        "probability":0 if sum(counts[1])<4 else 1 if sum(counts[1])>3 and sum(counts[1])<7 else 2},
                    "natural":
                        {dates[0]:counts[2][0],
                         dates[1]:counts[2][1],
                         dates[2]:counts[2][2],
                         dates[3]:counts[2][3],
                         dates[4]:counts[2][4],
                         dates[5]:counts[2][5],
                         dates[6]:counts[2][6],
                         dates[7]:counts[2][7],
                         dates[8]:counts[2][8],
                         dates[9]:counts[2][9],
                         "probability": 0 if sum(counts[2]) < 4 else 1 if sum(
                             counts[2]) > 3 and sum(counts[2]) < 7 else 2},
                    "GKH":
                        {dates[0]:counts[3][0],
                         dates[1]:counts[3][1],
                         dates[2]:counts[3][2],
                         dates[3]:counts[3][3],
                         dates[4]:counts[3][4],
                         dates[5]:counts[3][5],
                         dates[6]:counts[3][6],
                         dates[7]:counts[3][7],
                         dates[8]:counts[3][8],
                         dates[9]:counts[3][9],
                         "probability": 0 if sum(counts[3]) < 4 else 1 if sum(
                             counts[3]) > 3 and sum(counts[3]) < 7 else 2},
                    "explosions":
                        {dates[0]:counts[4][0],
                         dates[1]:counts[4][1],
                         dates[2]:counts[4][2],
                         dates[3]:counts[4][3],
                         dates[4]:counts[4][4],
                         dates[5]:counts[4][5],
                         dates[6]:counts[4][6],
                         dates[7]:counts[4][7],
                         dates[8]:counts[4][8],
                         dates[9]:counts[4][9],
                         "probability": 0 if sum(counts[4]) < 4 else 1 if sum(
                             counts[4]) > 3 and sum(counts[4]) < 7 else 2},
                    "another":
                        {dates[0]:counts[5][0],
                         dates[1]:counts[5][1],
                         dates[2]:counts[5][2],
                         dates[3]:counts[5][3],
                         dates[4]:counts[5][4],
                         dates[5]:counts[5][5],
                         dates[6]:counts[5][6],
                         dates[7]:counts[5][7],
                         dates[8]:counts[5][8],
                         dates[9]:counts[5][9],
                         "probability": 0 if sum(counts[5]) < 4 else 1 if sum(
                             counts[5]) > 3 and sum(counts[5]) < 7 else 2},
                    }
               }
    return templates
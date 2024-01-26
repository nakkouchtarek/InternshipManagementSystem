#!/home/user/Stuff/pythonml/env/bin/python

import os
from pathlib import Path
import aiofiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, File, Form, HTTPException, Request, BackgroundTasks, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pymongo, json, base64
from gridfs import GridFS
from bson import ObjectId
from fastapi import BackgroundTasks
from StatisticGenerator import StatisticGenerator
from FileProcessor import FileProcessor
import asyncio

stats = StatisticGenerator()
processor = FileProcessor()

db = pymongo.MongoClient("mongodb://localhost:27017/").ftest

app = FastAPI()

app.mount("/html", StaticFiles(directory="html"), name="html")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/graphs", StaticFiles(directory="graphs"), name="graphs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def scheduled_task():
    while True:
        stats.generate_graphs()
        await asyncio.sleep(24 * 60 * 60)

def save_file(file_path: str, studentId: str, reportId: str, content: bytes):
    with open(file_path, 'wb') as out_file:
        out_file.write(content)

    processor.file_extract(file_path, studentId, reportId)

    os.remove(file_path)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(scheduled_task())

@app.get("/")
def read_root():
    html_path = Path("html") / "index.html"
    return FileResponse(html_path)

@app.get("/search")
def read_root(request: Request, keywords: str, year: str, theme: str, company: str):
    authorization = request.headers.get("authorization").split(" ")[1]
    decoded = jwt.decode(authorization,"secret","HS256")

    collection = db.Internships
    students = db.Students

    query = {}

    if decoded['type'] != 'admin': query["student_id"] = students.find_one({"studentName":decoded['username']})['_id']
    if company and company != "all": query["company_name"] = company
    if theme and theme != "all": query["theme"] = theme

    if keywords:
        ids = []

        for student in students.find():
            if keywords.lower() in student["studentName"].lower():
                ids.append(student["_id"])

        field_conditions = []

        for field in db.Internships.find_one().keys():
            field_conditions.append({field: {"$regex": f".*{keywords}.*", "$options": "i"}})

        query["$or"] = [{"student_id": {"$in": ids}}, {"$or": field_conditions}]


    if year and year != "all":
        search_year = int(year)
        query["$and"] = [
            {"start_date": {"$lte": f"{search_year}-12-31"}},
            {"end_date": {"$gte": f"{search_year}-01-01"}}
        ]

    result = collection.find(query)

    d = {}

    for i,doc in enumerate(result):
        d[i] = doc

        d[i]['studentName'] = students.find_one({"_id": d[i]['student_id']})['studentName']

        if 'reportId' in d[i]:
            d[i]['reportId'] = str(d[i]['reportId'])
        else:
            d[i]['reportId'] = "65b332e670f5da90b9a70084"

        del d[i]['student_id']
        del d[i]['_id']
    
    return d


fs = GridFS(db, collection='reports')

@app.get("/get_document/")
def get_image(id: str):
    try:
        # Retrieve file from GridFS
        file = fs.get(ObjectId(id))

        if file is None:
            raise HTTPException(status_code=404, detail="Image not found")

        # read image
        image_content = file.read()

        # encode to base64
        base64_content = base64.b64encode(image_content).decode("utf-8")

        return {"filename": file.filename, "data": base64_content}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/get_documents/")
def get_all_documents(request: Request):
    try:
        authorization = request.headers.get("authorization").split(" ")[1]
        decoded = jwt.decode(authorization,"secret","HS256")
        
        collection = db.reports

        if decoded['type'] == 'admin':
            documents_info = [{"id": str(document['fileId']), "name": document['fileName'], "student":document['studentName']} for document in collection.find()]
        else:
            documents_info = [{"id": str(document['fileId']), "name": document['fileName'], "student":document['studentName']} for document in collection.find() if document['studentName'] == decoded['username']]

        return {"documents": documents_info}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.post("/uploadfile/")
async def upload_file(
    request: Request, 
    file: UploadFile = File(...), 
    year: str = Form(...), 
    file_type: str = Form(...), 
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    authorization = request.headers.get("authorization").split(" ")[1]
    decoded = jwt.decode(authorization,"secret","HS256")

    students = db.Students

    content = await file.read()

    report_id = fs.put(content, filename=file.filename, uploadDate=datetime.utcnow())

    background_tasks.add_task(save_file, f"./uploads/{file.filename}", students.find_one({"studentName":decoded['username']})['_id'], report_id, content)

    report_document = {
        "studentName": decoded['username'],
        "year": int(year),
        "fileType": file_type,
        "fileName": file.filename,
        "fileId": report_id
    }

    reports_collection = db['reports']
    reports_collection.insert_one(report_document)

@app.get("/get_companies")
def read_root():
    collection = db.Internships

    d = set()
    
    for doc in collection.find():
        if doc['company_name'] != '':
            d.add(doc['company_name'])

    return d

@app.get("/get_themes")
def read_root():
    collection = db.Internships

    d = set()
    
    for doc in collection.find():
        if doc['theme'] != '':
            d.add(doc['theme'])
        
    return d

@app.post("/login/")
async def login(request: Request):
    try:
        data = await request.json()
        username = data['username']
        password = data['password']

        collection = db.users

        data = collection.find({})

        for document in data: 
            details = document['details']

            if username == details['username'] and password == details['password']:
                
                future_datetime = datetime.now() + timedelta(hours=24)
                future_datetime = future_datetime.strftime("%Y-%m-%d %H:%M:%S")
                encoded_jwt = jwt.encode({"expiration":f"{future_datetime}", "userId":document['userId'], "type":document['details']['type'], "username":document['details']['username']}, "secret", algorithm="HS256")

                return {"token":encoded_jwt}
        
        return {"token":""}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/register/")
async def check_validity(request: Request):
    received = await request.json()

    collection = db.users

    data = collection.find({})

    for document in data: 
        details = document['details']
        
        if details['username'] == received['username']:
            return {"state":"User already exits"}

    latest_document = collection.find_one(sort=[("_id", pymongo.DESCENDING)])

    if latest_document:
        latest_document = int(latest_document.get('userId', 0)) + 1
    else:
        latest_document = 1

    collection.insert_one({
        "userId": str(latest_document),
        "details": {
        "username": received['username'],
        "password": received['password'],
        "year": received['year'],
        "type": "student",
        "graduation": int(received['year'])+5
    }
    })

    collection = db.Students

    collection.insert_one({
        "studentName": received['username'],
        "year": received['year'],
        "promot": int(received['year'])+5
    })

    return {"state":"created"}

@app.post("/check_validity/")
async def check_validity(background_tasks: BackgroundTasks, request: Request):
    data = await request.json()

    exp = jwt.decode(data['token'],"secret","HS256")

    if datetime.strptime(exp['expiration'], "%Y-%m-%d %H:%M:%S") > datetime.now():
        return {"type":exp['type'], 'username':exp['username']}
    else:
        print("exp")
        return {"type":"expired", 'username':''}
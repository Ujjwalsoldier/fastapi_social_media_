from datetime import datetime,timedelta
import os
from fastapi.encoders import jsonable_encoder
from pathlib import Path
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from fastapi import FastAPI,Request,Response,Depends,status,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List , Optional
from db import users
#Token-based (JWT with APIs)
from fastapi_login import LoginManager
#psassword hashing 
from passlib.context import CryptContext

# load_dotenv()
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
SECRET_KEY= os.getenv('SECRET_KEY')
# print(SECRET_KEY)
ACCESS_TOKEN_EXPIRES_MINUTES = 60

# print("SECRET_KEY:", SECRET_KEY)

# manager = LoginManager(
#     secret=SECRET_KEY.encode(),
#     token_url="/login",
#     use_cookie=True,
#     custom_exception=NotAuthenticatedException  
# )
class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(secret=SECRET_KEY, token_url="/login", use_cookie=True)
manager.cookie_name="auth"


@manager.user_loader()
def get_user_from_db(username:str):
    # import pdb;pdb.set_trace()
    if username in users.keys():
        return UserDB(**users[username])
    
def authenticate_user(username:str , password:str):
    # import pdb;pdb.set_trace()
    user = get_user_from_db(username=username)
    if not user:
        return None
    if not verify_password(plain_password=password,hashed_password=user.hashed_password):
        return None
    return user
#Yeh passlib library ka ek class hai.
# CryptContext ek password security ka manager hai.
# Isse tum multiple hashing algorithms use kar sakte ho (jaise bcrypt, sha256_crypt, etc.).
# Iska kaam: hashing karna aur baad me verify bhi karna ki password sahi hai ya nahi.       
pwd_ctx = CryptContext(schemes=["bcrypt"],deprecated="auto")

#two funtions with hashed password 
def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)

def verify_password(plain_password,hashed_password):
    return pwd_ctx.verify(plain_password,hashed_password)

# print(get_hashed_password("password"))
print(verify_password("password",get_hashed_password("password")))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

class Notification(BaseModel):
    author:str
    description:str


class User(BaseModel):
    name:str
    username:str
    email:str
    birthday:Optional[str]= None
    friends:Optional[List[str]]=[]   
    notification: Optional[List[Notification]] =[]


class UserDB(User):
    hashed_password:str    

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Ab yeh absolute path use karega
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def root(request:Request):
    return templates.TemplateResponse("index.html",{"request":request , "title":"FriendConnect -Home "})

@app.get("/login",response_class=HTMLResponse)
def get_login(request:Request):
    return templates.TemplateResponse("login.html",{"request":request,"title":"FriendConnect -Login"})

@app.post("/login")
# def login(request:Request,response:Response,form_data: OAuth2PasswordRequestForm=Depends(OAuth2PasswordRequestForm)):
def login(request: Request, response:Response,form_data: OAuth2PasswordRequestForm = Depends()):

# def login(request:Request,response:Response,form_data: OAuth2PasswordRequestForm = Depends()):
    #import pdb;pdb.set_trace()

    user=authenticate_user(username=form_data.username,password=form_data.password)
    
    if not user:
        return templates.TemplateResponse("login.html",{"request":request,"title":"FriendConnect -Login" , "invalid":True},status_code=status.HTTP_401_UNAUTHORIZED)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = manager.create_access_token(
        data={"sub":user.username},
        expires=access_token_expires
    )
    resp =RedirectResponse("/home",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    return resp

# class NotAuthenticatedException(Exception):
#     pass

def not_authenticated_exception_handeler(request,exception):
    return RedirectResponse("/login")

app.add_exception_handler(NotAuthenticatedException,not_authenticated_exception_handeler)
@app.get("/home")
def home(request:Request,user:User=Depends(manager)):
    user=User(**dict(user))
    return templates.TemplateResponse("home.html",{"request":request,"title":"friendConnect - Home","user":user})

# import pdb;pdb.set_trace()
@app.get("/logout")
def logout():
    response = RedirectResponse("/")
    manager.set_cookie(response,None)
    return response

@app.get("/register",response_class=HTMLResponse)
def get_register(request:Request):
    return templates.TemplateResponse("register.html",{"request":request,"title" : "FriendConnect -Register", "invalid":False })

# @app.get("/register", response_class=HTMLResponse)
# def get_register():
#     return HTMLResponse("<h1>Register Page</h1>")   

@app.post("/register")
def register(request:Request,username:str = Form(...), name:str = Form(...),password:str = Form(...),email:str = Form(...)):
    hashed_password = get_hashed_password(password)
    invalid = False
    for db_username in users.keys():
        if username == db_username:
            invalid = True
        elif users[db_username]["email"] == email:
            invalid = True

    if invalid :
        return templates.TemplateResponse("register.html",{"request":request,"title" : "FriendConnect -Register", "invalid":True },status_code=status.HTTP_400_BAD_REQUEST)
    users[username] = jsonable_encoder(UserDB(username=username,email=email,name=name,hashed_password=hashed_password))
    
    response = RedirectResponse("/login",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(response,None) 

    return response   



@app.get("/user")
def get_jadkhalili(request: Request , username:str, response_class):

    for i in users.keys():
        if i ==  'jadkhalili':
            return HTMLResponse(i)
        

    
    



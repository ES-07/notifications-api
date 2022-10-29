import email
from msilib.schema import MIME
from fastapi import FastAPI
from api.models import Intrusion
import httpx
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header


app = FastAPI()

client = httpx.AsyncClient()

@app.get("/")
def alive():
    return {'message': 'Notifications API is alive!'}

@app.post("/intrusion/")
async def create_item(intrusion: Intrusion):
    print("Intrusion received:")
    print(intrusion)
    intrusion_dict = intrusion.dict()
    camera_id = intrusion_dict.camera_id
    email = request_email(client, camera_id)
    send_email(intrusion_dict)
    return intrusion

async def request_email(client, camera_id):
    print(f"Requesting email for the camera {camera_id}")
    response = await client.get(f"sites-api/{camera_id}")
    return response.text

def send_email(intrusion_dict):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    
    information = f"NEW INTRUSION DETECTED AT {intrusion_dict.timestamp} | FRAME: {intrusion_dict.frame_id} | CAMERA: {intrusion_dict.camera_id}\nThis is an automatic message!"
    msg = MIMEText(information, 'plain', 'utf-8')

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = Header("Intrusion detected!", 'utf-8')
    msg['From'] = "cctv-es007@gmail.com"
    msg['To'] = email

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail("cctv-es007@gmail.com", [email], msg.as_string())
    s.quit()
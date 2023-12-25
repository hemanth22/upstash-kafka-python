from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os

app = FastAPI()

class EmailData(BaseModel):
    to_email: str
    subject: str
    bodyhtml: str

@app.post("/send-email")
async def send_email(request: Request, email_data: EmailData):
    try:
        # Accessing the raw JSON payload
        raw_json = await request.json()
        print("Raw JSON:", raw_json)

        # Parsing the JSON data
        to_email = email_data.to_email
        subject = email_data.subject
        bodyhtml = email_data.bodyhtml

        # Sending the email
        send_email(to_email, subject, bodyhtml)

        return {"message": "Email sent successfully"}
    except Exception as e:
        # Handling potential errors
        raise HTTPException(status_code=500, detail="Internal Server Error")

def send_email(to_email, subject, bodyhtml):
    API_KEY_HELPER = os.environ.get('API_KEY_HELPER')
    SMTP_URL_FINAL = os.environ.get('SMTP_URL_FINAL')
    SMTP_PORT = os.environ.get('SMTP_PORT')
    sender_email = "hemanth22hemu@gmail.com"

    # Create the MIME object
    # msg = MIMEMultipart()
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach the HTML message
    text = bodyhtml
    html = bodyhtml

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_URL_FINAL, SMTP_PORT) as server:
        server.starttls()
        server.login(sender_email, API_KEY_HELPER)
        server.sendmail(sender_email, to_email, message.as_string())
        print("Email sent successfully!")
        server.quit()
        print("Connection Closed")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

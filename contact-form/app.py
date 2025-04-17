import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from opentelemetry import trace
import logging

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add a basic stream handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(handler)

tracer = trace.get_tracer(__name__)

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the frontend URL here instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email API route
@app.post("/email")
async def email(request: Request):
    messageContents = await request.json()
    message = Mail(
        to_emails="os.environ.get('SENDGRID_TO_EMAIL')",
        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
        subject=messageContents["subject"],
        html_content= f"{messageContents["message"]}<br />{messageContents["name"]}")
    message.reply_to = messageContents["email"]

    try:
        logger.info("Sending email...")
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        
        logger.info(f"Email sent with status code: {response.status_code}")
        return response
    except Exception as e:
        logger.exception(f"Email sending failed: {e}")
        return e

# Serve static files (the microfrontend build)
app.mount("/", StaticFiles(directory="./dist", html=True), name="static")

# Run the app locally (if needed)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

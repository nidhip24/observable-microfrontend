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
logger.setLevel(logging.INFO)

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
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("send_email") as span:
        try:
            messageContents = await request.json()
            span.set_attribute("email.subject", messageContents.get("subject", ""))
            span.set_attribute("email.from", messageContents.get("email", "unknown"))

            message = Mail(
                to_emails=os.environ.get('SENDGRID_TO_EMAIL'),
                from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
                subject=messageContents["subject"],
                html_content=f'{messageContents["message"]}<br />{messageContents["name"]}'
            )
            message.reply_to = messageContents["email"]

            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)

            logger.info("Email sent successfully.")
            return {
                "status_code": response.status_code,
                "body": response.body.decode() if response.body else "",
                "headers": dict(response.headers)
            }

        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to send email")

# Serve static files (the microfrontend build)
app.mount("/", StaticFiles(directory="./dist", html=True), name="static")

# Run the app locally (if needed)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

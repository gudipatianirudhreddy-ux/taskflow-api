import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_group_invitation(
    to_email: str,
    inviter_email: str,
    group_name: str,
    accept_url: str
):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_email or not smtp_password:
        raise ValueError("SMTP_EMAIL and SMTP_PASSWORD environment variables must be set.")

    subject = f"You're invited to join {group_name}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 30px auto;
                background-color: #ffffff;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            }}
            h2 {{
                color: #1a202c;
                margin-top: 0;
            }}
            p {{
                color: #4a5568;
                font-size: 16px;
                line-height: 1.5;
            }}
            .button-container {{
                margin: 25px 0;
                text-align: center;
            }}
            .btn {{
                background-color: #4f46e5;
                color: #ffffff !important;
                padding: 12px 24px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 6px;
                display: inline-block;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 13px;
                color: #a0aec0;
                border-top: 1px solid #e2e8f0;
                padding-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>You're invited to join {group_name}</h2>
            <p><strong>{inviter_email}</strong> has invited you to collaborate in <strong>{group_name}</strong>.</p>
            <p>Click the button below to accept the invitation and join the group:</p>
            <div class="button-container">
                <a href="{accept_url}" class="btn" target="_blank">Accept Invitation</a>
            </div>
            <p class="footer">Please note: This invitation link will expire in 7 days.</p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())

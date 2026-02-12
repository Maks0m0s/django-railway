import smtplib

try:
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
    server.starttls()
    server.quit()
    print("Connection successful!")
except Exception as e:
    print("Cannot connect:", e)
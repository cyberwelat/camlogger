import cv2
import time
import smtplib
import os
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "" #fotoğrafları gönderecek mail adresi
EMAIL_PASSWORD = "" #app password
EMAIL_RECEIVER = "" #mail gönderilecek adres

def send_email(filenames):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = "Yeni Fotoğraflar"
        msg.set_content("Ekli dosyalarda çekilen fotoğrafları bulabilirsiniz.")

        for file in filenames:
            with open(file, "rb") as f:
                msg.add_attachment(f.read(), maintype="image", subtype="png", filename=file)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print(f"Send hatası: {e}")

def delete_photos(filenames):
    for file in filenames:
        if os.path.exists(file):
            os.remove(file)

cap = cv2.VideoCapture(0)
photo_files = []

for i in range(1, 6): #çekilcek fooğraf sayısı (var sayılan 5) (10 fotoğraf için 6 yerine 11 yazın)
    ret, frame = cap.read()
    if ret:
        filename = f'okked{i}.png'
        cv2.imwrite(filename, frame)
        photo_files.append(filename)
    if i < 5:
        time.sleep(5) #fotoğraf çekme aralığı (var sayılan 3 saniye)

cap.release()
send_email(photo_files)
delete_photos(photo_files)

# Editer : Luca_yao
# E-mail : stelliva42@gmail.com
# Date : 2024/02/06

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(USER):
    
    cleaned_user = USER.replace("_2", "").replace("_3", "")
    
    sender_email = "example@outlook.com"
    receiver_email = f"{cleaned_user}@outlook.com"
    subject = f"【MIS通報】{USER} 您的VPN已到期"
    body = f"{USER} 您的VPN使用權限日期已到期\n\n因應ISO27001資安規範，VPN權限以半年為限\n\n資訊處每年六月及十二月 將重新審視，公告通知\n\n為避免影響到同仁，如有使用VPN需求，請再填寫《VPN申請單》 重新申請 \n\n如有其他特殊需求，請與資訊處OA聯繫，感謝您的配合。\n\nMIS@outlook.com"
                
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    smtpobj = smtplib.SMTP("mail.protection.outlook.com", 25)
    smtpobj.sendmail(sender_email, receiver_email, message.as_string())

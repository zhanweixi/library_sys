import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apps.library.models import BorrowModel, BooksModel, LibraryUser
from celery import shared_task


# Create your tests here.

@shared_task
def return_reminder():
    now_date = datetime.datetime.now()
    reminder_date = now_date + datetime.timedelta(days=7)
    queryset = BorrowModel.objects.filter(max_getDate__lte=reminder_date)
    try:
        for obj_ in queryset:
            book_id = obj_.book_id
            reader_id = obj_.reader_id
            book_obj = BooksModel.objects.filter(ISBN=book_id).first()
            reader_obj = LibraryUser.objects.filter(code=reader_id).first()
            mail_msg = "尊敬的用户{}, 你借阅的图书《{}》归还时间还有不足7天到期, 请及时归还。".format(reader_obj.name,
                                                                                                   book_obj.name)
            receivers_email = reader_obj.email
            send_email(receivers_email=receivers_email, mail_msg=mail_msg)
    except Exception as e:
        print(str(e))


def send_email(receivers_email, mail_msg):
    # 邮件信息
    smtp_host = "smtp.qq.com"
    sender_email = 'xxx@139.com'
    mail_pass = "xxxxx"  # " # SMTP授权码
    # 编辑邮件
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receivers_email
    message['Subject'] = '图书订阅过期提醒'
    message.attach(MIMEText(mail_msg, "plain"))
    try:
        smtpObj = smtplib.SMTP(smtp_host, 25)
        smtpObj.starttls()  # 25 为 SMTP 端口号
        smtpObj.login(sender_email, mail_pass)
        smtpObj.sendmail(sender_email, receivers_email, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

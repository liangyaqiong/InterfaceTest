import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Config import settings
from Utils.local_config_utils import LocalConfig




class EmailUtils:

    def __init__(self,smtp_body,smtp_attach_path=None):
        self.smtp_body = smtp_body
        self.smtp_attach_path = smtp_attach_path
        self.smtp_server = LocalConfig.smtp_server
        self.smtp_receiver = LocalConfig.smtp_receiver
        self.smtp_smtp_key = LocalConfig.smtp_key
        self.smtp_cc = LocalConfig.smtp_cc
        self.smtp_sender = LocalConfig.smtp_sender
        self.smtp_subject = LocalConfig.smtp_subject

    def mail_send_body(self):
        message = MIMEMultipart()
        message['from'] = self.smtp_sender
        message['to'] = self.smtp_receiver
        message['Cc'] = self.smtp_cc   #抄送
        message['subject'] = self.smtp_subject #邮件正文
        #附件内容设置
        message.attach(MIMEText(self.smtp_body,'html','utf-8'))
        #添加附件
        if self.smtp_attach_path:
           attach_file = MIMEText(open(self.smtp_attach_path,'rb').read(),'base64', 'utf-8')
           attach_file.add_header('Content-Disposition', 'attachment',filename = ('UTF-8','',os.path.basename(self.smtp_attach_path))) #os.path.basename(self.smtp_attach_path) 此句是获取到文件名
           message.attach(attach_file)
        return message

    def email_send(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_server)
        smtp.login(self.smtp_sender,self.smtp_smtp_key)
        smtp.sendmail(self.smtp_sender,self.smtp_receiver.split(',')+self.smtp_sender.split(','),self.mail_send_body().as_string())


if __name__=='__main__':
    smtp_attach_path = os.path.join(settings.reports_path,'API_TEST_V1.0\API_TEST_V1.0.html')
    print()
    EmailUtils('<h3 align="center">自动化测试报告</h3>',smtp_attach_path).email_send()






import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr 
import logger


LOG_MODULE = 'System'
AUTH_MAIL = 'inforassistant@foxmail.com' 
AUTH_MAIL_PASS = 'yinszohqhigbdaef'


def send_message(mail,word):
    ''' send email 发邮件
    :params mail: Return address 收信人地址
    :params word: Content sent 发送的内容
    '''
    def sentmail():
        ret=True
        try:
            msg = MIMEMultipart()
            html_att = MIMEText(word, 'html', 'utf-8')
            att=MIMEText(word,'plain','utf-8')
            msg.attach(html_att)
            msg.attach(att)
            msg['From']=formataddr(["IIA",AUTH_MAIL])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["Friend",mail])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="IIA 验证码"                        # 邮件的主题，也可以说是标题
        
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25 465
            server.login(AUTH_MAIL, AUTH_MAIL_PASS)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(AUTH_MAIL,[mail,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret=False
        return ret
    
    #my_sender= AUTH_MAIL  # 发件人邮箱账号
    #my_pass = AUTH_MAIL_PASS     # 发件人邮箱密码
    #my_user=mail                     # 收件人邮箱账号
    logger.info("Start sending mail",LOG_MODULE)
    if sentmail():logger.info("Sent mail successfully",LOG_MODULE)
    else: logger.info("Failed to send mail",LOG_MODULE) 



import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders
from typing import Union, List, Tuple


def send_email(smtp_server: str,
               smtp_port: int,
               from_email: str,
               from_password: str,
               title: str,
               body: str,
               to_emails: Union[List[str], Tuple[str], str],
               from_name: str = None,
               ssl=True,
               to_cc_mails: Union[List[str], Tuple[str], str, None] = None,
               attachments: Union[List[str], Tuple[str], str, None] = None):
    """发送邮件功能, 支持抄送、附件, 目前仅支持 html 渲染的 body 样式

    Args:
        smtp_server: SMTP 服务器域名, 例如: smtp.feishu.cn
        smtp_port: SMTP 服务器端口, 例如: 465
        from_email: 发件人邮箱, 例如: xxx@xxx.com
        from_password: 发件人密码
        from_name: 发件人名称
        ssl: 是否使用SMTP_SSL连接服务器
        title: 邮件主题
        body: 邮件正文
        to_emails: 收件人, 支持多个收件人
        to_cc_mails: 抄送人, 支持多个抄送人
        attachments: 附件, 支持多个附件, 附件的绝对路径或相对路径

    Raises:
        SMTPException: 发送邮件异常
    """
    message = MIMEMultipart()
    # 主题
    message['Subject'] = Header(title, 'utf-8')
    # 发件人
    message['From'] = formataddr(
        (from_name, from_email), 'utf-8')
    # 抄送人
    if isinstance(to_cc_mails, (tuple, list)):
        to_cc_mails = ','.join(to_cc_mails)
    message['Cc'] = to_cc_mails
    # 邮件正文
    message.attach(MIMEText(body, 'html'))
    # 附件
    if attachments:
        if isinstance(attachments, str):
            attachments = [attachments]
        for attachment in attachments:
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = attachment.split(os.sep)[-1]
            part.add_header('Content-Disposition',
                            f'attachment; filename= {filename}')
            message.attach(part)

    # 连接服务器发送邮件
    if ssl:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)
    server.login(from_email, from_password)
    server.send_message(message, from_email, to_emails)


class SmtpEmailNotice:
    """
    邮件通知工具
    """

    def __init__(self,
                 smtp_server: str,
                 smtp_port: int,
                 from_email: str,
                 from_password: str,
                 from_name: str = None,
                 ssl=True, ):
        """
        Args:
            smtp_server: SMTP 服务器域名, 例如: smtp.feishu.cn
            smtp_port: SMTP 服务器端口, 例如: 465
            from_email: 发件人邮箱, 例如: xxx@xxx.com
            from_password: 发件人密码
            from_name: 发件人名称
            ssl: 是否使用SMTP_SSL连接服务器
        """
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._from_email = from_email
        self._from_password = from_password
        self._from_name = from_name if from_name else from_email
        self._ssl = ssl

    def send_email(self,
                   title: str,
                   body: str,
                   to_emails: Union[List[str], Tuple[str], str],
                   to_cc_mails: Union[List[str], Tuple[str], str, None] = None,
                   attachments: Union[List[str], Tuple[str], str, None] = None):
        """发送邮件功能, 支持抄送、附件, 目前仅支持 html 渲染的 body 样式

        Args:
            title: 邮件主题
            body: 邮件正文
            to_emails: 收件人, 支持多个收件人
            to_cc_mails: 抄送人, 支持多个抄送人
            attachments: 附件, 支持多个附件, 附件的绝对路径或相对路径

        Raises:
            SMTPException: 发送邮件异常
        """
        return send_email(smtp_server=self._smtp_server,
                          smtp_port=self._smtp_port,
                          from_email=self._from_email,
                          from_password=self._from_password,
                          title=title,
                          body=body,
                          to_emails=to_emails,
                          from_name=self._from_name,
                          ssl=self._ssl,
                          to_cc_mails=to_cc_mails,
                          attachments=attachments)

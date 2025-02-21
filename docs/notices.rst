通知服务
========

Seatools 提供了多种通知服务工具。

邮件通知
--------

使用 SMTP 发送邮件:

.. code-block:: python

   from seatools.notices import SmtpEmailNotice
   from seatools.builders import HtmlBuilder

   notice = SmtpEmailNotice(
       smtp_server='smtp.example.com',
       smtp_port=465,
       from_email='sender@example.com',
       from_password='password',
       from_name='Sender'
   )

   # 发送HTML邮件
   notice.send_email(
       '测试标题',
       HtmlBuilder(auto_add_html_tag=True)
           .h1('正文标题')
           .p('正文内容')
           .a('链接', 'https://example.com'),
       to_emails=['receiver@example.com'],
       to_cc_mails=['cc@example.com'],
       attachments=['file.txt']
   )

飞书机器人
---------

支持文本、富文本、卡片等多种消息格式:

.. code-block:: python

   from seatools.notices import (
       FeishuRobotNotice,
       FeishuRobotTextMsg,
       FeishuRobotPostMsg,
       FeishuRobotCardMsgTemplate
   )

   notice = FeishuRobotNotice(
       webhook='webhook_url',
       secret='secret_key'
   )

   # 发送文本消息
   notice.send_msg(FeishuRobotTextMsg(text='测试消息'))

   # 发送富文本消息
   notice.send_msg(
       FeishuRobotPostMsg(
           title='测试标题',
           content=FeishuRobotPostMsg.content_builder()
               .add_text('测试文本')
               .add_a('测试链接', 'https://example.com')
               .add_at('all')
               .build()
       )
   )

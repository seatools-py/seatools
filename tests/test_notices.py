import pytest

from seatools.notices import SmtpEmailNotice, FeishuRobotNotice, FeishuRobotTextMsg, FeishuRobotPostMsg, \
    FeishuRobotCardMsg, FeishuRobotCardMsgTemplate
from seatools.builders import HtmlBuilder


@pytest.mark.skip()
def test_smtp_email_notice():
    notice = SmtpEmailNotice(smtp_server='smtp.feishu.cn',
                             smtp_port=465,
                             from_email='xxx@xxx.com',
                             from_password='123456',
                             from_name='测试邮箱')
    notice.send_email(title='测试邮件',
                      body=HtmlBuilder(auto_add_html_tag=True
                                       ).h1('测试标题').p('测试').a('测试链接', 'https://www.baidu.com').build(),
                      to_emails=['xxx@xxx.com'],
                      to_cc_mails=['xxx@xxx.com'],
                      attachments=[__file__])


@pytest.mark.skip()
def test_feishu_robot_notice():
    notice = FeishuRobotNotice('xxx',
                               'xxxx')
    # 测试普通消息
    notice.send_msg(FeishuRobotTextMsg(text='测试消息'))
    # 测试富文本消息
    notice.send_msg(FeishuRobotPostMsg(title='测试标题',
                                       content=FeishuRobotPostMsg.content_builder(
                                       ).add_text(
                                           '测试文本'
                                       ).add_a(
                                           '测试链接', 'https://www.baidu.com'
                                       ).add_newline().add_at(
                                           'all'
                                       ).build()))
    # 测试卡片消息
    # 使用卡片消息模板消息生成卡片消息发送(推荐)
    card_template = FeishuRobotCardMsgTemplate(elements=[
        {
            "tag": "div",
            "text": {
                "content": "{{content}}!xxxx",
                "tag": "lark_md"
            }
        }
    ], config={
        "wide_screen_mode": True
    }, header={
        "template": "blue",
        "title": {
            "content": "{{title}}",
            "tag": "plain_text"
        }
    })
    # 使用卡片模板card_template.gen_msg方法生成卡片消息并发送
    notice.send_msg(card_template.gen_msg(elements_map={'content': '测试内容'},
                                          header_map={'title': '测试标题'}))
    # 直接发送卡片消息
    notice.send_msg(FeishuRobotCardMsg(elements=[
        {
            "tag": "div",
            "text": {
                "content": "xxxx",
                "tag": "lark_md"
            }
        }
    ], config={
        "wide_screen_mode": True
    }, header={
        "template": "blue",
        "title": {
            "content": "xxxxx",
            "tag": "plain_text"
        }
    }))

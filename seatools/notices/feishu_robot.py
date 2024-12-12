import json
import time
from typing import Optional, Any, Union, Dict
import pydantic
import requests
from ..models import BaseModel
from ..cryptography import sha256_hmac, encode_base64
import re


class _FeishuRobotBaseMsg(BaseModel):

    def get_msg_type(self):
        raise NotImplementedError

    def to_json(self):
        return self.model_dump(exclude_none=True)


class FeishuRobotTextMsg(_FeishuRobotBaseMsg):
    """飞书机器人文本消息封装"""
    # 发送的文本内容
    text: str

    def get_msg_type(self):
        return 'text'


class FeishuRobotPostMsgTag(BaseModel):
    """飞书机器人富文本消息标签封装"""
    # 标签类型, 支持 text(文本), a(链接), at(艾特)
    tag: str
    # 文本消息
    text: Optional[str] = None
    # 表示是否 unescape 解码。默认值为 false，未用到 unescape 时可以不填
    un_escape: Optional[bool] = None
    # 链接地址
    href: Optional[str] = None
    # at目标的ID
    user_id: Optional[str] = None
    # at目标的用户名称
    user_name: Optional[str] = None
    """
    图片的唯一标识。可通过 上传图片 接口获取 image_key
    https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
    """
    image_key: Optional[str] = None


_FeishuRobotPostMsgContent = list


class FeishuRobotPostMsgContentBuilder:
    """
    飞书富文本消息内容建造器
    """

    def __init__(self):
        self._data = [[]]
        self._index = 0

    def add_text(self, text: str, un_escape: Optional[bool] = None):
        """添加一个text文本标签
        Args:
            text: 文本内容
            un_escape: 表示是否 unescape 解码。默认值为 false，未用到 unescape 时可以不填
        """
        self._data[self._index].append(
            FeishuRobotPostMsgTag(tag='text', text=text, un_escape=un_escape).model_dump(exclude_none=True))
        return self

    def add_a(self, text: str, href: str):
        """添加一个a超链接标签

        Args:
            text: 超链接的文本内容
            href: 默认的链接地址，你需要确保链接地址的合法性，否则消息会发送失败
        """
        self._data[self._index].append(
            FeishuRobotPostMsgTag(tag='a', text=text, href=href).model_dump(exclude_none=True))
        return self

    def add_at(self, user_id: str, user_name: Optional[str] = None):
        """添加一个at标签

        Args:
            user_id:
                用户的 Open ID 或 User ID。
                - @ 单个用户时，user_id字段必须是有效值（仅支持 @ 自定义机器人所在群的群成员）。
                - @ 所有人时，填 all。
            user_name: 用户名称
        """
        self._data[self._index].append(
            FeishuRobotPostMsgTag(tag='at', user_id=user_id, user_name=user_name).model_dump(exclude_none=True))
        return self

    def add_img(self, image_key):
        """添加一个img标签

        Args:
            image_key:
                图片的唯一标识。可通过 上传图片 接口获取 image_key
                https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
        """
        self._data[self._index].append(
            FeishuRobotPostMsgTag(tag='img', image_key=image_key).model_dump(exclude_none=True))
        return self

    def add_newline(self):
        """
        换行
        """
        self._data.append([])
        self._index += 1
        return self

    def build(self) -> _FeishuRobotPostMsgContent:
        """生成 FeishuRobotPostMsg.content 字段对象"""
        return self._data


class FeishuRobotPostMsg(_FeishuRobotBaseMsg):
    """飞书富文本消息封装
    Usage:
        FeishuRobotPostMsg(title='xxx',
                           content=FeishuRobotPostMsg.content_builder().add_text('xxxx').build()
        )
    """
    # 标题
    title: Optional[str] = None
    # 内容
    content: _FeishuRobotPostMsgContent

    def get_msg_type(self):
        return 'post'

    def to_json(self, lang='zh_cn'):
        return {'post': {lang: self.model_dump()}}

    @staticmethod
    def content_builder():
        return FeishuRobotPostMsgContentBuilder()


class FeishuRobotCardMsg(_FeishuRobotBaseMsg):
    """飞书机器人卡片消息
    建议使用飞书消息卡片搭建工具快速创建模板, 直接构建对象传参
    https://open.feishu.cn/tool/cardbuilder?templateId=ctp_AAYHcTkBGx0k
    """
    # 卡片消息体内容
    elements: list
    # 卡片消息配置
    config: Optional[dict] = None
    # 卡片消息标题
    header: Optional[dict] = None

    def get_msg_type(self):
        return 'interactive'


class FeishuRobotCardMsgTemplate(BaseModel):
    """飞书机器人卡片消息模板, 模板规则, 使用 {{}} 包裹的文本视为变量, 例如 {{name}} 表示变量name"""
    # 卡片消息文本
    elements: list
    # 卡片消息配置
    config: Optional[dict] = None
    # 卡片消息标题
    header: Optional[dict] = None

    def gen_msg(self, elements_map: Union[Dict[str, Any], pydantic.BaseModel, None] = None,
                header_map: Union[Dict[str, Any], pydantic.BaseModel, None] = None) -> FeishuRobotCardMsg:
        """通过模板生成消息配置

        Args:
            elements_map: 卡片消息模板名称与值的映射
            header_map: 卡片消息标题模板名称与值的映射
        """
        elements = json.dumps(self.elements, ensure_ascii=False)
        if elements_map:
            if isinstance(elements_map, pydantic.BaseModel):
                elements_map = elements_map.model_dump()
            for name, value in elements_map.items():
                elements = re.sub(
                    '{{\\s*?' + name + '\\s*?}}', str(value), elements)
        header = json.dumps(
            self.header, ensure_ascii=False) if self.header else None
        if header and header_map:
            if isinstance(header_map, pydantic.BaseModel):
                header_map = header_map.model_dump()
            for name, value in header_map.items():
                header = re.sub('{{\\s*?' + name + '\\s*?}}',
                                str(value), header)
        if elements:
            elements = json.loads(elements)
        if header:
            header = json.loads(header)
        return FeishuRobotCardMsg(elements=elements, config=self.config, header=header)


class _FeishuRobotFullMsg(BaseModel):
    # 消息类型
    msg_type: str
    # 普通文本、富文本消息内容
    content: Optional[Any] = None
    # 卡片消息内容 (与content二选一)
    card: Optional[Any] = None
    # 传递secret秘钥时必传时间戳校验
    timestamp: Optional[str] = None
    # 传递secret秘钥时必传校验sign
    sign: Optional[str] = None

    def set_msg(self, msg: _FeishuRobotBaseMsg):
        if isinstance(msg, (FeishuRobotTextMsg, FeishuRobotPostMsg)):
            self.content = msg.to_json()
        if isinstance(msg, FeishuRobotCardMsg):
            self.card = msg.to_json()


class FeishuRobotNotice:
    """
    飞书机器人通知工具
    """

    def __init__(self, webhook: str, secret: Optional[str] = None):
        """
        Args:
            webhook: 飞书webhook地址
            secret: 签名校验秘钥, 非必填
        """
        self._webhook = webhook
        self._secret = secret

    def _gen_sign(self, timestamp: Union[int, str]):
        """生成飞书的sign

        Args:
            timestamp: 秒级时间戳
        """
        # 先拼接串
        sec = f'{timestamp}\n{self._secret}'
        # base64 + sha256 hmac 编码
        return encode_base64(sha256_hmac(sec, encoding='utf-8')).decode('utf-8')

    def send_text_msg(self, text: str, timeout: Union[float, tuple] = None):
        """发送飞书机器人纯文本消息

        Args:
            text: 文本消息
            timeout: 可选, 发送消息超时时间, 支持float或者tuple2 (connection timeout, read timeout)
        """
        msg = FeishuRobotTextMsg(text=text)
        return self.send_msg(msg, timeout)

    def send_post_msg(self,
                      title: Optional[str] = None,
                      content_builder: FeishuRobotPostMsgContentBuilder = None,
                      timeout: Union[float, tuple] = None):
        """发送飞书机器人富文本消息

        Args:
            title: 富文本标题
            content_builder: 富文本内容建造器, 通过 FeishuRobotPostMsg.content_builder() 可获取Builder实例
            timeout: 可选, 发送消息超时时间, 支持float或者tuple2 (connection timeout, read timeout)
        """
        content = []
        if content_builder:
            content = content_builder.build()
        msg = FeishuRobotPostMsg(title=title, content=content)
        return self.send_msg(msg, timeout)

    def send_msg(self, msg: _FeishuRobotBaseMsg, timeout: Union[float, tuple] = None):
        """发送飞书机器人消息

        Args:
            msg: 飞书机器人消息
            timeout: 可选, 发送消息超时时间, 支持float或者tuple2 (connection timeout, read timeout)
        """
        # 初始化完整消息对象
        full_msg = _FeishuRobotFullMsg(msg_type=msg.get_msg_type())
        # 设置业务消息
        full_msg.set_msg(msg)
        # 有秘钥则补充sign校验相关参数
        if self._secret:
            full_msg.timestamp = str(int(time.time()))
            full_msg.sign = self._gen_sign(full_msg.timestamp)
        response = requests.post(self._webhook,
                                 json=full_msg.model_dump(exclude_none=True),
                                 timeout=timeout)
        if response.status_code != 200:
            raise Exception(
                '发送飞书机器人消息响应状态码异常, 状态码: {}, 响应信息: {}', response.text)
        return response.json()

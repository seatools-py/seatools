from typing import Union
from enum import Enum
from .base import BaseBuilder


class ATarget(Enum):
    SELF = '_self'
    BLANK = '_blank'
    PARENT = '_parent'
    TOP = '_top'


class HtmlBuilder(BaseBuilder):
    """HTML 标签建造器"""

    def __init__(self, auto_add_html_tag=False):
        self.html = ''
        self._tag_end = '\n'
        self._auto_add_html_tag = auto_add_html_tag

    def h1(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('h1', content_, **attrs)

    def h2(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('h2', content_, **attrs)

    def h3(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('h3', content_, **attrs)

    def h4(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('h4', content_, **attrs)

    def h5(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('h5', content_, **attrs)

    def h6(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('h6', content_, **attrs)

    def br(self):
        return self._common_tag('br')

    def b(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('b', content_, **attrs)

    def em(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('em', content_, **attrs)

    def i(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('i', content_, **attrs)

    def blockquote(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('blockquote', content_, **attrs)

    def code(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('code', content_, **attrs)

    def pre(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('pre', content_, **attrs)

    def p(self, content_: Union[str, 'HtmlBuilder'] = None, **attrs):
        return self._common_tag('p', content_, **attrs)

    def a(self, content_: Union[str, 'HtmlBuilder'] = None, href: str = '', target: Union[ATarget, str] = ATarget.SELF, **attrs):
        if isinstance(target, ATarget):
            target = target.value
        return self._common_tag('a', content_, href=href, target=target, **attrs)

    def img(self, src, **attrs):
        return self._common_tag('img', src=src, **attrs)

    def strong(self, content_: Union[str, 'HtmlBuilder'], **attrs):
        return self._common_tag('strong', content_, **attrs)

    def div(self, content_: Union[str, 'HtmlBuilder'] = None, **attrs):
        return self._common_tag('div', content_, **attrs)

    def no_tag(self, content_: Union[str, 'HtmlBuilder']):
        """无标签"""
        return self._common_tag(content_=content_)

    def custom_tag(self, tag_: str, content_: Union[str, 'HtmlBuilder'] = None, **attrs):
        """自定义标签"""
        return self._common_tag(tag_, content_, **attrs)

    def _common_tag(self, tag_: str = None, content_: Union[str, 'HtmlBuilder'] = None, **attrs):
        attrs_str = self._convert_attrs_to_str(**attrs)
        if content_ and tag_:
            self.html += f'<{tag_}{attrs_str}>{content_}</{tag_}>{self._tag_end}'
            return self
        if content_:
            self.html += f'{content_}{self._tag_end}'
            return self
        if tag_:
            self.html += f'<{tag_}{attrs_str} />{self._tag_end}'
            return self
        return self

    @staticmethod
    def _convert_attrs_to_str(**attrs):
        attrs_str = ''
        if attrs:
            for key, value in attrs.items():
                attrs_str += f' {key}="{value}"'
        return attrs_str

    def build(self):
        html = self.html
        if self._auto_add_html_tag:
            html = f'<html>\n{html}\n</html>'
        return html

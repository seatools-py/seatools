from typing import Union

from .base import BaseBuilder


class MarkdownBuilder(BaseBuilder):
    """Markdown 建造器"""

    def __init__(self):
        self._md = ''
        self._tag_end = '\n\n'

    def h1(self, content: Union[str, 'MarkdownBuilder']):
        return self._before_sign('#', content)

    def h2(self, content: Union[str, 'MarkdownBuilder']):
        return self._before_sign('##', content)

    def h3(self, content: Union[str, 'MarkdownBuilder']):
        return self._before_sign('###', content)

    def h4(self, content: Union[str, 'MarkdownBuilder']):
        return self._before_sign('####', content)

    def h5(self, content: Union[str, 'MarkdownBuilder']):
        return self._before_sign('#####', content)

    def h6(self, content: Union[str, 'MarkdownBuilder']):
        return self._before_sign('######', content)

    def em(self, content: Union[str, 'MarkdownBuilder']):
        return self._wrapper_sign('*', content)

    def i(self, content: Union[str, 'MarkdownBuilder']):
        return self._wrapper_sign('_', content)

    def strong(self, content: Union[str, 'MarkdownBuilder']):
        return self._wrapper_sign('**', content)

    def b(self, content: Union[str, 'MarkdownBuilder']):
        return self._wrapper_sign('__', content)

    def del_(self, content: Union[str, 'MarkdownBuilder']):
        return self._wrapper_sign('~~', content)

    def a(self, content: Union[str, 'MarkdownBuilder'], href: str = ''):
        return self._text(f'[{content}]({href})')

    def img(self, src, alt=''):
        return self._text(f'![{alt}]({src})')

    def hr(self):
        return self._text('---')

    def blockquote(self, content: Union[str, 'MarkdownBuilder']):
        return self._before_sign('>', content)

    def code(self, content: Union[str, 'MarkdownBuilder']):
        return self._wrapper_sign('`', content)

    def pre(self, content: Union[str, 'MarkdownBuilder'], code_type=''):
        return self._wrapper_sign('```', f'{code_type}\n{content}\n')

    def p(self, content: Union[str, 'MarkdownBuilder']):
        return self.no_tag(content)

    def no_tag(self, content: Union[str, 'MarkdownBuilder']):
        return self._text(content)

    def _text(self, text: Union[str, 'MarkdownBuilder']):
        self._md += f'{text}{self._tag_end}'
        return self

    def _before_sign(self, sign: str, content: Union[str, 'MarkdownBuilder'] = ''):
        self._md += f'{sign} {content}{self._tag_end}'
        return self

    def _wrapper_sign(self, sign: str, content: Union[str, 'MarkdownBuilder'] = ''):
        self._md += f'{sign}{content}{sign}{self._tag_end}'
        return self

    def build(self):
        return self._md[:-2] if self._md else self._md

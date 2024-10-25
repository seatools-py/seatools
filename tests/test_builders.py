from seatools.builders import HtmlBuilder, MarkdownBuilder


def test_html_builder():
    b = HtmlBuilder(auto_add_html_tag=True)
    b.h1('标题').p('啦啦啦').no_tag('hello').div(HtmlBuilder().p('11111'))
    html = b.build()
    print(html)


def test_markdown_builder():
    m = MarkdownBuilder()
    m.h1('标题').p('啦啦啦').no_tag('hello').a('测试链接', 'https://www.baidu.com')
    markdown = m.build()
    print(markdown)

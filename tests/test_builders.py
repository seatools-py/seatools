from seatools.builders import HtmlBuilder, MarkdownBuilder


def test_html_builder():
    b = HtmlBuilder(auto_add_html_tag=True)
    b.h1('标题h1').h2('标题h2').h3('标题h3').h4('标题h4').h5('标题h5').h6('标题h6').br().b('标签b').p('啦啦啦').em(
        '标签em').i('标签i').blockquote('标签blockquote').code('标签code').pre('标签pre').img(
        'https://blog.dragons96.com/logo.png').strong('标签strong').custom_tag('div', '自定义标签').no_tag('hello').div(
        HtmlBuilder().p('11111')).a('测试链接', 'https://www.baidu.com')._common_tag()
    html = b.build()
    assert html, 'html为空！'


def test_markdown_builder():
    m = MarkdownBuilder()
    m.h1('标题h1').h2('标题h2').h3('标题h3').h4('标题h4').h5('标题h5').h6('标题h6').hr().b('标签b').p('啦啦啦').em(
        '标签em').i('标签i').blockquote('标签blockquote').code('标签code').pre('标签pre').img(
        'https://blog.dragons96.com/logo.png').strong('标签strong').no_tag(
        'hello').a('测试链接', 'https://www.baidu.com').del_('删除线')
    markdown = m.build()
    assert markdown, 'markdown为空！'

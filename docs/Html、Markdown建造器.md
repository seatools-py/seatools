### `seatools.builders` 建造器
1. `seatools.builders.html.HtmlBuilder` - `class`: HTML文本建造器, 更友好易读易维护的方式创建HTML文本, 示例:

```python
from seatools.builders import HtmlBuilder

b = HtmlBuilder(auto_add_html_tag=True)
b.h1('标题').p('啦啦啦').no_tag('hello').div(HtmlBuilder().p('11111'))
html = b.build()
print(html)
"""
<html>
<h1>标题</h1>
<p>啦啦啦</p>
hello
<div><p>11111</p>
</div>

</html>
"""
```
2. `seatools.builders.html.Markdown` - `class`: Markdown文本建造器, 更友好易读易维护的方式创建Markdown文本, 示例:

```python
from seatools.builders import MarkdownBuilder

m = MarkdownBuilder()
m.h1('标题').p('示例').a('链接', href='https://www.baidu.com')
markdown = m.build()
print(markdown)
"""
# 标题

示例

[链接](https://www.baidu.com)
"""
```

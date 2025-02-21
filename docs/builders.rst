构建器工具
=========

HTML构建器
---------

用于构建 HTML 内容:

.. code-block:: python

   from seatools.builders import HtmlBuilder

   html = (
       HtmlBuilder(auto_add_html_tag=True)
           .h1('标题')
           .p('段落')
           .div(
               HtmlBuilder()
                   .span('内容')
                   .build()
           )
           .build()
   )

飞书消息构建器
------------

构建飞书机器人消息:

.. code-block:: python

   from seatools.notices import FeishuRobotPostMsg

   msg = (
       FeishuRobotPostMsg.content_builder()
           .add_text('文本内容')
           .add_a('链接文字', 'https://example.com')
           .add_at('all')
           .build()
   )

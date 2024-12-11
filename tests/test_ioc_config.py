import re


def extract_content(s):
    # 正则表达式模式，捕获 ${...} 中的内容
    pattern = r'\$\{(.*?)\}'
    # 使用 re.findall() 函数找到所有匹配的捕获组内容
    return re.findall(pattern, s)

def test_ioc_config():
    # 测试字符串
    input_string = "${a}asdh${b}sd"

    # 调用函数并打印结果
    result = extract_content(input_string)
    print(result)


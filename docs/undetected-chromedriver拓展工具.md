### `seatools.uc` (undetected-chromedriver简称uc) 拓展工具
1. `seatools.uc.Chrome` 拓展的`chrome`驱动`driver`, 使用方式如下:

```python
# 使用undetected_chromedriver写法
import random
import undetected_chromedriver as uc

driver = uc.Chrome()

# 使用unique_tools.uc写法
from seatools import uc

driver = uc.Chrome()

# 拓展方法如下

"""
1. wait_el方法, 等待并获取元素, 若等待后能够获得则获取元素则返回WebElement对象, 若等待后不可获得则抛出Timeout异常, 等同于:
WebDriverWait(driver, timeout).until(
    EC.presence_of_element_located((by, locator))
)
driver.find_element(by, locator)
"""
driver.wait_el('xxx', by=uc.By.XPATH)

"""
2. send_keys方法, 人性化的输入内容
"""
# 每秒输入1个字符
driver.send_keys(driver.wait_el('xxx', uc.By.XPATH), 'xxxx', interval=1)
# 每随机[0~1]秒输入1个字符
driver.send_keys(driver.wait_el('xxx', uc.By.XPATH), 'xxxx', interval=random.random)

"""
3. action_chains方法, 获取当前driver的操作链ActionChains对象
"""
action_chains = driver.action_chains()
action_chains.click_and_hold(...).move_by_offset(...).perform()

"""
4. get_cookies_map方法: 获取cookie {key1: value1, key2: values2}结构数据
5. get_cookies_str方法: 获取cookie key1=value1; key2=value2 字符串结构数据
"""

driver.get_cookies_map()
driver.get_cookies_str()
```

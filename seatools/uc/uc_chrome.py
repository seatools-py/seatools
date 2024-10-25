import random
import time
from typing import Union, Callable, Dict

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class Chrome(uc.Chrome):
    """自定义拓展uc.Chrome, 提供更便捷的方法"""

    def __init__(
        self,
        options=None,
        user_data_dir=None,
        driver_executable_path=None,
        browser_executable_path=None,
        port=0,
        enable_cdp_events=False,
        desired_capabilities=None,
        advanced_elements=False,
        keep_alive=True,
        log_level=0,
        headless=True,
        version_main=None,
        patcher_force_close=False,
        suppress_welcome=True,
        use_subprocess=True,
        debug=False,
        no_sandbox=True,
        user_multi_procs: bool = False,
        **kw,
    ):
        # 内置常用options
        if not options:
            options = uc.ChromeOptions()
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        super().__init__(options=options,
                         user_data_dir=user_data_dir,
                         driver_executable_path=driver_executable_path,
                         browser_executable_path=browser_executable_path,
                         port=port,
                         enable_cdp_events=enable_cdp_events,
                         desired_capabilities=desired_capabilities,
                         advanced_elements=advanced_elements,
                         keep_alive=keep_alive,
                         log_level=log_level,
                         headless=headless,
                         version_main=version_main,
                         patcher_force_close=patcher_force_close,
                         suppress_welcome=suppress_welcome,
                         use_subprocess=use_subprocess,
                         debug=debug,
                         no_sandbox=no_sandbox,
                         user_multi_procs=user_multi_procs,
                         **kw)

    def wait_el(self, locator: str, by: str = uc.By.XPATH, timeout: int = 10) -> uc.WebElement:
        """等待timeout秒并获取元素, 获取失败则产生timeout异常"""
        WebDriverWait(self, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return self.find_element(by, locator)

    @classmethod
    def send_keys(cls, el: uc.WebElement, content: str, interval: Union[float, Callable[[], float]]=random.random):
        """给元素el输入内容, 每输入一个字符等待interval的间隔, 更拟人化

        Args:
            el: 输入的元素
            content: 输入的内容
            interval: 输入每个元素等待的间隔
        """
        if not content:
            return
        for c in content:
            el.send_keys(c)
            if isinstance(interval, float):
                time.sleep(interval)
            else:
                time.sleep(interval())

    def action_chains(self):
        """获取当前行为链完成各种行为"""
        return ActionChains(self)

    def get_cookies_map(self) -> Dict[str, str]:
        """获取cookie key: value映射的字典"""
        ck_dict = {}
        for item in self.get_cookies():
            ck_dict[item['name']] = item['value']
        return ck_dict

    def get_cookies_str(self) -> str:
        """获取拼接字符串的cookie, 示例: x=1; y=2"""
        return '; '.join([f'{k}={v}' for k, v in self.get_cookies_map().items()])

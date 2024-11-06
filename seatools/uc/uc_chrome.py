import random
import time
from typing import Union, Callable, Dict, List, Literal, Optional, Any

import requests
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from urllib.parse import urlparse


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
        """等待timeout秒并获取1个元素, 获取失败则产生timeout异常"""
        WebDriverWait(self, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return self.find_element(by, locator)

    def wait_els(self, locator: str, by: str = uc.By.XPATH, timeout: int = 10) -> List[uc.WebElement]:
        """等待timeout秒并获取符合条件的元素列表, 获取失败则产生timeout异常"""
        WebDriverWait(self, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return self.find_elements(by, locator)

    @classmethod
    def send_keys(cls, el: uc.WebElement, content: str, interval: Union[float, Callable[[], float]] = random.random):
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

    def invoke(self,
               url,
               method: Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'CONNECT', 'TRACE'],
               params: Dict[str, Any] = None,
               data: Any = None,
               json: Dict[str, Any] = None,
               files: Any = None,
               auth: Any = None,
               timeout=None,
               proxies=None,
               stream=None,
               verify=None,
               cert=None,
               headers: Optional[Dict[str, str]] = None):
        """以http方式直接调用特定接口, 自动填充headers中不存在的ua, cookie等信息

        Args:
            url: 调用的链接
            method: 调用的方法
            params: url参数
            data: 传递的数据
            json: Content-Type 为 application/json 传递的数据
            files: 传递的文件数据
            auth: 认证信息
            headers: 覆盖的请求头, 不存在的键将使用当前环境覆盖, 除非特别声明值为None
            timeout: 超时时间, 默认不超时
            proxies: 代理对象
            stream: 是否以流方式处理响应
            verify: 是否TLS校验
            cert: TLS cert证书
        """
        headers = {k.lower(): v for k, v in headers.items()} if headers else {}
        if 'user-agent' not in headers:
            headers['user-agent'] = self.execute_script('return navigator.userAgent')
        if 'cookie' not in headers:
            headers['cookie'] = self.get_cookies_str()
        if 'sec-ch-ua' not in headers:
            brands = self.execute_script('return navigator.userAgentData.brands')
            if brands:
                sec_ch_uas = []
                for brand in brands:
                    if 'brand' not in brand or 'version' not in brand:
                        continue
                    sec_ch_uas.append(f'"{brand["brand"]}";v="{brand["version"]}"')
                if sec_ch_uas:
                    headers['sec-ch-ua'] = ', '.join(sec_ch_uas)
        if 'sec-ch-ua-mobile' not in headers:
            is_mobile = self.execute_script('return navigator.userAgentData.mobile')
            headers['sec-ch-ua-mobile'] = f'?{"1" if is_mobile else "0"}'
        if 'sec-ch-ua-platform' not in headers:
            platform = self.execute_script('return navigator.userAgentData.platform')
            if platform:
                headers['sec-ch-ua-platform'] = f'"{platform}"'
        if 'referer' not in headers:
            headers['referer'] = self.current_url
        if 'origin' not in headers:
            parsed_url = urlparse(url)
            headers['origin'] = f'{parsed_url.scheme}://{parsed_url.hostname}'
        return requests.request(method, url, params=params, data=data, json=json, headers=headers, files=files,
                                auth=auth, stream=stream, timeout=timeout, proxies=proxies, verify=verify, cert=cert)

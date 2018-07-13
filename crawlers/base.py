# -*- coding: utf-8 -*-
# Created by crazyX on 2018/7/8
from socket import timeout
from urllib.error import URLError, HTTPError
from crawlers.include.utils import logger, HTTP_METHOD_TIMEOUT


class OJ(object):
    # 每一个账号同一时间只考虑交一道题目，这样可以有效避免查封，且方便处理

    def __init__(self, handle, password):
        self.handle = handle
        self.password = password

    # 以下为基础属性
    @property
    def browser(self):
        raise NotImplementedError

    @property
    def url_home(self):
        raise NotImplementedError

    def url_problem(self, pid):
        raise NotImplementedError

    @property
    def url_login(self):
        raise NotImplementedError

    @property
    def url_submit(self):
        raise NotImplementedError

    @property
    def http_headers(self):
        raise NotImplementedError

    @property
    def url_status(self):
        raise NotImplementedError

    @property
    def result_fields(self):
        raise NotImplementedError

    @property
    def problem_fields(self):
        raise NotImplementedError

    @property
    def uncertain_result_status(self):
        raise NotImplementedError

    @property
    def compatible_result_fields(self):
        return ['v_run_id', 'v_submit_time', 'v_user', 'problem', 'language', 'status', 'time', 'memory']

    @property
    def compatible_problem_fields(self):
        # time limit 数字，单位为 ms
        # memory limit 数字，单位为 kb
        # input/output sample 为有序列表，长度相同
        # 三个description和hint为html源码，并替换了其中的image路径为本地路径
        # 其余为字符串
        return ['title', 'judge_os', 'time_limit', 'memory_limit',
                'description', 'input_description', 'output_description', 'hint',
                'input_sample', 'output_sample',
                ]

    # 以下为基础函数
    def get(self, url):
        try:
            return self.browser.open(url, timeout=HTTP_METHOD_TIMEOUT)
        except (HTTPError, URLError) as error:
            logger.error('Data not retrieved because %s\nURL: %s', error, url)
            return None
        except timeout:
            logger.error('socket timed out\nURL: %s', url)
            return None

    def post(self, url, data):
        raise NotImplementedError

    @staticmethod
    def http_status_code(response):
        return response.status if response else None

    @staticmethod
    def str2int(string):
        if not string:
            return 0
        try:
            return int(string[:-1])
        except:
            return int(string[:-2])

    def ping(self):
        # 5s是否能访问主页
        response = self.get(self.url_home)
        return self.http_status_code(response) == 200

    # 以下为OJ行为函数
    @staticmethod
    def batch_register(self):
        pass

    @property
    def get_languages(self):
        # 获取语言列表
        # example:
        # LANGUAGE = {
        #     'G++': '1',
        #     'G++11': '42',
        #     'G++14': '50',
        #     'GCC': '10',
        #     'JAVA': '36',
        #     'PYTHON2': '7',
        #     'PYTHON3': '31',
        # }
        raise NotImplementedError

    def login(self):
        raise NotImplementedError

    def is_login(self):
        raise NotImplementedError

    def replace_image(self, html):
        raise NotImplementedError

    def get_problem(self, pid):
        raise NotImplementedError

    def submit_code(self, pid, source, lang):
        # 返回 run id
        raise NotImplementedError

    def get_result(self):
        # 只需要获取最近一次提交的结果
        # 如果遇到了什么异常，考虑直接重新提交
        raise NotImplementedError

    def get_result_by_rid(self, rid):
        # 这个不一定每个系统都能实现
        pass

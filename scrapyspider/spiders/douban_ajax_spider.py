# -*- coding: utf-8 -*-
# @Time     : 2017/4/9 14:32
# @Author   : woodenrobot


import re
import json


from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import DoubanMovieItem


class DoubanAJAXSpider(Spider):
    name = 'douban_ajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        datas = json.loads(response.body)
        item = DoubanMovieItem()
        if datas:
            for data in datas:
                item['ranking'] = data['rank']
                item['movie_name'] = data['title']
                item['score'] = data['score']
                item['score_num'] = data['vote_count']
                yield item

            # 如果datas存在数据则对下一页进行采集
            page_num = re.search(r'start=(\d+)', response.url).group(1)
            page_num = 'start=' + str(int(page_num)+20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            yield Request(next_url, headers=self.headers)
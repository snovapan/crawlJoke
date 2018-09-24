# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql.cursors

class CrawljokePipeline(object):
    def __init__(self):
        self.filename = open("joke.json", "wb")

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.filename.write(text.encode("utf-8"))
        self.insert(item)
        return item

    def close_spider(self, spider):
        self.filename.close()

    def getCon(self):
        return pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='joke',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    def insert(self,item):
        conn = self.getCon()
        try:
            with conn.cursor() as cursor:
                val = [item['classify'],item['title'],item['content'],item['pubtime'],item['jokelink']]
                sql = 'INSERT INTO t_joke(classify,title,content,pubtime,jokelink) select %s,%s,%s,from_unixtime(unix_timestamp(%s)),%s'
                cursor.execute(sql, val)
                # 如果没有设置自动提交事务，则这里需要手动提交一次
                conn.commit()
        except:
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()
        finally:
            # 关闭数据库连接
            conn.close()
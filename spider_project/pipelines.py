# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import MySQLdb.cursors
from twisted.enterprise import adbapi

class SpiderProjectPipeline(object):
    def __init__(self,db):
        # self.dbpool = dbpool
        self.db=db
    @classmethod
    def from_settings(cls, settings):

        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法
        '''
        db=MySQLdb.connect("127.0.0.1","dqq","123456","baidu",charset="utf8")
        # dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(db)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        cursor=self.db.cursor()
        cursor.execute('insert into items values("%s","%s","%s")'% (item['itemTitle'],item['itemUrls'], item['itemSummary']))
        self.db.commit()
        # query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        # query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    # SQL语句在这里
    def _conditional_insert(self, tx, item):
        sql = "insert into items values(%s,%s,%s)"
        params = (
        item['itemTitle'], item['itemUrl'], item['itemSummary'])
        tx.execute(sql, params)
    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue

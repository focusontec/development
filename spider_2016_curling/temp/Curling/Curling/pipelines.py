#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Date  : 2017/7/31
# @Author: lsj
# @File  : pipelines.py
# @Desc  :
pip install sqlalchemy
[ˈælkəmi]

数据库入库模块--只适合接入已有数据库，不创建和修改表结构
注意：所映射表中必须有主键
注意：SQLAlchemy本身没有提供修改表结构（schema）的方式，可通过Alembic或SQLAlchemy-Migrate修改表结构
# 数据库常见异常
<class 'sqlalchemy.exc.OperationalError'>:(psycopg2.extensions.TransactionRollbackError) deadlock detected
DETAIL:  Process 596557058 waits for ShareLock on transaction 150211684; blocked by process 587834696.
<class 'sqlalchemy.exc.DatabaseError'>:(psycopg2.DatabaseError) could not receive data from server: Connection timed out
<class 'sqlalchemy.exc.OperationalError'>:(psycopg2.OperationalError) server closed the connection unexpectedly
# 其他
# from sqlalchemy.engine.url import URL # URL(**DATABASE) 连接串拼接函数
"""

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import division  # 导入未来精确除法"/"，若执行截断除法，可使用"//"操作符
from __future__ import print_function  # 导入未来输出方法print()
from __future__ import unicode_literals  # 导入未来字符串特性默认unicode，可通过b''转换为str即byte数组

import codecs
import json
import logging
import re
import time
from collections import Iterable
from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


# 数据库操作类：PG
class DataBasePG(object):
    def __init__(self, pg_conn, schema_name, *conditions):
        # 转换unicode编码 convert_unicode=True 打印详细SQL echo=True
        self.engine = create_engine(pg_conn, convert_unicode=True, pool_size=100, pool_recycle=3600, echo=False)
        self.schema_name = schema_name
        self.sess = sessionmaker(bind=self.engine)
        # self.session = self.sess()
        self.class_dict = {}
        self.logger = logging.getLogger('DataBasePG')
        self.conditions = conditions if conditions else ('vc_md5',)  # where条件

    # 字典入库，样例：{表名: [{字段1: 值1, 字段2: 值2},]}
    def process_dict(self, obj_dict, *conditions):
        if not isinstance(obj_dict, dict):
            return
        for key, values in obj_dict.items():
            if not isinstance(values, Iterable) or not values:
                continue
            self.__check_class(key)
            if conditions:
                tup_pks = conditions
            elif self.conditions:
                tup_pks = self.conditions
            else:
                model = self.class_dict[key]
                primary_keys = [c.name for c in model.__table__.primary_key]  # 默认通过主键增删改
                primary_keys.reverse()  # 倒序
                tup_pks = tuple(primary_keys)
            self.process_base(key, values, *tup_pks)
            # session.bulk_save_objects(
            #     [self.__create_model(key, value) for value in values if isinstance(value, dict)])
            # session.bulk_insert_mappings(self.class_dict[key], values)
            # session.bulk_update_mappings(self.class_dict[key], values)
            # engine.execute(self.class_dict[key].__table__.insert(), values)
            # for value in values:
            #     self.__process_kvp((key, value))
        pass

    # 字典入库，重试五次
    def process_base(self, table_name, data_rows, *conditions):
        error_max = 5
        while error_max:
            try:
                self.__process_base(table_name, data_rows, *conditions)
                break
            except Exception as e:
                # (psycopg2.DatabaseError) server closed the connection unexpectedly
                # (psycopg2.OperationalError) terminating connection due to administrator command
                # (psycopg2.InternalError) cannot execute UPDATE in a read-only transaction
                self.logger.error('{}:{}'.format(type(e), e))
                error_max -= 1
                time.sleep(1)
        pass

    # 字典入库
    def __process_base(self, table_name, data_rows, *conditions):
        start_time = time.clock()
        data_rows_insert, data_rows_update = self.batch_select(table_name, data_rows, *conditions)
        select_time, insert_time, update_time = time.clock() - start_time, 0, 0
        # if data_rows_insert:
        #     start_time_insert = time.clock()
        #     self.batch_insert(table_name, data_rows_insert)
        #     insert_time = time.clock() - start_time_insert
        # if data_rows_update:
        #     start_time_update = time.clock()
        #     self.batch_update(table_name, data_rows_update, conditions)
        #     update_time = time.clock() - start_time_update
        model = self.class_dict[table_name]
        if data_rows_insert:
            start_time_insert = time.clock()
            with self.session_scope() as session:
                session.bulk_insert_mappings(model, data_rows_insert)
            insert_time = time.clock() - start_time_insert
        if data_rows_update:
            start_time_update = time.clock()
            with self.session_scope() as session:
                session.bulk_update_mappings(model, data_rows_update)
            update_time = time.clock() - start_time_update
        all_time = time.clock() - start_time
        self.logger.info('{0}.{1} select:{2:.3f}/insert:{3:.3f}/update:{4:.3f}/all:{5:.3f}'.format(
            self.schema_name, table_name, select_time, insert_time, update_time, all_time))
        pass

    # 检测并创建匿名类
    def __check_class(self, name):
        if name not in self.class_dict.keys():
            # ArgumentError: Mapper Mapper could not assemble any primary key columns for mapped table
            table = Table(name, MetaData(schema=self.schema_name, bind=self.engine), autoload=True)
            self.class_dict[name] = self.quick_mapper(table)
        pass

    # 检查字段并创建类实例
    def __create_model(self, table_name, data_dict):
        missing_fields = []
        model = self.class_dict[table_name]()
        for k, v in data_dict.items():
            if hasattr(model, k):
                setattr(model, k, v)
            else:
                missing_fields.append(k)
        if missing_fields:
            # raise DatabaseError  # 更改表结构会引发未知异常，故不推荐
            # (psycopg2.OperationalError) FATAL:  Sorry, too many clients already
            # print('表{}缺少字段{}'.format(table_name, '、'.join(missing_fields)))
            # print('表{}字段修正：{}'.format(table_name, '、'.join(missing_fields)))
            self.logger.error('表{}缺少字段{}'.format(table_name, '、'.join(missing_fields)))
            self.logger.warning('表{}字段修正：{}'.format(table_name, '、'.join(missing_fields)))
            sql = 'ALTER TABLE '
            sql += '"{}"."{}" {};'.format(
                self.schema_name, table_name,
                ', '.join(['ADD COLUMN "{}" varchar(100)'.format(x) for x in missing_fields]))
            self.execute(sql)  # 执行增加字段SQL
            table = Table(table_name, MetaData(schema=self.schema_name, bind=self.engine), autoload=True)
            self.class_dict[table_name] = self.quick_mapper(table)  # 重新创建映射类
            model = self.__create_model(table_name, data_dict)  # 重新实例化
        return model
        pass

    # 实例列表或单实例入库，样例：[类实例1, 类实例2] 或 (类实例1, 类实例2) 或 类实例
    def process_obj(self, obj):
        if isinstance(obj, Iterable):
            for model in obj:
                self.process_obj(model)
        elif obj:
            # 单实例入库，样例：类实例
            with self.session_scope() as session:
                session.merge(obj)  # session.add(model)
        else:
            pass
        pass

    # 反映射函数
    @staticmethod
    def quick_mapper(table):
        class GenericMapper(declarative_base()):
            __table__ = table

        return GenericMapper

    # 事务会话
    @contextmanager
    def session_scope(self):
        """提供围绕一系列操作的事务范围"""
        session = self.sess()
        try:
            yield session
            session.commit()
        except IntegrityError as e:
            print(type(e), e)
        except Exception as e:
            session.rollback()
            self.logger.error('{}:{}'.format(type(e), e))
            raise e
        finally:
            session.close()

    # 执行SQL
    def execute(self, sql, **kwargs):
        raw_sql = text(sql)
        with self.session_scope() as session:
            temp = session.execute(raw_sql, kwargs)
            if re.match(pattern=r'^SELECT[\s\S]+$', string=sql, flags=re.I):
                temp = temp.fetchall()
                return temp

    # 对比数据是否有新的字段，有的话更新数据表字段
    def check_table(self, table_name, keys):
        sql = "SELECT "
        sql += "m.attname FROM pg_attribute m WHERE m.attrelid = "
        sql += "(SELECT a.oid FROM pg_class a,pg_namespace b WHERE "
        sql += "a.relname='{}' AND b.nspname='{}' AND a.relnamespace=b.oid".format(table_name, self.schema_name)
        sql += ") AND m.attstattarget<0"
        columns = [row[0] for row in self.execute(sql)]
        missing_fields = list(set(keys) - set(columns))
        if missing_fields:
            # print('表{}缺少字段{}'.format(table_name, '、'.join(missing_fields)))
            # print('表{}字段修正：{}'.format(table_name, '、'.join(missing_fields)))
            self.logger.error('表{}缺少字段{}'.format(table_name, '、'.join(missing_fields)))
            self.logger.warning('表{}字段修正：{}'.format(table_name, '、'.join(missing_fields)))
            sql = 'ALTER TABLE '
            sql += '"{}"."{}" {};'.format(
                self.schema_name, table_name,
                ', '.join(['ADD COLUMN "{}" varchar(100)'.format(x) for x in missing_fields]))
            self.execute(sql)  # 执行增加字段SQL

    # 生成拼接SQL参数，样例：[{字段1: 值1, 字段2: 值2},]，(条件1，条件2)
    @staticmethod
    def __splice_sql(data_rows, *conditions):
        col_keys, arg_keys, arg_dict = list(), list(), dict()
        for i, data_row in enumerate(data_rows):
            for k, value in data_row.items():
                if conditions and k not in conditions:
                    continue
                if k not in col_keys:
                    col_keys.append(k)
                key = '{}_{}'.format(k, i)
                arg_dict[key] = value
            arg_keys.append(list())
        # 字段补遗
        for i, arg_key in enumerate(arg_keys):
            for k in col_keys:
                key = '{}_{}'.format(k, i)
                arg_key.append(key)
                if key not in arg_dict.keys():
                    arg_dict[key] = None
        return col_keys, arg_keys, arg_dict
        pass

    # 批量插入，样例：表名，[{字段1: 值1, 字段2: 值2},]
    def batch_insert(self, table_name, data_rows):
        # insert into tbl1 (id,info,crt_time) values (1,'test',now()), (2,'test2',now()), (3,'test3',now());
        if not data_rows:
            return
        for data_row in data_rows:
            self.check_table(table_name, data_row.keys())
        table_name = '"{}"."{}"'.format(self.schema_name, table_name)
        col_keys, arg_keys, arg_dict = self.__splice_sql(data_rows)
        sql = 'INSERT INTO '
        sql += '{} ("{}") VALUES '.format(table_name, '", "'.join(col_keys))
        sql += ','.join(['(:{})'.format(', :'.join([k for k in arg_key])) for arg_key in arg_keys])
        sql += ';'
        self.execute(sql, **arg_dict)
        pass

    # 批量更新
    def batch_update(self, table_name, data_rows, *conditions):
        # update test set info=tmp.info from (values (1,'new1'),(2,'new2'),(6,'new6')) as tmp (id,info)
        # where test.id=tmp.id;
        table_name = '"{}"."{}"'.format(self.schema_name, table_name)
        col_keys, arg_keys, arg_dict = self.__splice_sql(data_rows)
        sql = 'UPDATE {} SET '.format(table_name)
        sql += ', '.join(['"{}"=tmp."{}"'.format(col_key, col_key) for col_key in col_keys])
        sql += ' FROM (VALUES '
        sql += ','.join(['(:{})'.format(', :'.join([k for k in arg_key])) for arg_key in arg_keys])
        sql += ') AS tmp ("{}")'.format('", "'.join(col_keys))
        sql += ' WHERE {}'.format(' AND '.join(['{}."{}"=tmp."{}"'.format(table_name, c, c) for c in conditions]))
        sql += ';'
        # print(sql)
        self.execute(sql, **arg_dict)
        pass

    # 批量删除
    def batch_delete(self, table_name, data_rows, *conditions):
        # delete from test using (values (3),(4),(5)) as tmp(id) where test.id=tmp.id;
        table_name = '"{}"."{}"'.format(self.schema_name, table_name)
        col_keys, arg_keys, arg_dict = self.__splice_sql(data_rows, *conditions)
        sql = 'DELETE FROM '
        sql += '{} USING (VALUES '.format(table_name)
        sql += ','.join(['(:{})'.format(', :'.join([k for k in arg_key])) for arg_key in arg_keys])
        sql += ') AS tmp ("{}")'.format('", "'.join(col_keys))
        sql += ' WHERE {}'.format(' AND '.join(['{}."{}"=tmp."{}"'.format(table_name, c, c) for c in conditions]))
        sql += ';'
        print(sql)
        self.execute(sql, **arg_dict)
        pass

    # 批量查询，用于批量更新/插入前的准备工作
    def batch_select(self, table_name, data_rows, *conditions):
        table_name = '"{}"."{}"'.format(self.schema_name, table_name)
        col_keys, arg_keys, arg_dict = self.__splice_sql(data_rows, *conditions)
        sql = 'SELECT '
        sql += ', '.join(['t1."{}"'.format(c) for c in conditions])
        sql += ' FROM {} AS t1, (VALUES '.format(table_name)
        sql += ','.join(['(:{})'.format(', :'.join([k for k in arg_key])) for arg_key in arg_keys])
        sql += ') AS tmp ("{}")'.format('", "'.join(col_keys))
        sql += ' WHERE {}'.format(' AND '.join(['t1."{}"=tmp."{}"'.format(c, c) for c in conditions]))
        sql += ';'
        res = self.execute(sql, **arg_dict)
        data_rows_insert, data_rows_update = list(), list()
        pk_data_set = set()
        for data_row in data_rows:
            pk_data = tuple(data_row.get(c) for c in conditions)
            if pk_data in pk_data_set:
                self.logger.warning('The data of {} is duplicated:{}'.format(table_name, pk_data))
                continue
            pk_data_set.add(pk_data)
            if pk_data in res:
                data_rows_update.append(data_row)
            else:
                data_rows_insert.append(data_row)
        # print(res, data_rows_insert, data_rows_update)
        return data_rows_insert, data_rows_update
        pass


# 文件存储Json
class JsonFilePipeline(object):
    # 保存到文件中对应的class
    # 1、在settings.py文件中配置
    # 2、在自己实现的爬虫类中yield item, 会自动执行
    count_num = 1
    def __init__(self):
        # 保存为json文件
        self.file = codecs.open('temp.json', 'w', encoding='utf-8')


    def process_item(self, item, spider):
        # 转为json的
        # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # line = json.dumps(dict(item)) + "\n"
        # 写入文件中
        self.file.write(str(JsonFilePipeline.count_num) + '\n')
        JsonFilePipeline.count_num+=1
        return item

    # 爬虫结束时关闭文件
    def spider_closed(self, spider):
        self.file.close()



# 关系型数据库存储：PG
class PGStorePipeline(DataBasePG):
    def __init__(self, pg_conn, schema_name):
        super(PGStorePipeline, self).__init__(pg_conn, schema_name)
        pass

    @classmethod
    def from_crawler(cls, spider):
        return cls(pg_conn=spider.settings.get('PG_CONN'),
                   schema_name=spider.settings.get('PG_SCHEMA'))

    # pipeline默认调用
    def process_item(self, item, spider):
        self.process_dict({item['table_name']: item['data_rows']})
        pass

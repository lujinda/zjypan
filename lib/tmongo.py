#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-25 12:56:22
# Filename      : tmongo.py
# Description   : 
from pymongo.database import Database as db_type, Collection as coll_type
from functools import partial
from threading import RLock

ROLLBACK_ACTION = ('insert', 'update', 'remove')

class TransactionNotBegin(Exception):
    pass

class TransactionNotEnd(Exception):
    pass

class ActionNotSuport(Exception):
    def __init__(self, action):
        super(ActionNotSuport, self).__init__('%s not suport' % action)

class Transaction():
    queue = [] # 这里面会存着一些回滚函数, 当出现异常时，会执行，参数早已通partial绑定好了
    def append(self, rollback_func):
        self.queue.append(rollback_func)

    def rollback(self):
        for _func, args in self.queue[::-1]:
            _func(args)
        self.queue = []

class TCollection():
    def __init__(self, collection, tran):
        assert tran != None
        self._collection = collection
        self._tran = tran

    def __getattr__(self, name):
        if name not in dir(self._collection): # 比如 db.account.xxx, account是TCollection， 如果xxx不是self._collection的属性，则表示指定的是子文档，就递归返回
            return TCollection(getattr(self._collection, name), self._tran)
        action = name
        if action not in ROLLBACK_ACTION:
            return getattr(self._collection, action) # 如果调用得方法不属于支持回滚的操作方法中，则返回原始的属性或方法
        exec_func = getattr(self, 'execute_' + action) # 反正我封装过的方法
        return exec_func

    def __rollback(self, action, args):
        assert action in ROLLBACK_ACTION
        if not isinstance(args, (list, tuple)):
            args = [args]


        if not args:
            return 

        _rollback = getattr(self, '_rollback_' + action)
        _rollback(args)

    def _rollback_insert(self, args):
        self._collection.remove({'_id': {"$in": args}})

    def _rollback_remove(self, args):
        self._collection.insert(args)

    def _rollback_update(self, args):
        if (not args) or args[0] == None:
            return
        for arg in args:
            _id = arg['_id']
            self._collection.update({'_id': _id}, arg)

    def execute_insert(self, *args, **kwargs):
        """封装了insert操作，就是把insert后的_id记起来，回滚操作就是删除这些id"""
        result = self._collection.insert(*args, **kwargs)

        self._tran.append((partial(self.__rollback, 'insert'), result))

        return result

    def execute_remove(self, spec_or_id=None, safe=None, multi=True, **kwargs):
        """封装了remove操作，就是把remove删除的东西，先find出来，回滚时，insert进去就行了"""
        if not isinstance(spec_or_id, dict):
            condition = None if spec_or_id == None else{'_id': spec_or_id}
        else:
            condition = spec_or_id

        result = self.__get_origin_result(condition, multi)

        self._tran.append((partial(self.__rollback, 'remove'),
                result))

        return self._collection.remove(spec_or_id, safe, multi, **kwargs)

    def execute_update(self, spec, document, upsert=False, manipulate=False, safe=None, multi=False, check_keys=True, **kwargs):
        """封装了update操作，就是比较麻烦的一个操作，需要判断upsert，如果是True，则会知道是否更新的是已存在的文件，如果是新插入的，回滚处理跟insert一样"""
        result = self.__get_origin_result(spec, multi)
        self._tran.append((partial(self.__rollback, 'update'),
                result))

        safe = upsert or safe
        result = self._collection.update(spec, document, upsert , 
                manipulate, safe, multi, check_keys, **kwargs)
        if result and result.get('updatedExisting', True) == False:
            self._tran.append((partial(self.__rollback, 'insert'),
                result['upserted']))

        return result


    def __get_origin_result(self, condition, multi):
        if multi == False:
            result = self._collection.find_one(condition)
        else:
            result = list(self._collection.find(condition))

        return result

class TMongo(object):
    def __init__(self, db):
        assert isinstance(db, db_type), 'db must pymongo.database.Database'
        self._db = db
        self.tran = None
        self.lock = RLock()

    def __enter__(self):
        self.begin()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type and exc_value and exc_traceback:
            self.rollback()
        self.end()

    def begin(self):
        if self.tran:
            raise TransactionNotEnd
        self.lock.acquire()

        self.tran = Transaction()

    def __getattr__(self, name):
        _obj = getattr(self._db, name, None)
        if name in dir(self._db):
            return _obj

        if self.tran != None:
            return TCollection(_obj, self.tran)
        else:
            return _obj

    def __getitem__(self, name):
        return self.__getattr__(name)

    def rollback(self):
        if not self.tran:
            raise TransactionNotBegin
        self.tran.rollback()
        self.end()

    def end(self):
        if not self.tran:
            raise TransactionNotBegin
        self.lock.release()
        self.tran = None


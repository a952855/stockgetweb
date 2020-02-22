#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis


class RedisSotcks():
    def __init__(self, host, port, password):
        self.rds = redis.Redis(
            host=host,
            port=port,
            password=password
        )

    def setStockInfos(self, _id, val):
        self.rds.hset(f'stocks:{_id}', 'infos', val)

    def getStockInfos(self, _id):
        infos = self.rds.hget(f'stocks:{_id}', 'infos').decode('utf-8')
        return infos

    def setAll(self, prefix, col, data):
        pipe = self.rds.pipeline()
        for k, v in data.items():
            pipe.hset(f'{prefix}:{k}', col, v)
        pipe.execute()

    def getAllStockInfos(self):
        cursor, keys = self.rds.scan(match='stocks:*')
        data = self.rds.mget(keys)
        return data

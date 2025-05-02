# -*- coding: utf8 -*-
import json

class SegReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def getShapes(self):
        # 读取json数据
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            shapes = data['shapes']
        return shapes
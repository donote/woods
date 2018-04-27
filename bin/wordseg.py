#!/usr/bin/env python
# encoding=utf-8
"""
Time: 2018.03.21
Author: Harry.Liu
Description: 使用pyhanlp进行分词与词性识别 python3环境下
Usage: crf特征生成 将segword映射到已标注的时间实体的BIO上
"""

import sys
import os
import json
import copy

sys.path.append('lib')
from pyhanlp import PyHanLP


def ws_parsing(hanlp, text):
    """
    对text进行分词和词性标注
    返回: [[word, pos, idx]]
    """
    retvec = []
    # 分词
    result = hanlp.segment(text)
    arr = []
    for e in result.toArray():
        arr.append(e.toString())
    #print('\t'.join(arr))

    idx = 0
    for e in arr:
        i = e.rfind('/')
        wd, pos = e[:i], e[i+1:]
        #print(wd, pos, idx)
        retvec.append([wd, pos, idx])
        idx += len(wd)
    return retvec


def match_timeent_bio(wspos, timent):
    """
    不做异常判断! 
    wspos信息对应到time实体BIO上, 每条bio对应到一条样本
    wspos: [(ws, pos, idx)...]
    timent: [[time, ei, si]...]
    return: [[ws, pos, BIO]]
    """
    retvec = []
    for e in wspos:
        ne  = copy.copy(e)
        idx = e[2]
        bio = 'O'
        for te in timent:
            time, si, ei = te[0], te[1], te[2]
            if idx == si:
                bio = 'NT-S'
            elif idx > si and idx < ei:
                bio = 'NT-I'
        ne[2] = bio
        retvec.append(ne)
    return retvec


def ws_parse_data():
    """
    获取待评估数据 格式: sentence \t json.dumps([[time, si, ei]...])
    python3 读入就是unicode编码(str)
    """
    # 实例化分词系统
    hanlp = PyHanLP()
    for line in sys.stdin:
        term = line.strip().split('\t')
        text, timent = term[0], json.loads(term[1])
        #print(text, timent)
        wsret = ws_parsing(hanlp, text)
        # 将ws/pos与time BIO对应上
        ftvec = match_timeent_bio(wsret, timent)
        #print(wsret)
        #print(timent)
        #print(ftvec)
        for e in ftvec:
            if len(e) == 3:
                print('\t'.join(e))
        print('')



def test_main():
    ws_parse_data()


def word_seg():
    """
    input: label \t text
    output: label \t word1 word2 ...
    """
    hanlp = PyHanLP()
    for line in sys.stdin:
        wdvec = []
        term = line.decode('utf8').strip().split('\t')
        if len(term) < 2:
            continue
        label, text = term[0], term[1]
        wsret = ws_parsing(hanlp, text)
        for w in wsret:
            if len(w) == 3:
                wdvec.append(w[0])
        s = u'%s\t%s' %(label, ' '.join(wdvec))
        print s.encode('utf8')


if __name__ == "__main__":
    #test_main()
    word_seg()


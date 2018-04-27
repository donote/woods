#! /usr/bin/env python
# coding:utf-8 
"""
Author: Harry.liu
Date: 2018/04/13
Desc: 使用HanLP进行中文分词 词性标注
词性标注选项可通过配置文件hanlp.properties中的ShowTermNature进行控制
From: https://github.com/hankcs/HanLP/releases 
Python2环境OK
注意: 程序内使用均为unicode, java的输入输出也是unicode
程序内外编码需要做转换
"""

import sys
from jpype import *

class PyHanLP(object):
    def __init__(self):
        """
        初始化阶段 启动JVM
        """
        # HanLP jar路径及相关参数 
        # 注意jar路径!
        HANLP_PATH = "~/thirdparty/HanLP/hanlp-1.5.4-release/hanlp-1.5.4.jar:/thirdparty/HanLP/hanlp-1.5.4-release/"
        jparams = "-Djava.class.path=" + HANLP_PATH
        jvmpath = getDefaultJVMPath()
        # 启动JVM
        startJVM(jvmpath, jparams, "-Xms1g", "-Xmx1g")

        # 实例化必要的类
        # detail see: com/hankcs/hanlp/HanLP.java
        self._hanlp = JClass('com.hankcs.hanlp.HanLP')
        self._hanlp_tokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')

    def __del__(self):
        """
        类析构时关闭JVM
        """
        shutdownJVM()

    def close(self):
        """
        显示关闭JVM
        """
        self.__del__()
    
    def segment(self, text):
        """
        Desc:中文分词 utf8或unicode编码输入
        Return: JArray(JString)
        """
        return self._hanlp.segment(text)

    def convert2PinyinList(self, text):
        """
        Desc: 中文转拼音 拼音后面带音标
        """
        return self._hanlp.convertToPinyinList(text)

    def segment_tokenizer(self, text):
        """
        Desc:中文分词 带NER POS
        Return: JArray(JString)
        """
        return self._hanlp_tokenizer.segment(text)

    def segment_tokenizer_sentence(self, text):
        """
        Desc:中文分词 带NER POS, 按,.，。等划分句子 返回各对句子分词结果
        Return: JArray(JArray(JString))
        """
        return self._hanlp_tokenizer.seg2sentence(text)

    def extractKeyword(self, document, item_cnt):
        """
        Desc: 关键词抽取
        """
        return self._hanlp.extractKeyword(document, item_cnt)

    def extractSummary(self, document, sent_cnt):
        """
        Desc: 摘要抽取
        """
        return self._hanlp.extractSummary(document, sent_cnt)

    def parseDependency(self, text):
        """
        Desc: 依存句法分析
        """
        return self._hanlp.parseDependency(text)

    def wordseg_pos(self, text):
        """
        Desc: 返回text分词及pos结果 [[word, pos, idx] ... ]
        """
        arr, retvec = [], []
        result = self.segment(text)
        for e in result.toArray():
            arr.append(e.toString())
        #print('\t'.join(arr))

        idx = 0
        for e in arr:
            i = e.rfind('/')
            wd, pos = e[:i], e[i+1:]
            retvec.append([wd, pos, idx])
            idx += len(wd)
        return retvec


def print2(result):
    """
    把java返回的结果转换为python2能够输出的字符串
    """
    arr = []
    for e in result.toArray():
        arr.append(e.toString())
    print('\t'.join(arr))


def print_s(result):
    """
    把java返回的结果转换为python2能够输出的字符串
    """
    arr = []
    for e in result.toArray():
        arr.append(e)
    print('\t'.join(arr))


def unit_test():
    """
    封装后单元测试
    """
    hanlp = PyHanLP()
    
    # 分词
    text = u'你好，欢迎在Python中调用HanLP的API'
    result = hanlp.segment(text)
    print2(result)

    testCases = [
        u"商品和服务",
        u"结婚的和尚未结婚的确实在干扰分词啊",
        u"买水果然后来世博园最后去世博会",
        u"中国的首都是北京",
        u"欢迎新老师生前来就餐",
        u"工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作",
        u"随着页游兴起到现在的页游繁盛，依赖于存档进行逻辑判断的设计减少了，但这块也不能完全忽略掉。"
        ]
    for sentence in testCases: print2(hanlp.segment(sentence))

    # 命名实体识别与词性标注
    text = u'中国科学院计算技术研究所的宗成庆教授正在教授自然语言处理课程'
    text = u'右肺上叶尖段见一小结节同前，大小约0.8*0.9cm，周边分叶，可见毛刺。右肺下叶背段见一半实性结节，形态大致同前，现最大层面测量约2.4*2.3cm，内见支气管气相，可见毛刺及胸膜牵拉。余肺透光度增高，右肺上叶后段见少量斑片状模糊影同前；两下肺后基底段新增斑片磨玻璃模糊影。新增左斜裂（-16）一结节，大小约3.5mm，边缘清。纵隔多个小淋巴结同前，较大短径约0.6cm。两侧肺门淋巴结未见明显肿大；两侧胸腔未见积液。双侧肱骨头、胸11椎体见结节状高密影。扫描所见肝脏S4见数个囊状低密度影，大者约1.4cm'
    text = u'于2014-4复查胸部CT示肺部病灶进展，在当地医院行2周期化疗，具体不详'
    result = hanlp.segment_tokenizer(text)
    print2(result)

    text = u'这个半月时间4个半月前的事情'
    result = hanlp.segment_tokenizer_sentence(text)
    print2(result)

    # 关键词提取
    document = u"水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
               u"根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，" \
               u"有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，" \
               u"严格地进行水资源论证和取水许可的批准。"
    result = hanlp.extractKeyword(document, 2)
    print_s(result)

    # 自动摘要
    result = hanlp.extractSummary(document, 3)
    print_s(result)

    # 依存句法分析 data/model/
    text = u"徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"
    text = u'手术描述：1.麻醉满意后，左侧卧位，常规消毒铺巾。取右侧腋中线第八肋间1.5cm切口，单肺通气后进入胸腔，置入胸腔镜探查'
    text = u'右上肺尖段结节、右下肺背段半实性结节，大致同前，肺癌与感染相鉴别，建议活检'
    text = u'于2014-4复查胸部CT示肺部病灶进展，在当地医院行2周期化疗，具体不详'
    #result = hanlp.parseDependency(text)


def segword():
    """
    作为工具使用 从标准输入得到数据 utf8
    token之间用\t分割
    Using: cat data/data_wordseg.txt | python lib/pyhanlp.py
    """
    hanlp = PyHanLP()
    for line in sys.stdin:
        line = line.decode('utf8').strip()
        # 分词
        result = hanlp.segment(line)
        arr = []
        for e in result.toArray():
            arr.append(e.toString())
        print('\t'.join(arr).encode('utf8'))


if __name__ == "__main__":
    unit_test()
    #segword()

#!usr/bin/python
#-*-coding:utf-8-*-
import nltk
import math
from nltk.corpus import reuters

def getKeyWords(inFileName,outFileName,keywordsNum):
    '''
    使用TF-IDE算法提取关键字
    :param inFileName: 待处理的输入文章
    :param outFileName: 关键字提取结果存放文件
    :param keywordsNum: 要提取的关键词数
    :return:
    '''

    fin = open(inFileName,'r')                      #打开待处理文件
    fout = open(outFileName,'w')                    #fout为结果输出记录

    fredist = nltk.FreqDist(fin.read().split(' '))  #使用nltk.FreqDist统计文本词频
    maxFreq = max(fredist.values())                 #获取出现的最大的频次(用来求后面相对频次)
    print 'maxFreq : %s' % maxFreq

    TFdist = {}                                     #calculate TF
    for key,value in fredist.items():
        TFdist[key] = float(value) / maxFreq        # TF = (某个单词在文章中出现的次数)/(该文出现次数最多的词的出现次数)

    IDFdist = {}                                    #calculate IDF
    for key,value in fredist.items():
        count = 1
        for fileid in reuters.fileids()[:100]:
            if reuters.words(fileid).count(key) > 0: #说明该文章包含该单词
                count += 1
        IDFdist[key] = math.log( 100.0/count )       # IDF = log(语料库文档总数/包含该词的文档数 +1)

    TFIDEdist = {}                                   #calculate TF-IDE
    for key in fredist.keys():
        TFIDEdist[key] = TFdist[key] * IDFdist[key]

    #输出前keywordsNum个关键字
    TFIDElist = sorted(TFIDEdist.items(),key=lambda x: x[1],reverse=True)
    outstr = ''
    for i in range(keywordsNum):
        outstr += TFIDElist[i][0] + ' : ' + str(TFIDElist[i][1]) +'\n'
    fout.write(outstr.encode('utf-8'))

    fin.close()
    fout.close()
    return TFIDElist[:keywordsNum]

def getSimilarity(keywlist1, keywlist2):

    keydist1 = {}                                      #获取两个文章关键字的集合
    keydist2 = {}
    keydist1.update(keywlist1)
    keydist2.update(keywlist2)

    for key in keydist2.keys():                       #用第二个文章关键词dist更新第一个
        keydist1.setdefault(key,0)
    for key in keydist1.keys():                       #用第一个文章关键词dist更新第二个
        keydist2.setdefault(key,0)

    crossProduct  =  0                                #求余弦相似度
    mode1 = 0
    mode2 = 0
    for key in keydist1.keys():
        crossProduct += keydist1[key] * keydist2[key]
        mode1 += keydist1[key] * keydist1[key]
        mode2 += keydist2[key] * keydist2[key]
    cosResult = float(crossProduct) / (math.sqrt(mode1) * math.sqrt(mode2))
    return  cosResult

if(__name__ == '__main__'):

    fileName1 = './mycorpusUTF8/EnglishText1.txt'
    resultFile1 = './mycorpusUTF8/EnglistResult1.txt'
    fileName2 = './mycorpusUTF8/EnglishText3.txt'
    resultFile2 = './mycorpusUTF8/EnglishResult3.txt'
    list1 = getKeyWords(fileName1,resultFile2,10)
    list2 = getKeyWords(fileName2,resultFile2,10)
    # strlist1 = [('I',1),('do',1),('like',1)]
    # strlist2 = [('I',1),('like',1),('do',1)]
    result = getSimilarity(list1,list2)
    print result
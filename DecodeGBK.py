
import os
import codecs

dirs = os.listdir('./mycorpus/')
for d in dirs:
    print d
    subdir = './mycorpus/' +d
    text = open(subdir,'r').read().decode('gbk')
    print text
    # subdir = os.listdir('./mycorpus/' +d)
    # text = open(subdir,'r').read().decode('gbk')
    # print text.encode('gbk')
    # text.close()

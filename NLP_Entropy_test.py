import os
import re
import math
import jieba
import matplotlib.pyplot as plt

def get_dic(dic, words): # 一元模型
    for i in range(len(words)-1):
        dic[words[i]] = dic.get(words[i], 0) + 1

def get_dou_dic(dic, words): # 二元模型
    for i in range(len(words)-1):
        dic[(words[i], words[i+1])] = dic.get((words[i], words[i+1]), 0) + 1
        
def get_tri_dic(dic, words): # 三元模型
    for i in range(len(words)-2):
        dic[((words[i], words[i+1]), words[i+2])] = dic.get(((words[i], words[i+1]), words[i+2]), 0) + 1

'''一元模型信息熵计算'''
def cal_uni(list, sumWords, flag):
    words_dic = {}
    get_dic(words_dic, list)
    entropy = []
    for uni_word in words_dic.items():
        entropy.append(-(uni_word[1] / sumWords) * math.log(uni_word[1] / sumWords, 2))
    if flag == 0:
        print("以字为单位的一元模型的中文信息熵为:", round(sum(entropy), 6), "比特")
    else:
        print("以词为单位的一元模型的中文信息熵为:", round(sum(entropy), 6), "比特")

'''二元模型信息熵计算'''
def cal_dou(list):
    words_dic = {}
    douwords_dic = {}
    get_dic(words_dic, list)
    get_dou_dic(douwords_dic, list)
    douwords_len = sum([dic[1] for dic in douwords_dic.items()])
    entropy = []
    for bi_word in douwords_dic.items():
        jp_xy = bi_word[1] / douwords_len  # 计算联合概率p(x,y)
        cp_xy = bi_word[1] / words_dic[bi_word[0][0]]  # 计算条件概率p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算二元模型的信息熵
    print("以词为单位的二元模型的中文信息熵为:", round(sum(entropy), 6), "比特")

'''三元模型信息熵计算'''
def cal_tri(list):
    words_dic = {}
    triwords_dic = {}
    get_dou_dic(words_dic, list)
    get_tri_dic(triwords_dic, list)
    triwords_len = sum([dic[1] for dic in triwords_dic.items()])
    entropy = []
    for tri_word in triwords_dic.items():
        jp_xy = tri_word[1] / triwords_len  # 计算联合概率p(x,y)
        cp_xy = tri_word[1] / words_dic[tri_word[0][0]]  # 计算条件概率p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算三元模型的信息熵
    print("以词为单位的三元模型的中文信息熵为:", round(sum(entropy), 6), "比特")

'''获得停词表'''
def stopwords(addr):
    stop_sum = 0  # 总的中文字符数
    stop_num_dic = {}  # 存储中文字符和出现次数的字典
    with open(addr, "r", encoding='utf-8', errors='ignore') as file1:
        fop = file1.readlines()
        for lword in fop:
            wd = lword.strip() # 清除掉空格之类的乱七八糟的东西
            stop_sum += 1  # 总的中文字符数+1
            stop_num_dic[wd] = stop_num_dic.get(wd, 0) + 1
        del fop, lword
    dic_lst = list(stop_num_dic.keys())
    return '|'.join(dic_lst)


''' Zipf's Law 验证开关, 默认为 1 开启状态, 计算信息熵时可将其设置为0关闭, 提高程序运行速度'''
test_flag = 0 

stopstr = stopwords("cn_stopwords.txt")
filepath = 'book/' # 需要遍历的文件夹
num = 0
listword = '' # 最终将所有中文放到一个str里
sumChar = 0 # 记录总字符数，包括停词以及非中文字符
sumWords = 0 # 记录除了停词表中意外的字符出现个数
filename = ['碧血剑.txt', '鹿鼎记.txt', '神雕侠侣.txt', '白马啸西风.txt', '飞狐外传.txt', '鸳鸯刀.txt', 
            '越女剑.txt', '雪山飞狐.txt', '连城诀.txt', '三十三剑客图.txt', '射雕英雄传.txt', 
            '书剑恩仇录.txt', '天龙八部.txt', '倚天屠龙记.txt', '笑傲江湖.txt', '侠客行.txt']
spe = filename[2] # 需要单独遍历的文件
legend = [] # 图例
print(spe[:-4], ":")

'''验证 Zipf's Law'''
if test_flag == 1:
    for root, path, fil in os.walk(filepath):
        counts = {}
        for txt_file in fil:
            legend.append(txt_file[:-4])
            '''遍历某一特定文件添加这个条件判断'''
            # if txt_file != spe: 
            #     continue
            with open(root+txt_file, "r", encoding='ANSI', errors='ignore') as file:
                words = jieba.lcut(re.sub(r'[\s!“”’‘"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+', "", file.read()))
            for word in words:
                if word.strip() != "" and word.strip() != " ":
                    counts[word] = counts.get(word, 0) + 1
            '''将词频排序并获取频率列表'''
            items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            frequencies = [count for _, count in items]
            plt.plot(frequencies)  # 绘制曲线
    '''绘制Zipf定律图表'''
    plt.title('Zipf-Law')  
    plt.xlabel('rank')  
    plt.ylabel('frequency')  
    plt.xticks()
    plt.yticks()
    plt.xscale('log')  # 设置x轴为对数刻度
    plt.yscale('log')  # 设置y轴为对数刻度
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 解决中文乱码
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend(legend)
    plt.show()

'''计算信息熵, 包括一元字信息熵, 以及一元、二元、三元词信息熵'''

'''一元字信息熵'''
for root, path, fil in os.walk(filepath):
    for txt_file in fil:
        '''遍历所有文件删除这个条件判断'''
        if txt_file != spe: 
            continue
        with open(root+txt_file, "r", encoding='ANSI', errors='ignore') as file:
            fp = file.readlines()
            for lword in fp:
                lword = lword.replace('\n', '')
                lword = lword.replace(' ', '')
                lword = lword.replace('　　', '')
                lword = lword.replace('\t', '')
                sumChar += len(lword)
                wordstr = re.sub(stopstr, '', lword)
                sumWords += len(wordstr)
                listword = listword + wordstr
            del file, fp
cal_uni(listword, sumWords, 0)

'''一元、二元、三元词信息熵'''
listWords = []
sumWords = 0 # 记录除了停词表中意外的字符出现个数
for root, path, fil in os.walk(filepath):
    for txt_file in fil:
        '''遍历所有文件删除这个条件判断'''
        if txt_file != spe: 
            continue
        with open(root+txt_file, "r", encoding='ANSI', errors='ignore') as file:
            fp = file.readlines()
            for lword in fp:
                lword = lword.replace('\n', '')
                lword = lword.replace(' ', '')
                lword = lword.replace('　　', '')
                lword = lword.replace('\t', '')
                wordstr = re.sub(stopstr, '', lword)
                for x in jieba.cut(wordstr):
                    listWords.append(x)
                    sumWords += 1
cal_uni(listWords, sumWords, 1)
cal_dou(listWords)
cal_tri(listWords)
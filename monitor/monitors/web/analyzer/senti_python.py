# -*- coding: utf-8 -*-
import jieba
import re
import numpy as np
from .. import settings


def not_empty(s):
    return s and s.strip()


def is_stop_word(word):
    stopwords = open_dict(Dict='stopwords')
    word = word.encode("utf-8")
    if word in stopwords:
        return True
    if word.isdigit():
        return True
    if not word.strip():
        return True
    return False

# 打开词典文件，返回列表
def open_dict(Dict = 'hahah', path=settings.SENTI_DIR_PATH):
    path = path + '%s.txt' % Dict
    dictionary = open(path, 'r')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        dict.append(word)
    return dict


def judgeodd(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'


#注意，这里你要修改path路径。
posdict = open_dict(Dict='positive')
deny_word = open_dict(Dict=u'否定词')
negdict = open_dict(Dict='negative')

degree_word = open_dict(Dict=u'程度级别词语')
mostdict = degree_word[degree_word.index('extreme')+1 : degree_word.index('very')]#权重4，即在情感词前乘以4
verydict = degree_word[degree_word.index('very')+1 : degree_word.index('more')]#权重3
moredict = degree_word[degree_word.index('more')+1 : degree_word.index('ish')]#权重2
ishdict = degree_word[degree_word.index('ish')+1 : degree_word.index('last')]#权重0.5



def sentiment_score_list(seg_sentence):
    # seg_sentence = dataset.split('。')
    words = []
    count1 = []
    count2 = []
    senti_score_words_result = {"count2": count2, "words": words}
    for index, sen in enumerate(seg_sentence): #循环遍历每一个评论
        # print index
        if not sen:
            continue
        segtmp = jieba.lcut(sen, cut_all=False)  #把句子进行分词，以列表的形式返回
        # 把所有的分词加到总list中
        words.extend(segtmp)
        i = 0 #记录扫描到的词的位置
        a = 0 #记录情感词的位置
        poscount = 0 #积极词的第一次分值
        poscount2 = 0 #积极词反转后的分值
        poscount3 = 0 #积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            word = word.encode("utf-8")
            if word in posdict:  # 判断词语是否是情感词
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    w = w.encode("utf-8")
                    if w in mostdict:
                        poscount *= 4.0
                    elif w in verydict:
                        poscount *= 3.0
                    elif w in moredict:
                        poscount *= 2.0
                    elif w in ishdict:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化

            elif word in negdict:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    w = w.encode("utf-8")
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in degree_word:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '！' or word == '!':  ##判断句子是否有感叹号
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1 # 扫描词位置前移


            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []

    return senti_score_words_result

def sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        AvgPos = np.mean(score_array[:, 0])
        AvgPos = float('%.1f'%AvgPos)
        AvgNeg = np.mean(score_array[:, 1])
        AvgNeg = float('%.1f'%AvgNeg)
        StdPos = np.std(score_array[:, 0])
        StdPos = float('%.1f'%StdPos)
        StdNeg = np.std(score_array[:, 1])
        StdNeg = float('%.1f'%StdNeg)
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
    return score


def strs_filter(text_str):
    re_html = re.compile('<[^>]+>'.decode('utf8'))#从'<'开始匹配，不是'>'的字符都跳过，直到'>'
    # re_punc = re.compile('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，；。？、~@#￥%……&*（）]+'.decode('utf8'))#去除标点符号
    # re_digits_letter = re.compile('\w+'.decode('utf8'))#去除数字及字母
    text_str = re_html.sub('', text_str)
    # text_str = re_punc.sub("", text_str)
    # text_str = re_digits_letter.sub("", text_str)
    return text_str


# 1代表积极-1代表负面0代表中性
def senti_content(text):
    text = text.decode('utf-8')
    # 过滤html标签
    text = strs_filter(text)
    tests = re.split('。|！|？|\n'.decode('utf8'), text)
    tests_f = list(filter(not_empty, tests))
    # 获取情感分析分值list和分词
    senti_score_words_result = sentiment_score_list(tests_f)
    socre_list = sentiment_score(senti_score_words_result['count2'])
    word_list = senti_score_words_result['words']
    ss = {"pos": 0, "neg": 0, "midd": 0}
    analyzer_result = {"senti_result": 0, "word_list": word_list}
    for index, score_item in enumerate(socre_list):
        # print index
        # print score_item
        result = score_item[4] - score_item[5]
        # print result
        if result > 0:
            ss.update({"pos": ss['pos'] + 1})
        elif result < 0:
            ss.update({"neg": ss['neg'] + 1})
        else:
            ss.update({"midd": ss['midd'] + 1})
    if ss['pos'] > ss['neg']:
        analyzer_result.update({"senti_result": 1})
    elif ss['pos'] < ss['neg']:
        analyzer_result.update({"senti_result": -1})
    else:
        analyzer_result.update({"senti_result": 0})
    return analyzer_result


# data = '你就是个王八蛋，混账玩意!你们的手机真不好用！非常生气，我非常郁闷！！！！'
# data2= '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
# print(sentiment_score(sentiment_score_list(data2)))

# -*- coding: utf-8 -*-
from django.test import TestCase
from analyzer import senti_python
import re
def strs_filter(text_str):
    re_html = re.compile('<[^>]+>'.decode('utf8'))#从'<'开始匹配，不是'>'的字符都跳过，直到'>'
    # re_punc = re.compile('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，；。？、~@#￥%……&*（）]+'.decode('utf8'))#去除标点符号
    # re_digits_letter = re.compile('\w+'.decode('utf8'))#去除数字及字母
    text_str = re_html.sub('', text_str)
    # text_str = re_punc.sub("", text_str)
    # text_str = re_digits_letter.sub("", text_str)
    return text_str

# Create your tests here.
from snownlp import SnowNLP
text = """
这秘密主页君要报警了，鸽了TS4早早来备战，结果赛前一天6.86更新了，puppey哥被Wings怼成爱沙尼亚哈哈明了。。。。天台人多么？我想去看看！
"""
text = text.decode('utf-8')
# tests = text.split("\n").split("。").split(".")


text = strs_filter(text)
tests = re.split('。|！|？|\n'.decode('utf8'),text)
tests_f = list(filter(senti_python.not_empty, tests))
socre_list = senti_python.sentiment_score(senti_python.sentiment_score_list(tests_f))
ss = {"pos": 0, "neg": 0, "midd": 0}
for index, score_item in enumerate(socre_list):
    print index
    print score_item
    result = score_item[4]-score_item[5]
    print result
    if result > 0:
        ss.update({"pos": ss['pos']+1})
    elif result < 0:
        ss.update({"neg": ss['neg'] + 1})
    else:
        ss.update({"midd": ss['midd'] + 1})

print ss

# print text
# a1 = SnowNLP(text)
# a2 = a1.sentiments
#
# print(a1)
# print(a2)



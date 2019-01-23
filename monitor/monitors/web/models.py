# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
# Create your models here.


class User(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.CharField(max_length=50, blank=True, null=True)
    u_pwd = models.CharField(max_length=50, blank=True, null=True)
    u_last_login_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return "%s" % self.u_name


class MonitorTask(models.Model):
    # 任务名称 唯一
    mt_name = models.CharField(max_length=50, primary_key=True)
    # 关键字
    mt_keys = models.CharField(max_length=50, blank=True, null=True)
    # 数据源
    mt_sources = models.CharField(max_length=200, blank=True, null=True)
    # 数据源个数
    mt_source_counts = models.IntegerField(default=0)
    # 备注
    mt_remark = models.CharField(max_length=200, blank=True, null=True)
    # 0停止1运行中
    mt_status = models.IntegerField(default=0)
    # 创建时间
    mt_create_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # 上次运行时间
    mt_last_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return "%s" % self.mt_name


class WeiboSpider(models.Model):
    # 名称
    name = models.CharField(max_length=100, primary_key=True)
    # 1代表爬取的是微博账号，5代表爬取的是微博搜索页
    type = models.CharField(max_length=2, blank=True, null=True)
    start_url = models.CharField(max_length=255, blank=True, null=True)
    weibo_uid = models.CharField(max_length=255, blank=True, null=True)
    fensi_count = models.CharField(max_length=20, blank=True, null=True)
    weibo_count = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "%s" % self.name


class WeiBoContent(models.Model):
    # 微博内容id
    content_id = models.CharField(max_length=255, primary_key=True)
    # 所属微博spider id
    spider_id = models.CharField(max_length=50, blank=True, null=True)
    # 微博内容
    content_text = models.CharField(max_length=5000, blank=True, null=True)
    # 转发数
    reposts_count = models.CharField(max_length=20, blank=True, null=True)
    # 评论数
    comments_count = models.CharField(max_length=20, blank=True, null=True)
    # 点赞数
    attitudes_count = models.CharField(max_length=20, blank=True, null=True)
    # 作者
    create_user = models.CharField(max_length=50, blank=True, null=True)
    # 微博url地址
    weibo_url = models.CharField(max_length=200, blank=True, null=True)
    # 创建时间
    created_at = models.DateTimeField(blank=True, null=True)
    # 更新时间
    update_at = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return "%s" % self.content_id


class WeiBoPinglun(models.Model):
    # 微博内容评论id
    pinglun_id = models.CharField(max_length=100, primary_key=True)
    # 父评论 id
    pinglun_parent_id = models.CharField(max_length=100, blank=True, null=True)
    # 评论内容
    pinglun_text = models.CharField(max_length=5000, blank=True, null=True)
    # 创建时间
    created_at = models.DateTimeField(blank=True, null=True)
    # 子评论数
    sub_pinglun_count = models.CharField(max_length=20, blank=True, null=True)
    # 点赞数
    like_count = models.CharField(max_length=20, blank=True, null=True)
    # 楼层
    floor_number = models.CharField(max_length=20, blank=True, null=True)
    # 评论人
    pinglun_user = models.CharField(max_length=100, blank=True, null=True)
    # 所属微博
    weibo_content_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.pinglun_id


class XieChengSpider(models.Model):
    # 名称
    name = models.CharField(max_length=255, primary_key=True)
    # 爬取的页面类型 问答、游记、目的地专页等
    type = models.CharField(max_length=2, blank=True, null=True)
    # 游记、问答相关搜索结果数
    search_count = models.CharField(max_length=255, blank=True, null=True)
    # 爬虫起始页url
    start_url = models.CharField(max_length=255, blank=True, null=True)
    # 满意度
    satisfaction_score = models.CharField(max_length=255, blank=True, null=True)
    # 因为开始需求不明确，结构设计不是很好，在游轮专页代表所有评论数
    satisfaction_count = models.CharField(max_length=255, blank=True, null=True)
    # 满意
    fell_a_score = models.CharField(max_length=255, blank=True, null=True)
    fell_a_count = models.CharField(max_length=255, blank=True, null=True)
    # 一般
    fell_b_score = models.CharField(max_length=255, blank=True, null=True)
    fell_b_count = models.CharField(max_length=255, blank=True, null=True)
    # 不满意
    fell_c_score = models.CharField(max_length=255, blank=True, null=True)
    fell_c_count = models.CharField(max_length=255, blank=True, null=True)
    # 位置交通
    location_traffic = models.CharField(max_length=255, blank=True, null=True)
    # 行程安排
    travel_schedule = models.CharField(max_length=255, blank=True, null=True)
    # 餐饮住宿
    dining_room = models.CharField(max_length=255, blank=True, null=True)
    # 旅行交通
    travel_traffic = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.name


class XieChengPingLun(models.Model):
    # 评论id
    pl_id = models.CharField(max_length=100, primary_key=True)
    # 评论用户
    pl_user = models.CharField(max_length=50, blank=True, null=True)
    # 游玩类型 家庭。。。
    pl_travel_type = models.CharField(max_length=20, blank=True, null=True)
    # 整体评价
    pl_compGradeContent = models.CharField(max_length=10, blank=True, null=True)
    pl_compTextContent = models.CharField(max_length=5000, blank=True, null=True)
    # 评论日期
    pl_date = models.DateTimeField(blank=True, null=True)
    # 产品名称
    pl_prodect_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.pl_id


class XieChengSubPingLun(models.Model):
    # 子评论id
    sub_pl_id = models.IntegerField(primary_key=True)
    # sub评论类名
    sub_pl_notes = models.CharField(max_length=200, blank=True, null=True)
    # sub评论满意度
    sub_showGradeValue = models.CharField(max_length=50, blank=True, null=True)
    # 父评论id
    sub_parent_id = models.CharField(max_length=20, blank=True, null=True)
    # 子评论文字内容
    sub_pl_text = models.CharField(max_length=1000, blank=True, null=True)
    # 子评论类型id
    sub_pl_type = models.IntegerField(default=9999, blank=True, null=True)

    def __str__(self):
        return "%s" % self.sub_pl_id


# 携程搜索问答model
class XieChengAskCon(models.Model):
    # 问题id
    ask_id = models.CharField(max_length=255, primary_key=True)
    # 问题所属搜索任务名称
    ask_task_name = models.CharField(max_length=255, blank=True, null=True)
    # 问题
    ask_title = models.CharField(max_length=1000, blank=True, null=True)
    # 问题
    ask_question = models.CharField(max_length=4000, blank=True, null=True)
    # 问题发起人
    ask_user = models.CharField(max_length=255, blank=True, null=True)
    # 问题发起时间
    ask_date = models.DateTimeField(blank=True, null=True)
    # 被收藏数
    ask_collects = models.CharField(max_length=10, blank=True, null=True)
    # 被分享数
    ask_shares = models.CharField(max_length=10, blank=True, null=True)
    # 回答数
    ask_answers = models.CharField(max_length=10, blank=True, null=True)
    # 问答原始url
    ask_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "%s" % self.ask_id


# 携程搜索问答答案model
class XieChengAskAnswer(models.Model):
    # 答案id
    answer_id = models.CharField(max_length=255, primary_key=True)
    # 答案父id
    answer_parent_id = models.CharField(max_length=255, blank=True, null=True)
    # 答案所属问题
    answer_ask_id = models.CharField(max_length=255, blank=True, null=True)
    # 答案
    answer_con = models.CharField(max_length=4000, blank=True, null=True)
    # 答案回答人
    answer_user = models.CharField(max_length=255, blank=True, null=True)
    # 回答时间
    answer_date = models.DateTimeField(blank=True, null=True)
    # 子评论数
    answer_sub_counts = models.CharField(max_length=10, blank=True, null=True)
    # 有用数
    answer_uesd_counts = models.CharField(max_length=10, blank=True, null=True)
    # 是否被采纳
    answer_is_best = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return "%s" % self.answer_id


# 携程搜索游记model
class XieChengTravelNote(models.Model):
    # 游记id
    note_id = models.CharField(max_length=255, primary_key=True)
    # 游记所属搜索任务名称
    note_task_name = models.CharField(max_length=255, blank=True, null=True)
    # 游记标题
    note_title = models.CharField(max_length=1000, blank=True, null=True)
    # 游记内容
    note_content = models.TextField(blank=True, null=True)
    # 游记作者
    note_user = models.CharField(max_length=255, blank=True, null=True)
    # 游记发表时间
    note_date = models.DateTimeField(blank=True, null=True)
    # 游记爬取时间
    note_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # 评论数
    note_answers = models.CharField(max_length=10, blank=True, null=True)
    # 游记url
    note_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "%s" % self.note_id


# 携程搜索游记model
class XieChengTravelNoteAnswer(models.Model):
    # 游记评论id
    answer_id = models.CharField(max_length=255, primary_key=True)
    # 评论所属游记id
    answer_note_id = models.CharField(max_length=255, blank=True, null=True)
    # 评论内容
    answer_content = models.CharField(max_length=1000, blank=True, null=True)
    # 父评论内容
    answer_parent_content = models.CharField(max_length=1000, blank=True, null=True)
    # 评论作者
    answer_user = models.CharField(max_length=255, blank=True, null=True)
    # 评论发表时间
    answer_date = models.DateTimeField(blank=True, null=True)
    # 评论爬取时间
    answer_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return "%s" % self.answer_id


# 穷游
class QyerSpider(models.Model):
    # 名称
    name = models.CharField(max_length=255, primary_key=True)
    # 爬取的页面类型 1:帖子、2：问答
    type = models.CharField(max_length=2, blank=True, null=True)
    # 相关搜索结果数
    search_count = models.IntegerField(blank=True, null=True)
    # 爬虫起始页url
    start_url = models.CharField(max_length=255, blank=True, null=True)
    # 是否全量爬取
    is_all = models.CharField(max_length=1, blank=True, null=True)
    # 上次爬取时间
    last_scrapy_time = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "%s" % self.name


# 穷游帖子
class QyerBbs(models.Model):
    # 帖子id
    bbs_id = models.CharField(max_length=255, primary_key=True)
    # 帖子所属搜索任务名称
    bbs_task_name = models.CharField(max_length=255, blank=True, null=True)
    # 帖子标题
    bbs_title = models.CharField(max_length=1000, blank=True, null=True)
    # 帖子内容
    bbs_content = models.TextField(blank=True, null=True)
    # 帖子作者
    bbs_user = models.CharField(max_length=255, blank=True, null=True)
    # 帖子发表时间
    bbs_date = models.DateTimeField(blank=True, null=True)
    # 爬取时间
    bbs_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # 浏览量
    bbs_scan_counts = models.IntegerField(blank=True, null=True)
    # 评论数
    bbs_answer_counts = models.IntegerField(blank=True, null=True)
    # 喜欢的个数
    bbs_like_counts = models.IntegerField(blank=True, null=True)
    # url
    bbs_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.bbs_id


# 穷游问答
class QyerAsk(models.Model):
    # 问答id
    ask_id = models.CharField(max_length=255, primary_key=True)
    # 问答所属搜索任务名称
    ask_task_name = models.CharField(max_length=255, blank=True, null=True)
    # 问答标题
    ask_title = models.CharField(max_length=1000, blank=True, null=True)
    # 问答内容
    ask_content = models.TextField(blank=True, null=True)
    # 问答作者
    ask_user = models.CharField(max_length=255, blank=True, null=True)
    # 问答发表时间
    ask_date = models.DateTimeField(blank=True, null=True)
    # 爬取时间
    ask_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # # 浏览量
    # bbs_scan_counts = models.IntegerField(blank=True, null=True)
    # 评论数
    ask_answer_counts = models.IntegerField(blank=True, null=True)
    # url
    ask_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.ask_id


# 穷游问答答案
class QyerAskAnswer(models.Model):
    # 回答id
    answer_id = models.CharField(max_length=255, primary_key=True)
    # 回答所属问答id
    answer_ask_id = models.CharField(max_length=255, blank=True, null=True)
    # 回答父id
    answer_parent_id = models.CharField(max_length=255, blank=True, null=True)
    # 回答内容
    answer_content = models.CharField(max_length=4000, blank=True, null=True)
    # 回答作者
    answer_user = models.CharField(max_length=255, blank=True, null=True)
    # 问答发表时间
    answer_date = models.DateTimeField(blank=True, null=True)
    # 爬取时间
    answer_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # 子评论数
    answer_sub_counts = models.IntegerField(blank=True, null=True)
    # 点赞的个数
    answer_like_counts = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.answer_id


# 马蜂窝
class MafwSpider(models.Model):
    # 名称
    name = models.CharField(max_length=255, primary_key=True)
    # 爬取的页面类型 1:游记、2：问答
    type = models.CharField(max_length=2, blank=True, null=True)
    # 相关搜索结果数
    search_count = models.IntegerField(blank=True, null=True)
    # 爬虫起始页url
    start_url = models.CharField(max_length=255, blank=True, null=True)
    # 是否全量爬取
    is_all = models.CharField(max_length=1, blank=True, null=True)
    # 上次爬取时间
    last_scrapy_time = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "%s" % self.name


# 马蜂窝游记
class MafwTravelBook(models.Model):
    # 游记id
    book_id = models.CharField(max_length=255, primary_key=True)
    # 游记所属搜索任务名称
    book_task_name = models.CharField(max_length=255, blank=True, null=True)
    # 游记标题
    book_title = models.CharField(max_length=1000, blank=True, null=True)
    # 游记内容
    book_content = models.TextField(blank=True, null=True)
    # 游记作者
    book_user = models.CharField(max_length=255, blank=True, null=True)
    # 游记发表时间
    book_date = models.DateTimeField(blank=True, null=True)
    # 游记爬取时间
    book_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # 被浏览量
    book_scan_counts = models.IntegerField(blank=True, null=True)
    # 评论数
    booker_answer_counts = models.IntegerField(blank=True, null=True)
    # url
    book_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.book_id


# 马蜂窝问答
class MafwAsk(models.Model):
    # 问答id
    ask_id = models.CharField(max_length=255, primary_key=True)
    # 问答所属搜索任务名称
    ask_task_name = models.CharField(max_length=255, blank=True, null=True)
    # 问答标题
    ask_title = models.CharField(max_length=1000, blank=True, null=True)
    # 问答内容
    ask_content = models.TextField(blank=True, null=True)
    # 问答作者
    ask_user = models.CharField(max_length=255, blank=True, null=True)
    # 问答发表时间
    ask_date = models.DateTimeField(blank=True, null=True)
    # 爬取时间
    ask_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # 有用数
    ask_used_counts = models.IntegerField(blank=True, null=True)
    # 评论数
    ask_answer_counts = models.IntegerField(blank=True, null=True)
    # 同问的个数
    ask_same_counts = models.IntegerField(blank=True, null=True)
    # url
    ask_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % self.ask_id


# 马蜂窝问答答案
class MafwAskAnswer(models.Model):
    # 回答id
    answer_id = models.CharField(max_length=255, primary_key=True)
    # 回答所属问答id
    answer_ask_id = models.CharField(max_length=255, blank=True, null=True)
    # 回答父id
    answer_parent_id = models.CharField(max_length=255, blank=True, null=True)
    # 回答内容
    answer_content = models.CharField(max_length=8000, blank=True, null=True)
    # 回答作者
    answer_user = models.CharField(max_length=255, blank=True, null=True)
    # 问答发表时间
    answer_date = models.DateTimeField(blank=True, null=True)
    # 爬取时间
    answer_scrapy_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    # 子评论数
    answer_sub_counts = models.IntegerField(blank=True, null=True)
    # 顶的个数
    answer_like_counts = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.answer_id
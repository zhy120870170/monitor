# -*- coding: utf-8 -*-
from django.db import transaction
from spiderurlstr import *
from django.http import HttpResponse
import urllib
import logging
import redis
import openpyxl
import pagetools
from ..analyzer import senti_python
from ..models import *
from .. import settings

logger = logging.getLogger("create_new_monitor")


@transaction.atomic
def create_new_monitor(mt_name, mt_keys, mt_sources, mt_source_counts, mt_remark):
    MonitorTask.objects.create(
        mt_name=mt_name,
        mt_keys=mt_keys,
        mt_sources=mt_sources,
        mt_source_counts=mt_source_counts,
        mt_remark=mt_remark
    )
    # 创建微博spider
    weibo_spider_name = mt_name + "@搜索"
    try:
        weibo_spider_url = weibo_search_url_start + urllib.quote(
            mt_keys.encode('utf8')) + weibo_search_url_end
    except BaseException, e:
        logger.info("创建微博spider异常，url转码异常")
        print e
    WeiboSpider.objects.create(
        name=weibo_spider_name, type='5', weibo_uid=weibo_spider_name, start_url=weibo_spider_url
    )
    # 创建携程ask spider
    xiecheng_ask_spider_name = mt_name + "@问答"
    xiecheng_ask_spider_url = xiecheng_ask_search_url % (urllib.quote(mt_keys.encode('utf8')))
    XieChengSpider.objects.create(
        name=xiecheng_ask_spider_name, type='3', start_url=xiecheng_ask_spider_url
    )
    # 创建携程travel note spider
    xiecheng_travel_spider_name = mt_name + "@游记"
    xiecheng_travel_spider_url = xiecheng_travel_search_url % (urllib.quote(mt_keys.encode('utf8')))
    XieChengSpider.objects.create(
        name=xiecheng_travel_spider_name, type='4', start_url=xiecheng_travel_spider_url
    )
    # 创建马蜂窝ask spider
    mafw_ask_spider_name = mt_name + "@问答"
    mafw_ask_spider_url = mafw_ask_search_url % (urllib.quote(mt_keys.encode('utf8')))
    MafwSpider.objects.create(
        name=mafw_ask_spider_name, type='2', start_url=mafw_ask_spider_url
    )
    # 创建马蜂窝游记 spider
    mafw_travel_spider_name = mt_name + "@游记"
    mafw_travel_spider_url = mafw_travel_search_url % (urllib.quote(mt_keys.encode('utf8')))
    MafwSpider.objects.create(
        name=mafw_travel_spider_name, type='1', start_url=mafw_travel_spider_url
    )
    # 创建穷游网ask spider
    qyer_ask_spider_name = mt_name + "@问答"
    qyer_ask_spider_url = qyer_ask_search_url % (urllib.quote(mt_keys.encode('utf8')))
    QyerSpider.objects.create(
        name=qyer_ask_spider_name, type='2', start_url=qyer_ask_spider_url
    )
    # 创建穷游网bbs spider
    qyer_bbs_spider_name = mt_name + "@帖子"
    qyer_bbs_spider_url = qyer_bbs_search_url % (urllib.quote(mt_keys.encode('utf8')))
    QyerSpider.objects.create(
        name=qyer_bbs_spider_name, type='1', start_url=qyer_bbs_spider_url
    )


@transaction.atomic
def del_monitor(mt_name):
    MonitorTask.objects.filter(mt_name=mt_name).delete()
    # 删除微博spider
    weibo_spider_name = mt_name + "@搜索"
    WeiboSpider.objects.filter(name=weibo_spider_name).delete()

    # 创建携程ask spider
    xiecheng_ask_spider_name = mt_name + "@问答"
    XieChengSpider.objects.filter(name=xiecheng_ask_spider_name).delete()

    # 创建携程travel note spider
    xiecheng_travel_spider_name = mt_name + "@游记"
    XieChengSpider.objects.filter(name=xiecheng_travel_spider_name).delete()

    # 创建马蜂窝ask spider
    mafw_ask_spider_name = mt_name + "@问答"
    MafwSpider.objects.filter(name=mafw_ask_spider_name).delete()

    # 创建马蜂窝游记 spider
    mafw_travel_spider_name = mt_name + "@游记"
    MafwSpider.objects.filter(name=mafw_travel_spider_name).delete()
    # 创建穷游网ask spider
    qyer_ask_spider_name = mt_name + "@问答"
    QyerSpider.objects.filter(name=qyer_ask_spider_name).delete()

    # 创建穷游网bbs spider
    qyer_bbs_spider_name = mt_name + "@帖子"
    QyerSpider.objects.filter(name=qyer_bbs_spider_name).delete()


@transaction.atomic
def start_monitor(task_name):
    logging.info("开启任务==》" + task_name)
    task = MonitorTask.objects.get(mt_name=task_name)
    conn = redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, port=settings.REDIS_PORT)

    if task.mt_keys.strip():
        urlcode_word = urllib.quote(task.mt_keys.encode('utf8'))
        mt_sources_list = task.mt_sources.split(',')
        if "11" in mt_sources_list:
            conn.lpush('weibo_spider:start_urls', weibo_search_url_start + urlcode_word + weibo_search_url_end)

        if "21" in mt_sources_list:
            conn.lpush('xiecheng_spider:start_urls', xiecheng_ask_search_url % urlcode_word)

        if "22" in mt_sources_list:
            conn.lpush('xiecheng_spider:start_urls', xiecheng_travel_search_url % urlcode_word)

        if "31" in mt_sources_list:
            conn.lpush('mafw_spider:start_urls', mafw_ask_search_url % urlcode_word)

        if "32" in mt_sources_list:
            conn.lpush('mafw_spider:start_urls', mafw_travel_search_url % urlcode_word)

        if "41" in mt_sources_list:
            conn.lpush('qyer_spider:start_urls', qyer_ask_search_url % urlcode_word)

        if "42" in mt_sources_list:
            conn.lpush('qyer_spider:start_urls', qyer_bbs_search_url % urlcode_word)


def search_gather_detail(mt_name, mt_source, start_date_str, end_date_str, page_num):
    start_date = datetime.strptime(start_date_str + " 00:00:00", "%Y%m%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str + " 23:59:59", "%Y%m%d %H:%M:%S")

    if "11" == mt_source:
        weibo_data_list = WeiBoContent.objects.filter(spider_id=mt_name + "@搜索") \
            .filter(created_at__range=[start_date, end_date]) \
            .order_by('-created_at')
        page_split_result = pagetools.split_page(weibo_data_list, page_num, 15)

        data_counts = WeiBoContent.objects.filter(spider_id=mt_name + "@搜索")\
            .filter(created_at__range=[start_date, end_date])\
            .count()

        page_tools = create_page_tools(page_split_result, data_counts, page_num)

        page_split_items = list(page_split_result['page'])
        result_list = []
        for item in page_split_items:
            result_item = {
                "content_id": item.content_id,
                "content_text": item.content_text,
                "reposts_count": item.reposts_count,
                "comments_count": item.comments_count,
                "attitudes_count": item.attitudes_count,
                "create_user": item.create_user,
                "weibo_url": item.weibo_url,
                "created_at": item.created_at.strftime("%Y-%m-%d"),
            }
            result_list.append(result_item)

    if "21" == mt_source:
        xiecheng_ask_data_list = XieChengAskCon.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        page_split_result = pagetools.split_page(xiecheng_ask_data_list, page_num, 15)

        data_counts = XieChengAskCon.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .count()

        page_tools = create_page_tools(page_split_result, data_counts, page_num)

        page_split_items = list(page_split_result['page'])
        result_list = []
        for item in page_split_items:
            result_item = {
                "ask_id": item.ask_id,
                "ask_title": item.ask_title,
                "ask_question": item.ask_question,
                "ask_user": item.ask_user,
                "ask_collects": item.ask_collects if item.ask_collects else "0",
                "ask_shares": item.ask_shares if item.ask_shares else "0",
                "ask_answers": item.ask_answers if item.ask_answers else "0",
                "ask_url": item.ask_url,
                "ask_date": item.ask_date.strftime("%Y-%m-%d %H:%M"),
            }
            result_list.append(result_item)

    if "22" == mt_source:
        xiecheng_travel_data_list = XieChengTravelNote.objects.filter(note_task_name=mt_name + "@游记") \
            .filter(note_date__range=[start_date, end_date]) \
            .order_by('-note_date')
        page_split_result = pagetools.split_page(xiecheng_travel_data_list, page_num, 15)

        data_counts = XieChengTravelNote.objects.filter(note_task_name=mt_name + "@游记") \
            .filter(note_date__range=[start_date, end_date]) \
            .count()

        page_tools = create_page_tools(page_split_result, data_counts, page_num)

        page_split_items = list(page_split_result['page'])
        result_list = []
        for item in page_split_items:
            result_item = {
                "note_id": item.note_id,
                "note_title": item.note_title,
                "note_content": item.note_content,
                "note_user": item.note_user,
                "note_answers": item.note_answers if item.note_answers else "0",
                "note_url": item.note_url,
                "note_date": item.note_date.strftime("%Y-%m-%d"),
            }
            result_list.append(result_item)

    if "31" == mt_source:
        mafw_ask_data_list = MafwAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        page_split_result = pagetools.split_page(mafw_ask_data_list, page_num, 15)

        data_counts = MafwAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .count()

        page_tools = create_page_tools(page_split_result, data_counts, page_num)

        page_split_items = list(page_split_result['page'])
        result_list = []
        for item in page_split_items:
            result_item = {
                "ask_id": item.ask_id,
                "ask_title": item.ask_title,
                "ask_content": item.ask_content,
                "ask_user": item.ask_user,
                "ask_used_counts": item.ask_used_counts if item.ask_used_counts else "0",
                "ask_answer_counts": item.ask_answer_counts if item.ask_answer_counts else "0",
                "ask_same_counts": item.ask_same_counts if item.ask_same_counts else "0",
                "ask_url": item.ask_url,
                "ask_date": item.ask_date.strftime("%Y-%m-%d"),
            }
            result_list.append(result_item)

    if "32" == mt_source:
        mafw_travel_data_list = MafwTravelBook.objects.filter(book_task_name=mt_name + "@游记") \
            .filter(book_date__range=[start_date, end_date]) \
            .order_by('-book_date')
        page_split_result = pagetools.split_page(mafw_travel_data_list, page_num, 15)

        data_counts = MafwTravelBook.objects.filter(book_task_name=mt_name + "@游记") \
            .filter(book_date__range=[start_date, end_date]) \
            .count()

        page_tools = create_page_tools(page_split_result, data_counts, page_num)

        page_split_items = list(page_split_result['page'])
        result_list = []
        for item in page_split_items:
            result_item = {
                "book_id": item.book_id,
                "book_title": item.book_title,
                "book_content": item.book_content,
                "book_user": item.book_user,
                "booker_answer_counts": item.booker_answer_counts if item.booker_answer_counts else "0",
                "book_scan_counts": item.book_scan_counts if item.book_scan_counts else "0",
                "book_url": item.book_url,
                "book_date": item.book_date.strftime("%Y-%m-%d %H:%M"),
            }
            result_list.append(result_item)

    if "41" == mt_source:
        qyer_ask_data_list = QyerAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        page_split_result = pagetools.split_page(qyer_ask_data_list, page_num, 15)

        data_counts = QyerAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .count()

        page_tools = create_page_tools(page_split_result, data_counts, page_num)

        page_split_items = list(page_split_result['page'])
        result_list = []
        for item in page_split_items:
            result_item = {
                "ask_id": item.ask_id,
                "ask_title": item.ask_title,
                "ask_content": item.ask_content,
                "ask_user": item.ask_user,
                "ask_answer_counts": item.ask_answer_counts if item.ask_answer_counts else "0",
                "ask_url": item.ask_url,
                "ask_date": item.ask_date.strftime("%Y-%m-%d"),
            }
            result_list.append(result_item)

    if "42" == mt_source:
        qyer_bbs_data_list = QyerBbs.objects.filter(bbs_task_name=mt_name + "@帖子") \
            .filter(bbs_date__range=[start_date, end_date]) \
            .order_by('-bbs_date')
        page_split_result = pagetools.split_page(qyer_bbs_data_list, page_num, 15)

        data_counts = QyerBbs.objects.filter(bbs_task_name=mt_name + "@帖子") \
            .filter(bbs_date__range=[start_date, end_date]) \
            .count()

        page_tools = create_page_tools(page_split_result, data_counts, page_num)

        page_split_items = list(page_split_result['page'])
        result_list = []
        for item in page_split_items:
            result_item = {
                "bbs_id": item.bbs_id,
                "bbs_title": item.bbs_title,
                "bbs_content": item.bbs_content,
                "bbs_user": item.bbs_user,
                "bbs_scan_counts": item.bbs_scan_counts if item.bbs_scan_counts else "0",
                "bbs_answer_counts": item.bbs_answer_counts if item.bbs_answer_counts else "0",
                "bbs_like_counts": item.bbs_like_counts if item.bbs_like_counts else "0",
                "bbs_url": item.bbs_url,
                "bbs_date": item.bbs_date.strftime("%Y-%m-%d"),
            }
            result_list.append(result_item)

    return {"data_list": result_list, "page_tools": page_tools}


def get_top_detail(mt_name, mt_source, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str + " 00:00:00", "%Y%m%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str + " 23:59:59", "%Y%m%d %H:%M:%S")

    if "11" == mt_source:
        entry_list = list(WeiBoContent.objects.filter(spider_id=mt_name + "@搜索") \
                            .filter(created_at__range=[start_date, end_date]) \
                            .order_by('-created_at')
                          )
        result_list = []
        for item in entry_list:
            result_item = {
                "content_id": item.content_id,
                "content_text": item.content_text,
                "reposts_count": item.reposts_count,
                "comments_count": item.comments_count,
                "attitudes_count": item.attitudes_count,
                "create_user": item.create_user,
                "weibo_url": item.weibo_url,
                "created_at": item.created_at.strftime("%Y-%m-%d"),
                "sort_attr": str_to_int(item.reposts_count)+str_to_int(item.comments_count)+str_to_int(item.attitudes_count),
            }
            result_list.append(result_item)

    if "21" == mt_source:
        entry_list = list(XieChengAskCon.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date'))
        result_list = []
        for item in entry_list:
            result_item = {
                "ask_id": item.ask_id,
                "ask_title": item.ask_title,
                "ask_question": item.ask_question,
                "ask_user": item.ask_user,
                "ask_collects": item.ask_collects if item.ask_collects else "0",
                "ask_shares": item.ask_shares if item.ask_shares else "0",
                "ask_answers": item.ask_answers if item.ask_answers else "0",
                "ask_url": item.ask_url,
                "ask_date": item.ask_date.strftime("%Y-%m-%d %H:%M"),
                "sort_attr": str_to_int(item.ask_collects) + str_to_int(item.ask_shares) + str_to_int(
                    item.ask_answers),
            }
            result_list.append(result_item)

    if "22" == mt_source:
        entry_list = list(XieChengTravelNote.objects.filter(note_task_name=mt_name + "@游记") \
            .filter(note_date__range=[start_date, end_date]) \
            .order_by('-note_date'))

        result_list = []
        for item in entry_list:
            result_item = {
                "note_id": item.note_id,
                "note_title": item.note_title,
                "note_content": item.note_content,
                "note_user": item.note_user,
                "note_answers": item.note_answers if item.note_answers else "0",
                "note_url": item.note_url,
                "note_date": item.note_date.strftime("%Y-%m-%d"),
                "sort_attr": str_to_int(item.note_answers),
            }
            result_list.append(result_item)

    if "31" == mt_source:
        entry_list = list(MafwAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date'))

        result_list = []
        for item in entry_list:
            result_item = {
                "ask_id": item.ask_id,
                "ask_title": item.ask_title,
                "ask_content": item.ask_content,
                "ask_user": item.ask_user,
                "ask_used_counts": item.ask_used_counts if item.ask_used_counts else "0",
                "ask_answer_counts": item.ask_answer_counts if item.ask_answer_counts else "0",
                "ask_same_counts": item.ask_same_counts if item.ask_same_counts else "0",
                "ask_url": item.ask_url,
                "ask_date": item.ask_date.strftime("%Y-%m-%d"),
                "sort_attr": str_to_int(item.ask_used_counts)+str_to_int(item.ask_answer_counts)+str_to_int(item.ask_same_counts),
            }
            result_list.append(result_item)

    if "32" == mt_source:
        entry_list = list(MafwTravelBook.objects.filter(book_task_name=mt_name + "@游记") \
            .filter(book_date__range=[start_date, end_date]) \
            .order_by('-book_date'))
        result_list = []
        for item in entry_list:
            result_item = {
                "book_id": item.book_id,
                "book_title": item.book_title,
                "book_content": item.book_content,
                "book_user": item.book_user,
                "booker_answer_counts": item.booker_answer_counts if item.booker_answer_counts else "0",
                "book_scan_counts": item.book_scan_counts if item.book_scan_counts else "0",
                "book_url": item.book_url,
                "book_date": item.book_date.strftime("%Y-%m-%d %H:%M"),
                "sort_attr": str_to_int(item.booker_answer_counts) + str_to_int(item.book_scan_counts),
            }
            result_list.append(result_item)

    if "41" == mt_source:
        entry_list = list(QyerAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date'))
        result_list = []
        for item in entry_list:
            result_item = {
                "ask_id": item.ask_id,
                "ask_title": item.ask_title,
                "ask_content": item.ask_content,
                "ask_user": item.ask_user,
                "ask_answer_counts": item.ask_answer_counts if item.ask_answer_counts else "0",
                "ask_url": item.ask_url,
                "ask_date": item.ask_date.strftime("%Y-%m-%d"),
                "sort_attr": str_to_int(item.ask_answer_counts),
            }
            result_list.append(result_item)

    if "42" == mt_source:
        entry_list = list(QyerBbs.objects.filter(bbs_task_name=mt_name + "@帖子") \
            .filter(bbs_date__range=[start_date, end_date]) \
            .order_by('-bbs_date'))

        result_list = []
        for item in entry_list:
            result_item = {
                "bbs_id": item.bbs_id,
                "bbs_title": item.bbs_title,
                "bbs_content": item.bbs_content,
                "bbs_user": item.bbs_user,
                "bbs_scan_counts": item.bbs_scan_counts if item.bbs_scan_counts else "0",
                "bbs_answer_counts": item.bbs_answer_counts if item.bbs_answer_counts else "0",
                "bbs_like_counts": item.bbs_like_counts if item.bbs_like_counts else "0",
                "bbs_url": item.bbs_url,
                "bbs_date": item.bbs_date.strftime("%Y-%m-%d"),
                "sort_attr": str_to_int(item.bbs_scan_counts)+str_to_int(item.bbs_answer_counts)+str_to_int(item.bbs_like_counts),
            }
            result_list.append(result_item)

    result_list = sorted(result_list, key=lambda x: x['sort_attr'], reverse=True)
    return {"data_list": result_list[:10]}


def export_execl_by_source(mt_name, mt_source, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str + " 00:00:00", "%Y%m%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str + " 23:59:59", "%Y%m%d %H:%M:%S")
    execl_date_str = "（%s-%s）" % (datetime.strftime(start_date, "%Y%m%d"), datetime.strftime(end_date, "%Y%m%d"))

    response = HttpResponse(content_type='application/octet-stream')

    workbook = openpyxl.Workbook()  # 创建工作簿
    sheet = workbook.active

    if "11" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_微博").decode('unicode_escape')
        sheet.title = unicode("微博%s" % execl_date_str, "utf-8")
        sheet.append([u'微博内容', u'转发数', u'评论数', u'点赞数', u'发表日期', u'作者', u'原始url'])
        data = WeiBoContent.objects.filter(spider_id=mt_name + "@搜索") \
            .filter(created_at__range=[start_date, end_date]) \
            .order_by('-created_at')
        for d in data:
            sheet.append([d.content_text, d.reposts_count, d.comments_count, d.attitudes_count,
                          d.created_at.strftime("%Y-%m-%d"), d.create_user, d.weibo_url])

    if "21" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_携程问答").decode('unicode_escape')
        sheet.title = "携程问答（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'问题名称', u'问题内容', u'作者', u'收藏数', u'分享数', u'回答数', u'发表日期', u'原始url'])
        data = XieChengAskCon.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        for d in data:
            sheet.append([d.ask_title, d.ask_question, d.ask_user, d.ask_collects if d.ask_collects else "0",
                          d.ask_shares if d.ask_shares else "0", d.ask_answers if d.ask_answers else "0",
                          d.ask_date.strftime("%Y-%m-%d %H:%M"), d.ask_url])

    if "22" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_携程游记").decode('unicode_escape')
        sheet.title = "携程游记（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'游记标题', u'作者', u'评论数', u'发表时间', u'游记内容', u'原始url'])
        data = XieChengTravelNote.objects.filter(note_task_name=mt_name + "@游记") \
            .filter(note_date__range=[start_date, end_date]) \
            .order_by('-note_date')
        for d in data:
            sheet.append([d.note_title, d.note_user, d.note_answers if d.note_answers else "0",
                          d.note_date.strftime("%Y-%m-%d"),
                          d.note_content, d.note_url])

    if "31" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_马蜂窝问答").decode('unicode_escape')
        sheet.title = "马蜂窝问答（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'内容', u'作者', u'有用数', u'评论数', u'同问数', u'发表日期', u'原始url'])
        data = MafwAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        for d in data:
            sheet.append([d.ask_title, d.ask_content, d.ask_user,
                          d.ask_used_counts if d.ask_used_counts else "0",
                          d.ask_answer_counts if d.ask_answer_counts else "0",
                          d.ask_same_counts if d.ask_same_counts else "0",
                          d.ask_date.strftime("%Y-%m-%d"),
                          d.ask_url])

    if "32" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_马蜂窝游记").decode('unicode_escape')
        sheet.title = "马蜂窝游记（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'作者', u'发表时间', u'评论数', u'浏览量', u'内容', u'原始url'])
        data = MafwTravelBook.objects.filter(book_task_name=mt_name + "@游记") \
            .filter(book_date__range=[start_date, end_date]) \
            .order_by('-book_date')
        for d in data:
            sheet.append([d.book_title, d.book_user, d.book_date.strftime("%Y-%m-%d %H:%M"),
                          d.booker_answer_counts if d.booker_answer_counts else "0",
                          d.book_scan_counts if d.book_scan_counts else "0",
                          d.book_content,
                          d.book_url])

    if "41" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_穷游问答").decode('unicode_escape')
        sheet.title = "穷游问答（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'内容', u'作者', u'评论数', u'发表日期', u'原始url'])
        data = QyerAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        for d in data:
            sheet.append([d.ask_title, d.ask_content, d.ask_user,
                          d.ask_answer_counts if d.ask_answer_counts else "0",
                          d.ask_date.strftime("%Y-%m-%d"),
                          d.ask_url])

    if "42" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_穷游帖子").decode('unicode_escape')
        sheet.title = "穷游帖子（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'作者', u'发表时间', u'评论数', u'浏览量', u'喜欢', u'内容', u'原始url'])
        data = QyerBbs.objects.filter(bbs_task_name=mt_name + "@帖子") \
            .filter(bbs_date__range=[start_date, end_date]) \
            .order_by('-bbs_date')
        for d in data:
            sheet.append([d.bbs_title, d.bbs_user, d.bbs_date.strftime("%Y-%m-%d"),
                          d.bbs_answer_counts if d.bbs_answer_counts else "0",
                          d.bbs_scan_counts if d.bbs_scan_counts else "0",
                          d.bbs_like_counts if d.bbs_like_counts else "0",
                          d.bbs_content,
                          d.bbs_url])

    try:
        workbook.save(response)
    except BaseException, e:
        raise e
    return response


def export_top_by_source(mt_name, mt_source, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str + " 00:00:00", "%Y%m%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str + " 23:59:59", "%Y%m%d %H:%M:%S")
    execl_date_str = "（%s-%s）" % (datetime.strftime(start_date, "%Y%m%d"), datetime.strftime(end_date, "%Y%m%d"))

    response = HttpResponse(content_type='application/octet-stream')

    workbook = openpyxl.Workbook()  # 创建工作簿
    sheet = workbook.active

    if "11" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_微博top10").decode('unicode_escape')
        sheet.title = unicode("微博top10%s" % execl_date_str, "utf-8")
        sheet.append([u'微博内容', u'转发数', u'评论数', u'点赞数', u'发表日期', u'作者', u'原始url'])
        data = get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        for d in data['data_list']:
            sheet.append([d['content_text'], d['reposts_count'], d['comments_count'], d['attitudes_count'],
                          d['created_at'], d['create_user'], d['weibo_url']])

    if "21" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_携程问答top10").decode('unicode_escape')
        sheet.title = "携程问答top10（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'问题名称', u'问题内容', u'作者', u'收藏数', u'分享数', u'回答数', u'发表日期', u'原始url'])
        data = get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        for d in data['data_list']:
            sheet.append([d['ask_title'], d['ask_question'], d['ask_user'], d['ask_collects'],
                          d['ask_shares'],
                          d['ask_date'], d['ask_url']])

    if "22" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_携程游记top10").decode('unicode_escape')
        sheet.title = "携程游记top10（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'游记标题', u'作者', u'评论数', u'发表时间', u'游记内容', u'原始url'])
        data = get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        for d in data['data_list']:
            sheet.append([d['note_title'], d['note_user'], d['note_answers'],
                          d['note_date'],
                          d['note_content'], d['note_url']])

    if "31" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_马蜂窝问答top10").decode('unicode_escape')
        sheet.title = "马蜂窝问答top10（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'内容', u'作者', u'有用数', u'评论数', u'同问数', u'发表日期', u'原始url'])
        data = get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        for d in data['data_list']:
            sheet.append([d['ask_title'], d['ask_content'], d['ask_user'],
                          d['ask_used_counts'],
                          d['ask_answer_counts'],
                          d['ask_same_counts'],
                          d['ask_date'],
                          d['ask_url']])

    if "32" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_马蜂窝游记top10").decode('unicode_escape')
        sheet.title = "马蜂窝游记top10（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'作者', u'发表时间', u'评论数', u'浏览量', u'内容', u'原始url'])
        data = get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        for d in data['data_list']:
            sheet.append([d['book_title'], d['book_user'], d['book_date'],
                          d['booker_answer_counts'],
                          d['book_scan_counts'],
                          d['book_content'],
                          d['book_url']])

    if "41" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_穷游问答top10").decode('unicode_escape')
        sheet.title = "穷游问答top10（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'内容', u'作者', u'评论数', u'发表日期', u'原始url'])
        data = get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        for d in data['data_list']:
            sheet.append([d['ask_title'], d['ask_content'], d['ask_user'],
                          d['ask_answer_counts'],
                          d['ask_date'],
                          d['ask_url']])

    if "42" == mt_source:
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (mt_name + "_穷游帖子top10").decode('unicode_escape')
        sheet.title = "穷游帖子top10（%s-%s）" % (start_date_str, end_date_str)
        sheet.append([u'标题', u'作者', u'发表时间', u'评论数', u'浏览量', u'喜欢', u'内容', u'原始url'])
        data = get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        for d in data['data_list']:
            sheet.append([d['bbs_title'], d['bbs_user'], d['bbs_date'],
                          d['bbs_answer_counts'],
                          d['bbs_scan_counts'],
                          d['bbs_like_counts'],
                          d['bbs_content'],
                          d['bbs_url']])

    try:
        workbook.save(response)
    except BaseException, e:
        raise e
    return response


def create_page_tools(page_split_result, data_counts, page_num):
    paginator = page_split_result['paginator']
    page = page_split_result['page']
    all_page = paginator.num_pages
    has_next = False
    has_previous = False
    previous_page_number = 0
    next_page_num = 0
    if page.has_next():
        has_next = True
        next_page_num = page.next_page_number()
    if page.has_previous():
        has_previous = True
        previous_page_number = page.previous_page_number()
    page_tools = {"all_counts": data_counts, "cur_page": page_num, "all_page": all_page,
                  "next_page_num": next_page_num, "previous_page_number": previous_page_number,
                  "has_next": has_next, "has_previous": has_previous,
                  "dis_range": page_split_result['dis_range']}
    return page_tools


def get_analyzer_senti(mt_name, mt_source, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str + " 00:00:00", "%Y%m%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str + " 23:59:59", "%Y%m%d %H:%M:%S")
    all_word_list = []
    word_cloud_result = []
    senti_analyzer_result = {"pos": 0, "neg": 0, "midd": 0, "title": 0}
    if "11" == mt_source:
        data = WeiBoContent.objects.filter(spider_id=mt_name + "@搜索") \
            .filter(created_at__range=[start_date, end_date]) \
            .order_by('-created_at')
        for d in data:
            senti_str = d.content_text
            analyzer_result = senti_python.senti_content(senti_str)
            senti_result = analyzer_result['senti_result']
            word_list = analyzer_result['word_list']
            all_word_list.extend(word_list)
            senti_analyzer_result.update({"title": senti_analyzer_result['title'] + 1})
            if senti_result > 0:
                senti_analyzer_result.update({"pos": senti_analyzer_result['pos'] + 1})
            elif senti_result < 0:
                senti_analyzer_result.update({"neg": senti_analyzer_result['neg'] + 1})
            else:
                senti_analyzer_result.update({"midd": senti_analyzer_result['midd'] + 1})
        # 情感分析结果
        senti_analyzer_result.update({"title": "微博情感分析：（共%d条）" % senti_analyzer_result['title']})

    if "21" == mt_source:
        data = XieChengAskCon.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        for d in data:
            senti_str = d.ask_title + d.ask_question
            analyzer_result = senti_python.senti_content(senti_str)
            senti_result = analyzer_result['senti_result']
            word_list = analyzer_result['word_list']
            all_word_list.extend(word_list)
            senti_analyzer_result.update({"title": senti_analyzer_result['title'] + 1})
            if senti_result > 0:
                senti_analyzer_result.update({"pos": senti_analyzer_result['pos'] + 1})
            elif senti_result < 0:
                senti_analyzer_result.update({"neg": senti_analyzer_result['neg'] + 1})
            else:
                senti_analyzer_result.update({"midd": senti_analyzer_result['midd'] + 1})
        senti_analyzer_result.update({"title": "携程问答情感分析：（共%d条）" % senti_analyzer_result['title']})

    if "22" == mt_source:
        data = XieChengTravelNote.objects.filter(note_task_name=mt_name + "@游记") \
            .filter(note_date__range=[start_date, end_date]) \
            .order_by('-note_date')
        for d in data:
            senti_str = d.note_title + d.note_content
            analyzer_result = senti_python.senti_content(senti_str)
            senti_result = analyzer_result['senti_result']
            word_list = analyzer_result['word_list']
            all_word_list.extend(word_list)
            senti_analyzer_result.update({"title": senti_analyzer_result['title'] + 1})
            if senti_result > 0:
                senti_analyzer_result.update({"pos": senti_analyzer_result['pos'] + 1})
            elif senti_result < 0:
                senti_analyzer_result.update({"neg": senti_analyzer_result['neg'] + 1})
            else:
                senti_analyzer_result.update({"midd": senti_analyzer_result['midd'] + 1})
        senti_analyzer_result.update({"title": "携程游记情感分析：（共%d条）" % senti_analyzer_result['title']})

    if "31" == mt_source:
        data = MafwAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        for d in data:
            senti_str = d.ask_title + d.ask_content
            analyzer_result = senti_python.senti_content(senti_str)
            senti_result = analyzer_result['senti_result']
            word_list = analyzer_result['word_list']
            all_word_list.extend(word_list)
            senti_analyzer_result.update({"title": senti_analyzer_result['title'] + 1})
            if senti_result > 0:
                senti_analyzer_result.update({"pos": senti_analyzer_result['pos'] + 1})
            elif senti_result < 0:
                senti_analyzer_result.update({"neg": senti_analyzer_result['neg'] + 1})
            else:
                senti_analyzer_result.update({"midd": senti_analyzer_result['midd'] + 1})
        senti_analyzer_result.update({"title": "马蜂窝问答情感分析：（共%d条）" % senti_analyzer_result['title']})

    if "32" == mt_source:
        data = MafwTravelBook.objects.filter(book_task_name=mt_name + "@游记") \
            .filter(book_date__range=[start_date, end_date]) \
            .order_by('-book_date')
        for d in data:
            senti_str = d.book_title + d.book_content
            analyzer_result = senti_python.senti_content(senti_str)
            senti_result = analyzer_result['senti_result']
            word_list = analyzer_result['word_list']
            all_word_list.extend(word_list)
            senti_analyzer_result.update({"title": senti_analyzer_result['title'] + 1})
            if senti_result > 0:
                senti_analyzer_result.update({"pos": senti_analyzer_result['pos'] + 1})
            elif senti_result < 0:
                senti_analyzer_result.update({"neg": senti_analyzer_result['neg'] + 1})
            else:
                senti_analyzer_result.update({"midd": senti_analyzer_result['midd'] + 1})
        senti_analyzer_result.update({"title": "马蜂窝游记情感分析：（共%d条）" % senti_analyzer_result['title']})

    if "41" == mt_source:
        data = QyerAsk.objects.filter(ask_task_name=mt_name + "@问答") \
            .filter(ask_date__range=[start_date, end_date]) \
            .order_by('-ask_date')
        for d in data:
            senti_str = d.ask_title + d.ask_content
            analyzer_result = senti_python.senti_content(senti_str)
            senti_result = analyzer_result['senti_result']
            word_list = analyzer_result['word_list']
            all_word_list.extend(word_list)
            senti_analyzer_result.update({"title": senti_analyzer_result['title'] + 1})
            if senti_result > 0:
                senti_analyzer_result.update({"pos": senti_analyzer_result['pos'] + 1})
            elif senti_result < 0:
                senti_analyzer_result.update({"neg": senti_analyzer_result['neg'] + 1})
            else:
                senti_analyzer_result.update({"midd": senti_analyzer_result['midd'] + 1})
        senti_analyzer_result.update({"title": "穷游问答情感分析：（共%d条）" % senti_analyzer_result['title']})

    if "42" == mt_source:
        data = QyerBbs.objects.filter(bbs_task_name=mt_name + "@帖子") \
            .filter(bbs_date__range=[start_date, end_date]) \
            .order_by('-bbs_date')
        for d in data:
            senti_str = d.bbs_title + d.bbs_content
            analyzer_result = senti_python.senti_content(senti_str)
            senti_result = analyzer_result['senti_result']
            word_list = analyzer_result['word_list']
            all_word_list.extend(word_list)
            senti_analyzer_result.update({"title": senti_analyzer_result['title'] + 1})
            if senti_result > 0:
                senti_analyzer_result.update({"pos": senti_analyzer_result['pos'] + 1})
            elif senti_result < 0:
                senti_analyzer_result.update({"neg": senti_analyzer_result['neg'] + 1})
            else:
                senti_analyzer_result.update({"midd": senti_analyzer_result['midd'] + 1})
        senti_analyzer_result.update({"title": "穷游帖子情感分析：（共%d条）" % senti_analyzer_result['title']})

    # 词云统计结果
    for i in set(all_word_list):
        if not senti_python.is_stop_word(i):
            word_cloud_result.append({"name": i, "value": all_word_list.count(i)})

    word_cloud_result = sorted(word_cloud_result, key=lambda x: x['value'], reverse=True)
    return {"senti_result": senti_analyzer_result, "word_cloud_result": word_cloud_result}


def str_to_int(inStr):
    try:
        return int(inStr)
    except BaseException:
        return 0

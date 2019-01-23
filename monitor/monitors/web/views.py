# -*- coding: utf-8 -*-
from django.shortcuts import render
import redis
from models import *
from tools import pagetools
from tools import datetools
from tools import monitorManage
from django.http import HttpResponse
from django.db import connections
from apscheduler.schedulers.background import BackgroundScheduler
import settings
import json
import logging
logging.basicConfig()


logger = logging.getLogger('web')


def login(request):
    return render(request, 'login.html')


def login_in(request):
    result = {"success": False, "message": "失败！"}

    if request.method == 'POST':
        u_name = request.POST.get('u_name')
        u_pwd = request.POST.get('u_pwd')
        try:
            passwd_db = User.objects.get(u_name=u_name).u_pwd
            if u_pwd == passwd_db:
                request.session['username'] = u_name
                request.session.set_expiry(24*60*60)
                result = {"success": True, "message": "成功！"}
            else:
                result = {"success": False, "message": "失败！"}
        except BaseException, e:
            result = {"success": False, "message": "失败！"}
    json_result = json.dumps(result)
    return HttpResponse(json_result)


def login_out(request):
    result = {"success": False, "message": "失败！"}
    if request.method == 'POST':
        try:
            del request.session['username']
            result = {"success": True, "message": "成功！"}
        except BaseException, e:
            result = {"success": False, "message": "失败！"}
    json_result = json.dumps(result)
    return HttpResponse(json_result)


def tasks(request):
    logger.debug("test")
    searchKey = request.GET.get('searchKey', default="")
    if searchKey:
        tasklist = MonitorTask.objects.filter(mt_name__contains=searchKey).order_by('-mt_create_date')
        task_counts = MonitorTask.objects.filter(mt_name__contains=searchKey).count()
    else:
        tasklist = MonitorTask.objects.order_by('-mt_create_date')
        task_counts = MonitorTask.objects.count()

    # 取出当前需要展示的页码, 默认为1
    page_num = request.GET.get('page', default='1')

    data = pagetools.split_page(tasklist, page_num, 15)
    data['all_counts'] = task_counts
    data['searchKey'] = searchKey
    return render(request, 'tasklist.html', data)


def edit_task(request):
    mt_name = request.GET.get('mt_name', default="")
    monitor_task = None
    try:
        monitor_task = MonitorTask.objects.get(mt_name=mt_name)
    except BaseException, e:
        print e
    return render(request, 'taskedit.html', {"monitor_task": monitor_task})


def del_task(request):
    result = {"success": True, "message": "成功！"}
    mt_name = request.GET.get('task_name')
    try:
        monitorManage.del_monitor(mt_name)
    except:
        result = {"success": False, "message": "失败！"}
    json_result = json.dumps(result)
    return HttpResponse(json_result)


def analyzer_task(request):
    mt_name = request.GET.get('task_name')
    all_task = MonitorTask.objects.order_by('-mt_create_date')
    result = {}
    data_start_date = datetools.get_previous_date(30).strftime('%Y%m%d')
    data_end_date = datetime.now().strftime('%Y%m%d')
    for index, item in enumerate(all_task):
        source_item = item.mt_sources.split(",")
        if index == 0 and mt_name is None:
            result_item = {"selected": "selected", "sources_keys": source_item, "sources_keys_str": item.mt_sources, "mt_keys": item.mt_keys}
        elif mt_name == item.mt_name:
            result_item = {"selected": "selected", "sources_keys": source_item, "sources_keys_str": item.mt_sources, "mt_keys": item.mt_keys}
        else:
            result_item = {"selected": "", "sources_keys": source_item, "sources_keys_str": item.mt_sources, "mt_keys": item.mt_keys}
        result.update({item.mt_name: result_item})
    return render(request, 'analyzer.html', {"data": result, "data_start_date": data_start_date, "data_end_date": data_end_date})


def start_single_task(request):
    mt_name = request.GET.get('task_name')
    monitorManage.start_monitor(mt_name)


def edit_task_submit(request):
    result = {"success": True, "message": "成功！"}

    is_add = request.POST.get('is_add')
    check_box_list = request.POST.getlist('task_data_source')
    mt_source = ",".join(check_box_list)
    mt_source_counts = len(check_box_list)
    mt_name = request.POST.get('task_name')
    mt_keys = request.POST.get('task_key')
    mt_remark = request.POST.get('remark')
    if "True" == is_add:
        old_task = MonitorTask.objects.filter(mt_name=mt_name)
        if old_task:
            result['success'] = False
            result['message'] = "任务名已存在！"
        else:
            try:
                monitorManage.create_new_monitor(mt_name, mt_keys, mt_source, mt_source_counts, mt_remark)
            except BaseException, e:
                logging.error("创建任务失败==》" + str(e))
                result['success'] = False
                result['message'] = str(e)
    else:
        try:
            old_task = MonitorTask.objects.get(mt_name=mt_name)
            old_task.mt_keys = mt_keys
            old_task.mt_sources = mt_source
            old_task.mt_source_counts = mt_source_counts
            old_task.mt_remark = mt_remark
            old_task.save()
        except BaseException, e:
            result['success'] = False
            result['message'] = e

    json_result = json.dumps(result)
    return HttpResponse(json_result)


def get_gather_detail(request):

    mt_name = request.GET.get('task_name')
    mt_source = request.GET.get('data_source')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    exportExecl_method_str = "exportExecl('" + mt_name + "','" + mt_source + "','" \
                             + start_date_str + "','" + end_date_str + "');"
    try:
        page_num = request.GET.get('page', default='1')
        datas = monitorManage.search_gather_detail(mt_name, mt_source, start_date_str, end_date_str, page_num)

        result = {"success": True, "message": "成功！", "datas": datas, "exportExecl_method": exportExecl_method_str}

        json_result = json.dumps(result)
    except BaseException, e:
        print e
    return HttpResponse(json_result)


def get_top10(request):
    mt_name = request.GET.get('task_name')
    mt_source = request.GET.get('data_source')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    exportExecl_method_str = "exportTop10Execl('" + mt_name + "','" + mt_source + "','" \
                             + start_date_str + "','" + end_date_str + "');"
    try:
        datas = monitorManage.get_top_detail(mt_name, mt_source, start_date_str, end_date_str)
        result = {"success": True, "message": "成功！", "datas": datas, "exportExecl_method": exportExecl_method_str}
        json_result = json.dumps(result)
    except BaseException, e:
        print e
    return HttpResponse(json_result)


def get_analyzer_senti(request):
    mt_name = request.GET.get('task_name')
    mt_source = request.GET.get('data_source')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    try:
        datas = monitorManage.get_analyzer_senti(mt_name, mt_source, start_date_str, end_date_str)
        result = {"success": True, "message": "成功！", "datas": datas}
        json_result = json.dumps(result)
    except BaseException, e:
        print e
    return HttpResponse(json_result)


def export_execl(request,mt_name, mt_source, start_date_str, end_date_str):
    try:
        response = monitorManage.export_execl_by_source(mt_name, mt_source, start_date_str, end_date_str)
    except BaseException, e:
        logging.info("导出execl异常：》" + str(e))
        print e
    return response


def exportTop10Execl(request,mt_name, mt_source, start_date_str, end_date_str):
    try:
        response = monitorManage.export_top_by_source(mt_name, mt_source, start_date_str, end_date_str)
    except BaseException, e:
        logging.info("导出execl异常：》" + str(e))
        print e
    return response


# 添加爬虫定时任务
scheduler = BackgroundScheduler()
def start_cron_task_main():
    msg = "已开启！"
    conn = redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, port=settings.REDIS_PORT)
    is_started = conn.get('cron_job')
    if not is_started:
        try:
            # jobs = scheduler.get_jobs(jobstore="default")
            jobs = scheduler.get_job(job_id="cron_job")
            if not jobs:
                # scheduler.add_job(cronjob, 'cron', day_of_week='0-6', hour=settings.CRON_HOUR, minute=settings.CRON_MINUTE, id="cron_job")
                scheduler.add_job(cronjob, 'cron', day_of_week='0-6', hour='*', minute=settings.CRON_MINUTE,
                                  id="cron_job")
                scheduler.start()
                conn.set("cron_job", "started", ex=300)
                msg = "开启成功！"
                # register_events(scheduler)
        except BaseException, e:
            print e
    print msg


def cronjob():
    close_old_connections()
    jobs = MonitorTask.objects.all()
    for job in jobs:
        monitorManage.start_monitor(job.mt_name)


# 在定时任务的调度线程里，如果长时间没有数据库的请求，连接会超时，再次调用会出现sql server gone away异常，所有在定时任务操作数据库之前先清除旧的异常链接
def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.tasks),
    url(r'^tasklist$', views.tasks),
    url(r'^editTask$', views.edit_task),
    url(r'^edit_task_submit$', views.edit_task_submit),
    url(r'^del_task$', views.del_task),
    url(r'^start_task$', views.start_single_task),
    url(r'^analyzer$', views.analyzer_task),
    url(r'^get_gather_detail$', views.get_gather_detail),
    url(r'^login_in$', views.login_in),
    url(r'^login$', views.login),
    url(r'^login_out$', views.login_out),
    url(r'^exportExecl/(.*)/(.*)/(.*)/(.*)', views.export_execl),
    url(r'^exportTop10Execl/(.*)/(.*)/(.*)/(.*)', views.exportTop10Execl),
    url(r'^get_analyzer_senti$', views.get_analyzer_senti),
    url(r'^get_top$', views.get_top10),
    # url(r'^weibo_pinglun/(.*)', views.weibo_pinglun),
    # url(r'^xiecheng/travel_note/(.*)', views.xiecheng_travel_note),
    # url(r'^xiecheng/ask_con/(.*)', views.xiecheng_ask_content),
    # url(r'^qunar/travel_book/(.*)', views.qunar_travel_book),
    # url(r'^qunar/ask_con/(.*)', views.qunar_ask_con),
    # url(r'^mafw/travel_book/(.*)', views.mafw_travel_book),
    # url(r'^mafw/ask_con/(.*)', views.mafw_ask_con),
    # url(r'^qyer/bbs/(.*)', views.qyer_bbs),
    # url(r'^qyer/asks/(.*)', views.qyer_asks)
]

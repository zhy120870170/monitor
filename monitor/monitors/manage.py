# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitors.settings")

    # 开启定时任务
    from web import views
    views.start_cron_task_main()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

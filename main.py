import os
import time
import threading
import logging
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpu_tasker.settings")
django.setup()

from base.utils import get_admin_config
from task.models import GPUTask
from task.utils import run_task
from gpu_info.utils import GPUInfoUpdater


django.setup()
from gpu_info.models import GPUServer
from django.contrib.auth.models import User
from task.models import GPUTask

import sys
import time

import argparse

task_logger = logging.getLogger('django.task')


if __name__ == '__main__':
    while True:
<<<<<<< HEAD

        try:
            task_logger.info('Running processes: {:d}'.format(threading.active_count()-1))

            for thread in threading.enumerate():
                print(thread.name)

            start_time = time.time()
            gpu_updater.update_gpu_info()


            with open( "./cmds_to_run.txt", "r" ) as fr, open( "./cmds_added.txt", "a" ) as fw:

                for i, line in enumerate( fr ):
                    task = eval(line)
                    fw.write( line )
                    task_name = task["task_name"]
                    task_workspace = task["task_workspace"]
                    memory_requirement = task["memory_requirement"]
                    cmd = task["cmd"]

                    print( "adding:", i, task )
                    task_instance = GPUTask()
                    task_instance.name = f"{task_name}_{i}" 
                    task_instance.workspace = task_workspace
                    task_instance.memory_requirement = memory_requirement
                    task_instance.utilization_requirement = 0
                    task_instance.cmd = cmd
                    task_instance.user = User.objects.get(username='han')
                    task_instance.status = 0
                    # task_instance.assign_server = GPUServer.objects.get(hostname="datalab5.engr.tamu.edu")
                    task_instance.save()

            with open( "./cmds_to_run.txt", "r+" ) as fr:
                fr.truncate()




            # STATUS_CHOICE = (
            #     (-2, '未就绪'),
            #     (-1, '运行失败'),
            #     (0, '准备就绪'),
            #     (1, '运行中'),
            #     (2, '已完成'),
            # )

            if len( GPUTask.objects.filter(status=0) ) == 0:
                for task in GPUTask.objects.filter(status=-1):
                    if task.traial <= 10:
                        task.status = 0
                        task.save()

            for task in GPUTask.objects.filter(status=1):
                print("runing:", task)

            for task in GPUTask.objects.filter(status=0):
                print("ready:", task)


            for task in GPUTask.objects.filter(status=-1):
                print("failure:", task)


            for task in GPUTask.objects.filter(status=0):
                gpu_updater.update_gpu_info()
                available_server = task.find_available_server()
                print("available_server:", available_server)

                if available_server is not None:
                    t = threading.Thread(target=run_task, args=(task, available_server))
                    t.start()
                    task.traial += 1
                    task.save()
                    time.sleep(1)


            end_time = time.time()

            # 确保至少间隔十秒更新一次
            duration = end_time - start_time
            if duration < 10:
                time.sleep(10 - duration)
        except Exception as e:
            print( e )
=======
        start_time = time.time()
        try:
            server_username, server_private_key_path = get_admin_config()
            gpu_updater = GPUInfoUpdater(server_username, server_private_key_path)

            task_logger.info('Running processes: {:d}'.format(
                threading.active_count() - 1
            ))

            gpu_updater.update_gpu_info()
            for task in GPUTask.objects.filter(status=0):
                available_server = task.find_available_server()
                if available_server is not None:
                    t = threading.Thread(target=run_task, args=(task, available_server))
                    t.start()
                    time.sleep(5)
        except Exception as e:
            task_logger.error(str(e))
        finally:
            end_time = time.time()
            # 确保至少间隔十秒，减少服务器负担
            duration = end_time - start_time
            if duration < 10:
                time.sleep(10 - duration)
>>>>>>> 36f4a7232af19c7211cd15be2b0125393802b21d

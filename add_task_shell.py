# -*- coding:utf-8 -*-

import django
#独立使用django的model
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpu_tasker.settings")
django.setup()
from gpu_info.models import GPUServer
from django.contrib.auth.models import User
from task.models import GPUTask

import sys
import time

import argparse

parser = argparse.ArgumentParser(description='add task.')
parser.add_argument('--task_name', type=str, default="test", help='task_name')
parser.add_argument('--task_workspace', type=str, default=".", help='task_workspace')
parser.add_argument('--task_cmds_file', type=str, default=".", help='task_cmds_file')
args = parser.parse_args()
#python add.py task_name task_workspace task_cmd_files

print(args)

with open( args.task_cmds_file, "r" ) as f:

    lines = f.readlines()
    task_name = lines[0].strip()
    task_workspace = lines[1].strip()

    
    for i, line in enumerate( lines[2:] ):
        time.sleep(5)
        print( i, task_name, task_workspace, line )
        task_instance = GPUTask()
        task_instance.name = f"{task_name}_{i}" 
        task_instance.workspace = task_workspace
        task_instance.memory_requirement = 3500
        task_instance.utilization_requirement = 0
        task_instance.cmd = line
        task_instance.user = User.objects.get(username='han')
        task_instance.status = 0
        # task_instance.assign_server = GPUServer.objects.get(hostname="datalab5.engr.tamu.edu")
        task_instance.save()

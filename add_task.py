# -*- coding:utf-8 -*-

import django
#独立使用django的model
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpu_tasker.settings")
django.setup()
from gpu_info.models import GPUServer
from django.contrib.auth.models import User# pwd = os.path.dirname(os.path.realpath(__file__))
from django.contrib.auth.models import User  # os.path.dirname() 获取当前脚本所在的文件夹名称
from django.contrib.auth.models import User  # os.path.realpath(__file__) 获取当前执行脚本的绝对路径。
from django.contrib.auth.models import User  # 获取当前文件的路径
from django.contrib.auth.models import User
from task.models import GPUTask


#找到项目文件
# sys.path.append(pwd+"../")




#添加数据开始


# class GPUTask(models.Model):
#     STATUS_CHOICE = (
#         (-2, '未就绪'),
#         (-1, '运行失败'),
#         (0, '准备就绪'),
#         (1, '运行中'),
#         (2, '已完成'),
#     )
#     name = models.CharField('任务名称', max_length=100)
#     user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE, related_name='tasks')
#     workspace = models.CharField('工作目录', max_length=200)
#     cmd = models.TextField('命令')
#     gpu_requirement = models.PositiveSmallIntegerField(
#         'GPU数量需求',
#         default=1,
#         validators=[MaxValueValidator(8), MinValueValidator(0)]
#     )
#     exclusive_gpu = models.BooleanField('独占显卡', default=False)
#     memory_requirement = models.PositiveSmallIntegerField('显存需求(MB)', default=0)
#     utilization_requirement = models.PositiveSmallIntegerField('利用率需求(%)', default=0)
#     assign_server = models.ForeignKey(GPUServer, verbose_name='指定服务器', on_delete=models.SET_NULL, blank=True, null=True)
#     priority = models.SmallIntegerField('优先级', default=0)
#     status = models.SmallIntegerField('状态', choices=STATUS_CHOICE, default=0)
#     create_at = models.DateTimeField('创建时间', auto_now_add=True)
#     update_at = models.DateTimeField('更新时间', auto_now=True)


cmds = ["source /data/han/miniconda3/bin/activate;conda activate torch171_geo163;python -u ef.py --dataset harris_sensitive_attribute_gender --dataset_path ../dataset/ --log_dir ../log/ --log_screen True --n_hidden 256 --num_epochs 400 --clf_pretrain_epochs 400 --adv_pretrain_epochs 140 --train_interval 100 --clf_lr 0.005 --adv_lr 0.01 --adv_lambda 80 --exp_name test",
    "source /data/han/miniconda3/bin/activate;conda activate torch171_geo163;python -u ef.py --dataset harris_sensitive_attribute_gender --dataset_path ../dataset/ --log_dir ../log/ --log_screen True --n_hidden 256 --num_epochs 400 --clf_pretrain_epochs 400 --adv_pretrain_epochs 140 --train_interval 100 --clf_lr 0.005 --adv_lr 0.01 --adv_lambda 80 --exp_name test" ]

for i, cmd in enumerate( cmds ):
    task_instance = GPUTask()
    task_instance.name = f"test8_{i}" 
    task_instance.workspace = "/home/grads/h/han/workspace/neighbor_fairness/src"
    task_instance.memory_requirement = 5000
    task_instance.utilization_requirement = 100
    task_instance.cmd = cmd
    task_instance.user = User.objects.get(username='han')
    task_instance.status = 0
    task_instance.assign_server = GPUServer.objects.get(hostname="datalab5.engr.tamu.edu")
    task_instance.save()

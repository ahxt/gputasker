import os
import signal
import random

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from gpu_info.models import GPUServer, GPUInfo
from django.contrib.auth.models import User


class GPUTask(models.Model):
    STATUS_CHOICE = (
        (-2, 'Not Ready'),
        (-1, 'Failed'),
        (0, 'Ready'),
        (1, 'Runing'),
        (2, 'Runned'),
    )
    name = models.CharField('task', max_length=100)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE, related_name='tasks')
    workspace = models.CharField('workspace', max_length=200)
    cmd = models.TextField('cmd')
    gpu_requirement = models.PositiveSmallIntegerField(
        'GPUs',
        default=1,
        validators=[MaxValueValidator(8), MinValueValidator(0)]
    )
    exclusive_gpu = models.BooleanField('exclusive', default=False)
    memory_requirement = models.PositiveSmallIntegerField('Mem(MB)', default=0)
    utilization_requirement = models.PositiveSmallIntegerField('rate(%)', default=0)
    assign_server = models.ForeignKey(GPUServer, verbose_name='assign_server', on_delete=models.SET_NULL, blank=True, null=True)
    priority = models.SmallIntegerField('priority', default=0)
    status = models.SmallIntegerField('status', choices=STATUS_CHOICE, default=0)
    create_at = models.DateTimeField('create_at', auto_now_add=True)
    update_at = models.DateTimeField('update_at', auto_now=True)
    traial = models.SmallIntegerField( "traial", default=0 )

    class Meta:
        verbose_name = 'GPU Task'
        verbose_name_plural = 'GPU Task'

    def __str__(self):
        return self.name

    def find_available_server(self):
        # TODO(Yuhao Wang): 优化算法，找最优server

        available_server = None
        if self.assign_server is None:
            available_gpu_list = []


            for server in GPUServer.objects.all():
                print( "server:", server )

                available_gpus = server.get_available_gpus(
                    self.gpu_requirement,
                    self.exclusive_gpu,
                    self.memory_requirement,
                    self.utilization_requirement
                )
                print("available_gpus:", available_gpus)

                if available_gpus:
                    available_gpu_list.extend( available_gpus )

            available_gpu_list = sorted(available_gpu_list, key=lambda x: (x[1], x[2], x[3]))

            print(available_gpu_list)

            if available_gpu_list is not None:
                available_gpu_list = available_gpu_list[:3]

                random.shuffle(available_gpu_list)

                available_server = {
                        'server': available_gpu_list[0][-1],
                        'gpus': [available_gpu_list[0][0]]
                    }
        
        else:
            available_gpus = self.assign_server.get_available_gpus(
                self.gpu_requirement,
                self.exclusive_gpu,
                self.memory_requirement,
                self.utilization_requirement
            )
            available_gpus = [ g[0] for g in available_gpus ]
            if available_gpus is not None:
                available_server = {
                    'server': self.assign_server,
                    'gpus': available_gpus[:self.gpu_requirement]
                }

        return available_server



class GPUTaskRunningLog(models.Model):
    STATUS_CHOICE = (
        (-1, 'Failed'),
        (1, 'Runing'),
        (2, 'Finished'),
    )
    index = models.PositiveSmallIntegerField('index')
    task = models.ForeignKey(GPUTask, verbose_name='task', on_delete=models.CASCADE, related_name='task_logs')
    server = models.ForeignKey(GPUServer, verbose_name='server', on_delete=models.SET_NULL, related_name='task_logs', null=True)
    pid = models.IntegerField('PID')
    gpus = models.CharField('GPU', max_length=20)
    log_file_path = models.FilePathField(path='running_log', match='.*\.log$', verbose_name="日志文件")
    status = models.SmallIntegerField('status', choices=STATUS_CHOICE, default=1)
    start_at = models.DateTimeField('start_at', auto_now_add=True)
    update_at = models.DateTimeField('update_at', auto_now=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'GPU Task Runing Log'
        verbose_name_plural = 'GPU Task Runing Log'

    def __str__(self):
        return self.task.name + '-' + str(self.index)

    def kill(self):
        os.kill(self.pid, signal.SIGKILL)
    
    def delete_log_file(self):
        if os.path.isfile(self.log_file_path):
            os.remove(self.log_file_path)

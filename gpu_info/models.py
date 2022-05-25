import json

from django.db import models


class GPUServer(models.Model):
    ip = models.CharField('IP地址', max_length=50)
    hostname = models.CharField('主机名', max_length=50, blank=True, null=True)
    port = models.PositiveIntegerField('端口', default=22)
    valid = models.BooleanField('是否可用', default=True)
    can_use = models.BooleanField('是否可调度', default=True)
    # TODO(Yuhao Wang): CPU使用率

    class Meta:
        ordering = ('ip',)
        verbose_name = 'GPU Servers'
        verbose_name_plural = 'GPU Servers'
        unique_together = (('ip', 'port'),)

    def __str__(self):
        return '{}:{:d}'.format(self.ip, self.port)


    def get_available_gpus(self, gpu_num, exclusive, memory, utilization):
        available_gpu_list = []
        
        if self.valid and self.can_use:

            for gpu in self.gpus.all():
                print("GPU:", gpu)
                # print(exclusive, memory, utilization)
                if gpu.check_available(exclusive, memory, utilization):

                    gpu_tuple = (gpu.index, int(gpu.memory_used/gpu.memory_total), int(gpu.memory_used_self/gpu.memory_total), gpu.memory_total, gpu.server)
                    # available_gpu_list.append(gpu.index)
                    # available_gpu_list.append(gpu.index)
                    available_gpu_list.append(gpu_tuple)
            
            if len(available_gpu_list) >= gpu_num:
                # available_gpu_list = sorted(available_gpu_list, key=lambda x: (x[1], x[2], x[3]))
                # available_gpu_list = [ gpu[0] for gpu in available_gpu_list]
                return available_gpu_list

            else:
                return None
        
        else:
            return None
    
    def set_gpus_busy(self, gpu_list):
        self.gpus.filter(index__in=gpu_list).update(use_by_self=True)

    def set_gpus_free(self, gpu_list):
        self.gpus.filter(index__in=gpu_list).update(use_by_self=False)




class GPUInfo(models.Model):
    uuid = models.CharField('UUID', max_length=40, primary_key=True)
    index = models.PositiveSmallIntegerField('序号')
    name = models.CharField('名称', max_length=40)
    utilization = models.PositiveSmallIntegerField('利用率')
    utilization_self = models.PositiveSmallIntegerField('自利用率', null=True)
    # utilization_self = models.FloatField('自利用率')
    memory_total = models.PositiveIntegerField('总显存')
    memory_used = models.PositiveIntegerField('已用显存')
    memory_used_self = models.PositiveIntegerField('自用显存')
    processes = models.TextField('进程')
    server = models.ForeignKey(GPUServer, verbose_name='服务器', on_delete=models.CASCADE, related_name='gpus')
    use_by_self = models.BooleanField('是否被gputasker进程占用', default=False)
    complete_free = models.BooleanField('完全空闲', default=False)
    can_use = models.BooleanField('是否可调度', default=True)
    update_at = models.DateTimeField('更新时间', auto_now=True)



    class Meta:
        ordering = ('server', 'index',)
        verbose_name = 'GPU Info'
        verbose_name_plural = 'GPU Info'

    def __str__(self):
        return self.name + '[' + str(self.index) + '-' + self.server.ip + ']'
    
    @property
    def memory_available(self):
        return self.memory_total - self.memory_used

    @property
    def utilization_available(self):
        return 100 - self.utilization


    def check_available(self, exclusive, memory, utilization):
        # if exclusive:
        #     return not self.use_by_self and self.complete_free
        # else:
        #     return not self.use_by_self and self.memory_available > memory and self.utilization_available > utilization
        if self.can_use == False:
            return False
        if exclusive:
            return self.complete_free
        else:
            return self.memory_available > memory


    def usernames(self):
        r"""
        convert processes string to usernames string array.
        :return: string array of usernames.
        """
        if self.processes != '':
            arr = self.processes.split('\n')
            # only show first two usernames
            username_arr = [json.loads(item)['username'] for item in arr[:2]]
            res = ', '.join(username_arr)
            # others use ... to note
            if len(arr) > 2:
                res = res + ', ...'
            return res
        else:
            return '-'

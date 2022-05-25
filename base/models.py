from django.db import models
from django.contrib.auth.models import User


class UserConfig(models.Model):
    user = models.OneToOneField(User, verbose_name='用户', on_delete=models.CASCADE, related_name='config', primary_key=True)
    server_username = models.CharField('服务器用户名', max_length=100)
    server_private_key = models.TextField('私钥')
    server_private_key_path = models.FilePathField(path='private_key', verbose_name="私钥文件", blank=True, null=True)

    class Meta:
<<<<<<< HEAD
        verbose_name = 'User Setting'
        verbose_name_plural = 'User Setting'


class SystemConfig(models.Model):
    user = models.OneToOneField(User, verbose_name='系统管理员', on_delete=models.CASCADE, related_name='system_config', primary_key=True)
    gpustat_path = models.CharField('gpustat路径', max_length=100)

    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Setting'
=======
        verbose_name = '用户设置'
        verbose_name_plural = '用户设置'
>>>>>>> 36f4a7232af19c7211cd15be2b0125393802b21d

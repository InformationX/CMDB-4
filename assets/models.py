'''
@Author: your name
@Date: 2020-03-11 05:13:56
@LastEditTime: 2020-03-11 21:30:42
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /CMDB/assets/models.py
'''
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 资产共有数据模型
class Assets(models.Model):
    ''' 所有资产的共有数据表 '''
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('softwore', '软件资产'),
    )
    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    asset_type = models.CharField(choice=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='资产类型')
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产序列号')
    business_unit = models.ForeignKey('BusinessUnit', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属业务线')
    status = models.SmallIntegerField(choice=asset_status, default=0, verbose_name='设备状态')
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='制造商', on_delete=models.SET_NULL)
    manager_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    tags = models.ManyToManyField('Tag', blank=True, verbos_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员', related_name='admin', on_delete= models.SET_NULL)
    idc = models.ForeiKey('IDC', null=True, blank=True, verbose_name='所在机房', on_delete=models.SET_NULL)
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='合同', on_delete=models.SET_NULL)
    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    price = models.FloatField(null=True, blank=True, verbose_name='价格')
    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='批准人', related_name='approved_by', on_delete=models.SET_NULL)
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_noe=True, verbose_name='更新日期')

    def __str__(self):
        return '<%s> %s' % (self.get_asset_type_display(), self.name)
    
    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
        ordering = ['-c_time']

# 服务器模型
class Server(models.Model):
    '''服务器设备'''
    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )
    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choice=sub_asset_type_choice, default=0, verbose_name='服务器类型')
    created_by = models.CharField(choice=created_by_choice, max_length=32, default='auto', verbose_name='添加方式')
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True, verbose_name='宿主机', on_delete=models.CASCADE)
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')
    os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'

# 安全设备
class SecurityDevice(models.Model):
    '''安全设备'''
    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'), 
        (4, '运维审计系统'), 
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choice=sub_asset_type_choice, default=0, verbose_name='安全设备')
    model = models.CharField(max_length=128, default='未知型号', verbose_name='安全设备型号')

    def __str__(self):
        return self.asset.name + '---' + self.get_sub_asset_type_display() + str(self.model) + 'id:%s' % self.id
    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = '安全设备'


class StorageDevice(models.Model):
    '''存储设备'''
    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'), 
        (2, '磁带库'), 
        (4, '磁带机'),
    )
    
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choice=sub_asset_type_choice, default=0, verbose_name='存储设备类型')
    model = models.CharField(max_length=128, default='未知设备', verbose_name='存储设备型号')
    
    def __str__(self):
        return self.asset.name + '---' + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = '存储设备'


class NetworkDevice(models.Model):
    '''网络设备'''
    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备')
    )
    
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choice=sub_asset_type_choice, default=0, verbose_name='网络设备类型')
    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='VLanIP')
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')
    model = models.CharField(verbose_name='网络设备型号', max_length=128, default='未知型号')
    firmware = models.CharField(verbose_name='设备固件版本', max_length=128, blank=True, null=True)
    port_num = models.SmallIntegerField(verbose_name='端口个数', null=True, blank=True)
    device_detail = models.TextField(null=True, blank=True, verbose_name='详细配置')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)
    
    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'


class Software(models.Model):
    '''只保存付费购买的软件'''
    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公/开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choice=sub_asset_type_choice, default=0, verbose_name='软件类型')
    license_num = models.IntegerField(default=1, verbose_name='授权数量')
    version = models.CharField(unique=True,help_text='例如:RedHat release 7 (Final)', max_lenglh=64, verbose_name='软件/系统版本')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)
    
    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = '软件/系统'

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime

from django.db import models


class TblAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.CharField(unique=True, max_length=255, verbose_name='用户邀请码')
    pid = models.BigIntegerField()
    role = models.IntegerField()
    status = models.IntegerField()
    phone = models.CharField(max_length=20, verbose_name='手机号')
    nickname = models.CharField(max_length=255, verbose_name='昵称')
    avatar = models.CharField(max_length=255, verbose_name='头像')
    bsn_address = models.CharField(max_length=255, verbose_name='bsn地址')
    name = models.CharField(max_length=255, verbose_name='真实姓名')
    amount = models.BigIntegerField(verbose_name='余额')
    id_card_num = models.CharField(max_length=255)
    id_card_positive_image_url = models.CharField(max_length=255)
    id_card_negative_image_url = models.CharField(max_length=255)
    authentication = models.BooleanField(default=False, verbose_name='是否认证')
    create_time = models.BigIntegerField()
    update_time = models.BigIntegerField()
    del_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_account'
        verbose_name = verbose_name_plural = '用户'


class TblAccountBank(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    name = models.CharField(max_length=255)
    bank_id = models.ForeignKey('TblBank', models.DO_NOTHING, db_column='bank_id')
    bank_name = models.CharField(max_length=255)
    bank_num = models.CharField(max_length=255)
    status = models.IntegerField()
    create_time = models.IntegerField()
    update_time = models.IntegerField()
    del_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_account_bank'


class TblAccountIncome(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    type = models.IntegerField()
    amount = models.BigIntegerField()
    remark = models.CharField(max_length=255)
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_account_income'


class TblBank(models.Model):
    name = models.CharField(max_length=255, verbose_name='银行名称')

    class Meta:
        managed = False
        db_table = 'tbl_bank'
        verbose_name = verbose_name_plural = '银行'


class TblBanner(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(default='', verbose_name='图片')
    name = models.CharField(max_length=255, default='', verbose_name='名称')
    index = models.IntegerField(default=0, verbose_name='排序')
    product_id = models.ForeignKey('TblProductSellHistory', models.DO_NOTHING, db_column='product_id',
                                   verbose_name='作品')
    link = models.CharField(max_length=255, default='', verbose_name='外链', help_text='外链', blank=True)
    create_time = models.BigIntegerField(default=lambda: int(datetime.datetime.now().timestamp()))
    update_time = models.BigIntegerField(default=0)
    del_time = models.BigIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'tbl_banner'
        verbose_name = verbose_name_plural = '轮播图'


class TblProduct(models.Model):
    CHOICES = (
        (0, '上架'),
        (1, '下架'),
    )
    id = models.BigAutoField(primary_key=True)
    author_id = models.ForeignKey('TblAccount', on_delete=models.DO_NOTHING, verbose_name='用户id',
                                  db_column='author_id')
    classify = models.BigIntegerField(default=0, blank=True)
    name = models.CharField(max_length=255, verbose_name='作品名称')
    description = models.TextField(verbose_name='描述')
    image = models.ImageField(max_length=255, verbose_name='作品图片')
    price = models.IntegerField(verbose_name='作品价格')
    status = models.BooleanField(verbose_name='是否支付')
    stock = models.BigIntegerField(verbose_name='库存')
    index = models.IntegerField(verbose_name='排序')
    create_time = models.IntegerField(blank=True)
    update_time = models.IntegerField(blank=True)
    del_time = models.SmallIntegerField(default=0, verbose_name='是否上架', choices=CHOICES)

    class Meta:
        managed = False
        db_table = 'tbl_product'
        verbose_name = verbose_name_plural = '作品'

    def __str__(self):
        return self.name


class TblProductClassify(models.Model):
    name = models.CharField(max_length=255)
    create_time = models.IntegerField()
    update_time = models.IntegerField()
    del_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_product_classify'


class TblProductLikes(models.Model):
    id = models.BigAutoField(primary_key=True)
    pid = models.BigIntegerField()
    uid = models.BigIntegerField()
    create_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_product_likes'


class TblProductOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    oid = models.CharField(max_length=255)
    pay_type = models.CharField(max_length=255)
    uid = models.BigIntegerField()
    pid = models.BigIntegerField()
    status = models.IntegerField()
    create_time = models.IntegerField()
    pay_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_product_order'


class TblProductSellHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    pid = models.ForeignKey('TblProduct', on_delete=models.DO_NOTHING, db_column='pid')
    uid = models.ForeignKey('TblAccount', on_delete=models.DO_NOTHING, db_column='uid')
    times = models.IntegerField()
    tx_id = models.CharField(max_length=255)
    token_id = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    cid = models.CharField(max_length=255)
    status = models.BooleanField(verbose_name='是否上链')
    display = models.BooleanField(verbose_name='是否展示')
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_user_product'
        verbose_name = verbose_name_plural = '用户作品'

    def __str__(self):
        return f'#{self.times}-{self.pid.name}'


class TblRecommend(models.Model):
    STATUS_CHOICES = (
        (0, '启用'),
        (1, '禁用'),
    )
    id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey('TblProductSellHistory', models.DO_NOTHING, db_column='product_id',
                                   verbose_name='作品')
    index = models.IntegerField(verbose_name='排序')
    status = models.IntegerField(default=0, choices=STATUS_CHOICES, verbose_name='状态')

    class Meta:
        managed = False
        db_table = 'tbl_recommend'
        verbose_name = verbose_name_plural = '推荐'


class TblWalletRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    amount = models.BigIntegerField()
    kind = models.IntegerField()
    source_id = models.BigIntegerField()
    source_type = models.IntegerField()
    remark = models.CharField(max_length=255)
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_wallet_record'


class TblWithdraw(models.Model):
    STATUS_CHOICES = (
        (0, '申请中'),
        (1, '已打款'),
    )
    id = models.BigAutoField(primary_key=True)
    uid = models.ForeignKey('TblAccount', models.DO_NOTHING, db_column='uid', verbose_name='用户')
    bank_id = models.ForeignKey('TblAccountBank', models.DO_NOTHING, db_column='bank_id', verbose_name='银行卡')
    amount = models.BigIntegerField(verbose_name='金额')
    status = models.IntegerField(default=0, choices=STATUS_CHOICES, verbose_name='状态')
    create_time = models.IntegerField()
    withdraw_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_withdraw'
        verbose_name = verbose_name_plural = '提现记录'


class TblPayType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True, verbose_name='是否启用')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'tbl_pay_type'
        verbose_name = verbose_name_plural = '支付渠道'


class TblProductSellHistoryAirDrop(models.Model):
    id = models.BigAutoField(primary_key=True)
    pid = models.ForeignKey('TblProduct', on_delete=models.DO_NOTHING, db_column='pid')
    uid = models.ForeignKey('TblAccount', on_delete=models.DO_NOTHING, db_column='uid')
    times = models.IntegerField()
    tx_id = models.CharField(max_length=255)
    token_id = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    cid = models.CharField(max_length=255)
    status = models.BooleanField(verbose_name='是否上链')
    display = models.BooleanField(verbose_name='是否展示')
    is_air_drop = models.BooleanField()
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_user_product'
        verbose_name = verbose_name_plural = '空投'

    def __str__(self):
        return f'#{self.times}-{self.pid.name}'


class TblAirDropRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    pid = models.ForeignKey('TblProduct', on_delete=models.DO_NOTHING, db_column='pid')
    uid = models.ForeignKey('TblAccount', on_delete=models.DO_NOTHING, db_column='uid')
    times = models.IntegerField()
    tx_id = models.CharField(max_length=255)
    token_id = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    cid = models.CharField(max_length=255)
    status = models.BooleanField(verbose_name='是否上链')
    display = models.BooleanField(verbose_name='是否展示')
    is_air_drop = models.BooleanField(verbose_name='是否为空投')
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_user_product'
        verbose_name = verbose_name_plural = '空投记录'

    def __str__(self):
        return f'#{self.times}-{self.pid.name}'

import datetime
import time

from django.contrib import admin

from django.utils.safestring import mark_safe

from . import models


# Register your models here.

@admin.register(models.TblAccount)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'nickname', 'img', 'phone', 'bsn_address', 'amount', 'authentication',)

    list_editable = ('authentication',)

    def img(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.avatar))

    img.allow_tags = True
    img.short_description = '头像'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.TblBank)
class TblBankModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.TblBanner)
class TblBannerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index', 'product_name', 'product_img')

    def product_name(self, row):
        return row.product_id.name

    def product_img(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.product_id.image))


@admin.register(models.TblRecommend)
class TblRecommendModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'index', 'product_name', 'product_img')

    def product_name(self, row):
        return row.product_id.name

    def product_img(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.product_id.image))


@admin.register(models.TblWithdraw)
class TblWithdrawModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bank_name', 'bank_num', 'phone', 'amount', 'status', 'apply_time', "pay_time")

    list_filter = ('status',)

    list_editable = ('status',)

    list_display_links = None

    def name(self, row):
        return row.bank_id.name

    name.short_description = '姓名'

    def bank_name(self, row):
        return row.bank_id.bank_id.name + '-' + row.bank_id.bank_name

    bank_name.short_description = '银行名称'

    def phone(self, row):
        return row.uid.phone

    phone.short_description = '手机号'

    def apply_time(self, row):
        return datetime.datetime.fromtimestamp(row.create_time).strftime('%Y-%m-%d %H:%M:%S')

    apply_time.short_description = '申请时间'

    def pay_time(self, row):
        if row.withdraw_time == 0:
            return ""
        return datetime.datetime.fromtimestamp(row.withdraw_time).strftime('%Y-%m-%d %H:%M:%S')

    pay_time.short_description = '提现时间'

    def save_model(self, request, obj, form, change):
        result = super(TblWithdrawModelAdmin, self).save_model(request, obj, form, change)
        if obj.status == 1:
            obj.withdraw_time = int(time.time())
        else:
            obj.withdraw_time = 0
        obj.save()
        return result

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def bank_num(self, row):
        return row.bank_id.bank_num

    bank_num.short_description = '银行卡号'


@admin.register(models.TblProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'img', 'price', 'index', 'stock', 'status', 'del_time')
    list_editable = ('del_time',)
    list_filter = ('name', 'status')
    search_fields = ('name',)
    ordering = ('-id', '-index', 'price')

    def img(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.image))

    img.short_description = '图片'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = '民生数藏管理'
admin.site.site_title = '民生数藏管理'
admin.site.index_title = '民生数藏管理'


@admin.register(models.TblPayType)
class PayTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_editable = ('status',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

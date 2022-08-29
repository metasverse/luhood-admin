import datetime
import time
import uuid

from django.conf import settings

from django.contrib import admin, messages
from django.http import JsonResponse, HttpResponseRedirect

from django.utils.safestring import mark_safe

from simpleui.admin import AjaxAdmin

from . import models
from . import forms
import requests
from .storage import OssStorage


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
        return row.product_id.pid.name

    product_name.short_description = '作品名称'

    def product_img(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.product_id.pid.image))

    product_img.short_description = '作品图片'


@admin.register(models.TblRecommend)
class TblRecommendModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'index', 'product_name', 'product_img')

    def product_name(self, row):
        return row.product_id.pid.name

    product_name.short_description = '作品名称'

    def product_img(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.product_id.pid.image))

    product_img.short_description = '作品图片'


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


# @admin.register(models.TblProduct)
# class ProductAdmin(AjaxAdmin, admin.ModelAdmin):
#     list_display = ('id', 'name', 'img', 'price', 'index', 'stock', 'status', 'del_time')
#     list_editable = ('del_time',)
#     list_filter = ('name', 'status')
#     search_fields = ('name',)
#     ordering = ('-id', '-index', 'price')
#
#     readonly_fields = ('classify', 'create_time', 'update_time')
#
#     actions = ['air_drop']
#
#     def img(self, row):
#         return mark_safe("<img src='{url}' width='40px'/>".format(url=row.image))
#
#     img.short_description = '图片'
#
#     def air_drop(self, request, queryset):
#         if not queryset:
#             return JsonResponse({})
#         if queryset.count() > 1:
#             return JsonResponse({'status': 'error', 'msg': '请只选择一个作品'})
#         # 校验手机号码
#         phones = request.POST.get('phones', '')
#         phones = phones.split('\r\n')
#         if len(phones) == 0:
#             return JsonResponse({'status': 'error', 'msg': '请输入手机号码'})
#         for phone in phones:
#             if not models.TblAccount.objects.filter(phone=phone).exists():
#                 return JsonResponse({'status': 'error', 'msg': f'手机号码为{phone}的用户不存在'})
#         # 请求空投接口
#         obj = queryset.first()
#         print(obj)
#         data = {
#             'pid': obj.id,
#             'phones': phones
#         }
#         resp = requests.post(settings.SERVER_DOMAIN + "/api/v1/product/airdrop", json=data)
#         print(resp.text)
#         return JsonResponse({'status': 'success', 'msg': resp.json()['data']})
#
#     air_drop.short_description = "空投"
#     air_drop.type = 'danger'
#     air_drop.layer = {
#         'params': [
#             {
#                 'type': 'textarea',
#                 'key': 'phones',
#                 'label': '手机号码',
#             }
#         ],
#         'title': '空投手机号码',
#         'tips': '多个手机号码以换行隔开'
#     }
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def save_model(self, request, obj, form, change):
#         obj.create_time = int(time.time())
#         obj.update_time = 0
#
#         super(ProductAdmin, self).save_model(request, obj, form, change)
#         import requests
#         data = {
#             "name": obj.name,
#             'price': obj.price,
#             'image': obj.image.url,
#             'uid': obj.author_id,
#             'count': obj.stock,
#             'description': obj.description,
#             'password': 'PublicProductRequest'
#         }
#         obj.delete()
#         resp = requests.post(settings.SERVER_DOMAIN + "/api/v1/product/create/public", json=data)
#         print(resp.json())
#         if resp.json().get('success'):
#             messages.add_message(request, messages.SUCCESS, "创建成功")
#         else:
#             messages.add_message(request, messages.ERROR, "创建失败")


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


@admin.register(models.TblProductSellHistory)
class TblProductSellHistory(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'price', 'status', 'display', 'author_name', 'owner_name']

    list_editable = ['display']

    def name(self, row):
        return row.pid.name

    name.short_description = '作品名称'

    def image(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.pid.image))

    image.short_description = '图片'

    def price(self, row):
        return f'{row.pid.price / 100}元'

    price.short_description = '价格'

    def author_name(self, row):
        return row.pid.author_id.nickname

    author_name.short_description = '作者'

    def owner_name(self, row):
        return row.uid.nickname

    owner_name.short_description = '拥有者'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(models.TblProductSellHistoryAirDrop)
class TblProductSellHistoryAirDrop(AjaxAdmin):
    list_display = ['id', 'name', 'image', 'price', 'status', 'display', 'author_name', 'owner_name']

    def get_queryset(self, request):
        return super(TblProductSellHistoryAirDrop, self).get_queryset(request).filter(is_air_drop=False)

    def name(self, row):
        return row.pid.name

    name.short_description = '作品名称'

    def image(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.pid.image))

    image.short_description = '图片'

    def price(self, row):
        return f'{row.pid.price / 100}元'

    price.short_description = '价格'

    def author_name(self, row):
        return row.pid.author_id.nickname

    author_name.short_description = '作者'

    def owner_name(self, row):
        return row.uid.nickname

    owner_name.short_description = '拥有者'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def air_drop(self, request, queryset):
        if not queryset:
            return JsonResponse({})
        if queryset.count() > 1:
            return JsonResponse({'status': 'error', 'msg': '请只选择一个作品'})
        # 校验手机号码
        phones = request.POST.get('phones', '')
        phones = phones.split('\r\n')
        if len(phones) == 0:
            return JsonResponse({'status': 'error', 'msg': '请输入手机号码'})
        for phone in phones:
            if not models.TblAccount.objects.filter(phone=phone).exists():
                return JsonResponse({'status': 'error', 'msg': f'手机号码为{phone}的用户不存在'})
        # 请求空投接口
        obj = queryset.first()
        print(obj)
        data = {
            'pid': obj.id,
            'phones': phones
        }
        resp = requests.post(settings.SERVER_DOMAIN + "/api/v1/product/airdrop", json=data)
        print(resp.text)
        return JsonResponse({'status': 'success', 'msg': resp.json()['data']})

    actions = ['air_drop']

    form = forms.ProductAddForm

    air_drop.short_description = "空投"
    air_drop.type = 'danger'
    air_drop.layer = {
        'params': [
            {
                'type': 'textarea',
                'key': 'phones',
                'label': '手机号码',
            }
        ],
        'title': '空投手机号码',
        'tips': '多个手机号码以换行隔开'
    }

    def save_form(self, request, form, change):
        if change:
            obj = form.cleaned_data.get('id')
            obj.display = form.cleaned_data.get('display')
            obj.save()
            return
        image = form.cleaned_data.get('image')
        author = models.TblAccount.objects.get(phone=form.cleaned_data.get('phone'))
        path = OssStorage().save(uuid.uuid4().__str__() + image.name.split('.')[-1], image)
        data = {
            "name": form.cleaned_data.get('name'),
            'price': 100,
            'image': path,
            'uid': author.id,
            'count': form.cleaned_data.get('stock'),
            'description': form.cleaned_data.get('desc'),
            'password': 'PublicProductRequest'
        }
        resp = requests.post(settings.SERVER_DOMAIN + "/api/v1/product/create/public", json=data)
        print(resp.json())
        if resp.json().get('success'):
            messages.add_message(request, messages.SUCCESS, "创建成功")
        else:
            messages.add_message(request, messages.ERROR, "创建失败")

    def save_model(self, request, obj, form, change):
        pass

    def save_related(self, request, form, formsets, change):
        pass

    def log_addition(self, request, obj, message):
        pass

    def log_change(self, request, obj, message):
        pass

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect("/admin/#/admin/app/tblproductsellhistory/")


@admin.register(models.TblAirDropRecord)
class TblAirDropRecordModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'price', 'status', 'display', 'author_name', 'owner_name']

    def name(self, row):
        return row.pid.name

    name.short_description = '作品名称'

    def image(self, row):
        return mark_safe("<img src='{url}' width='40px'/>".format(url=row.pid.image))

    image.short_description = '图片'

    def price(self, row):
        return f'{row.pid.price / 100}元'

    price.short_description = '价格'

    def author_name(self, row):
        return row.pid.author_id.nickname

    author_name.short_description = '作者'

    def owner_name(self, row):
        return row.uid.nickname

    owner_name.short_description = '拥有者'

    def get_queryset(self, request):
        return super(TblAirDropRecordModelAdmin, self).get_queryset(request).filter(is_air_drop=True)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

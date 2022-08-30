from django import forms
from . import models


class ProductAddForm(forms.ModelForm):
    phone = forms.CharField(max_length=255, help_text='站内用户手机号码', label='手机号码')
    name = forms.CharField(max_length=255, label='作品名称')
    desc = forms.CharField(max_length=255, label='作品描述')
    # price = forms.IntegerField(min_value=1, label='作品价格')
    stock = forms.IntegerField(min_value=1, label='空投份数')
    image = forms.ImageField(label='作品图片')

    class Meta:
        model = models.TblProductSellHistory
        exclude = (
            'pid', 'uid', 'times', 'tx_id', 'token_id', 'hash', 'cid', 'status', 'display', 'create_time',
            'is_air_drop')

    def clean(self):
        super(ProductAddForm, self).clean()
        phone = self.cleaned_data.get('phone')
        if not models.TblAccount.objects.filter(phone=phone).exists():
            raise forms.ValidationError('手机号码不存在')
        return self.cleaned_data

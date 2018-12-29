# admin.py
from datetime import timedelta

from django import forms
from django.contrib import admin

from widget.models import Test


class SplitDurationWidget(forms.MultiWidget):
    """
    A Widget that splits duration input into four number input boxes.
    """
    class Media:
        js = ('splitwidget.js',)

    def __init__(self, attrs=None):
        day_attrs = {'placeholder': '# of Days', 'data-toggle':'tooltip', 'title':"Input the number of Days"}
        hour_attrs = {'placeholder': '# of Hours', 'data-toggle':'tooltip', 'title':"Input the number of Hours"}
        minute_attrs = {'placeholder': '# of Minutes', 'data-toggle':'tooltip', 'title':"Input the number of Minutes"}
        second_attrs = {'placeholder': '# of Seconds', 'data-toggle':'tooltip', 'title':"Input the number of Seconds"}

        if attrs:
            day_attrs.update(attrs)
            hour_attrs.update(attrs)
            minute_attrs.update(attrs)
            second_attrs.update(attrs)

        widgets = (
            forms.NumberInput(day_attrs),
            forms.NumberInput(hour_attrs),
            forms.NumberInput(minute_attrs),
            forms.NumberInput(second_attrs)
        )

        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = value
            if d:
                hours = d.seconds // 3600
                minutes = (d.seconds % 3600) // 60
                seconds = d.seconds % 60
                return [int(d.days), int(hours), int(minutes), int(seconds)]
        return [None, None, None, None]


class MultiValueDurationField(forms.MultiValueField):
    widget = SplitDurationWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
            forms.IntegerField(),
            forms.IntegerField(),
        )
        super(MultiValueDurationField, self).__init__(
            fields=fields,
            require_all_fields=True, *args, **kwargs)

    def compress(self, data_list):
        if len(data_list) == 4:
            return timedelta(
                days=int(data_list[0]),
                hours=int(data_list[1]),
                minutes=int(data_list[2]),
                seconds=int(data_list[3]))
        else:
            return timedelta(0)


class TestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['lead_time'] = MultiValueDurationField()

    class Meta:
        model = Test
        fields = '__all__'


class TestAdmin(admin.ModelAdmin):
    form = TestForm


admin.site.register(Test, TestAdmin)
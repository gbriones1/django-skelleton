import json
import sys

from itertools import chain

from django import forms
from django.core.cache import cache
from django.utils.encoding import (
    force_str, force_text,
)
from django.utils.html import conditional_escape, format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.core import serializers

class Datalist(forms.widgets.Select):
    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if value is None:
            value = ''
        datalist_attrs = attrs
        final_attrs = self.build_attrs(attrs)
        final_attrs["name"] = name
        final_attrs["list"] = final_attrs.pop("id")
        if value != '':
            if name == "brand":
                final_attrs["value"] = Brand.objects.get(id=value).name
            elif name == "provider":
                final_attrs["value"] = Provider.objects.get(id=value).name
        output = [format_html('<input{} />', flatatt(final_attrs)), format_html('<datalist{}>', flatatt(datalist_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</datalist>')
        return mark_safe('\n'.join(output))

    def render_options(self, choices, selected_choices):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        if option_value == "":
            option_label = ""
        option_value = force_text(option_value)
        # return format_html('<option value="{}"></option>',
        #                    force_text(option_label))
        return '<option value="{}"></option>'.format(option_label.encode('utf-8').decode())


class FormSet(forms.widgets.Select):

    def __init__(self, search=False, allow_create=True, include=[], form=[]):
        super(forms.widgets.Select, self).__init__()
        self.search = search
        self.allow_create = allow_create
        self.include = include
        self.form = form

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        model_name = self.choices.queryset.model.__name__
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        final_attrs["name"] = name
        final_attrs["type"] = 'hidden'
        final_attrs["class"] = 'formset'
        final_attrs["data-model"] = model_name
        output = []
        table_attrs = {"class": "table", "class":"table formSet-table"}
        if self.allow_create:
            table_attrs['data-allow_create'] = 'true'
        output.append(format_html('<div{}>', flatatt({"class": "row formSet-container"})))
        output.append(format_html('<div{}>', flatatt({"class": "col-sm-12", "style":"height: 300px;overflow-y: auto;padding: 0"})))
        output.append(format_html('<table{} >', flatatt(table_attrs)))
        output.append('<thead><tr>')
        form_fields = []
        for field in self.form:
            form_fields.append((field.id_for_label, field.label, str(field)))
            output.append(format_html('<th{}>'+field.label+'</th>', flatatt({"data-field":field.html_name})))
        output.append('<th></th>')
        if self.allow_create:
            output.append('<th>')
            output.append(format_html('<button{}><i class="fa fa-plus"></i></button>', flatatt({"class":"btn btn-primary btn-sm formSet-create", "type":"button"})))
            output.append('</th>')
        output.append('</tr></thead>')
        output.append('<tbody></tbody>')
        output.append('</table>')
        output.append('</div>')

        if self.search:
            output.append(format_html('<div{}>', flatatt({"class": "row"})))
            output.append(format_html('<div{}>', flatatt({"class": "col-sm-6"})))
            output.append(format_html('<td><input{} /></td>', flatatt({"placeholder":"Search", "class":"formSet-search"})))
            output.append('</div>')
            output.append('</div>')

        final_attrs["data-fields"] = json.dumps(form_fields)
        output.append(format_html('<input{} />', flatatt(final_attrs)))
        output.append('</div>')

        return mark_safe('\n'.join(output))

class HiddenField(forms.Field):
    widget = forms.widgets.HiddenInput

    def __init__(self, *args, **kwargs):
        super(HiddenField, self).__init__(label='', *args, **kwargs)

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class HiddenJSONField(HiddenField):

    def __init__(self, serializer):
        initial = ""
        try:
            initial = json.dumps(serializer(serializer.Meta.model.objects.all(), many=True).data)
        except:
            pass
        super(HiddenField, self).__init__(initial=initial)

class ColumnCheckboxWidget(forms.widgets.CheckboxSelectMultiple):
    template_name = 'sections/multiple_input_cols.html'

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["col_size"] = int(12/len(context['widget']['optgroups']))
        for _, options, _ in context['widget']['optgroups']:
            for option in options:
                option["name"] = "{}_{}".format(option["name"], option["value"])
                option["value"] = True
        return context


class MultiSetWidget(forms.widgets.Select):
    template_name = 'sections/multiset_widget.html'

    def __init__(self, search=True, amounts=False, editable_fields=[], extra_fields={}):
        super(forms.widgets.Select, self).__init__()
        self.search = search
        self.amounts = amounts
        self.editable_fields = editable_fields
        self.extra_fields = extra_fields
        self.attrs["class"] = "multiset form-control"

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["widget"]["type"] = "hidden"
        context["search"] = self.search

        editable = {}
        for field in self.editable_fields:
            widget = self.choices.queryset.model._meta.get_field(field).formfield().widget
            if hasattr(widget, 'input_type'):
                editable[field] = {
                    'tag': 'input',
                    'type': widget.input_type,
                }
            elif hasattr(widget, 'choices'):
                editable[field] = {
                    'tag': 'select',
                    'choices': widget.choices,
                }
        for field in self.extra_fields.keys():
            editable[field] = self.extra_fields[field]
        context["editable"] = json.dumps(editable)
        
        if self.amounts:
            context["multiple"] = "true"
        return context
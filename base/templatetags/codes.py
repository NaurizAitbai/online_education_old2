import re
from django import template
from django.template.loader import render_to_string

from base.models import Code

register = template.Library()

@register.filter(name='convert_codes')
def convert_codes(lesson_text):
    codes_list = re.findall(r'{% code "(.*?)" %}', lesson_text)

    for code_name in codes_list:
        code = Code.objects.get(name=code_name)
        context = {
            'code': code
        }
        tag_code = '{{% code "{}" %}}'.format(code.name)
        rendered_template = render_to_string('widgets/code_editor.html', context=context)
        lesson_text = lesson_text.replace(tag_code, rendered_template)
    
    return lesson_text
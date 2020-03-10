import re
from django import template

from base.models import Code

register = template.Library()

@register.filter(name='convert_codes')
def convert_codes(lesson_text):
    codes_list = re.findall(r'{% code "(.*?)" %}', lesson_text)

    for code_name in codes_list:
        code = Code.objects.get(name=code_name)
        lesson_text = lesson_text.replace('{{% code "{}" %}}'.format(code.name), """
<textarea id="editor_{}" class="code-editor">{}</textarea>
""".format(code.name, code.code))
    
    return lesson_text
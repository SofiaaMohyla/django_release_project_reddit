from django.template.defaultfilters import register as defaultfilter_register
from django.template.defaulttags import register as defaulttags_register
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })

    # Добавление всех фильтров из Django в Jinja2
    for filter_name, filter_func in defaultfilter_register.filters.items():
        env.filters[filter_name] = filter_func

    # Добавление всех тегов из Django в Jinja2
    for tag_name, tag_func in defaulttags_register.tags.items():
        env.globals[tag_name] = tag_func

    return env

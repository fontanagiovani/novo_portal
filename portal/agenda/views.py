# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from portal.agenda.models import Agenda
from django.core.urlresolvers import reverse
from datetime import date, datetime, timedelta # para trabalhar com datas e horarios
from django.db.models import Q # para trabalhar com condicao ou na queryset

from portal.core.decorators import contar_acesso
# Create your views here.

# http://programando-ads.blogspot.com.br/2014/12/manipular-semanas-com-python.html
# https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#date
# https://docs.djangoproject.com/en/dev/ref/models/querysets/#range
# https://stackoverflow.com/questions/30782060/how-to-loop-over-datetime-range-in-django-templates
# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
# https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects #q object
# https://stackoverflow.com/questions/39441639/getting-the-date-of-the-first-day-of-the-week # corrigir erro ao identificar primeiro dia da semana

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

@contar_acesso
def compromissos(request, dia=0, mes=0, ano=0):
    try:
        today = date(int(ano), int(mes), int(dia))
    except ValueError:
        #raise ValueError("data no formato incorreto")
        today = datetime.now()

    first_day = today - timedelta(days=today.isoweekday() %7)
    last_day = first_day + timedelta(days=6)
    agenda = Agenda.objects.filter(Q(inicio__range=(first_day, last_day)) | Q(fim__range=(first_day, last_day))).order_by('inicio', 'fim')

#    import calendar
#    print "calendário!!!"
#    print (calendar.monthcalendar(2017,8))

    return render(request, 'agenda/lista_compromissos.html', {'agenda': agenda, 'today': today, 'first_day': first_day, 'last_day': last_day, 'daterange': daterange(first_day, last_day)})

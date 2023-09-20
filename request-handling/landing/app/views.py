from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()

def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    landing_used = request.GET.get('from-landing', '')
    if landing_used == 'test':
        counter_click.update('t')
        return render(request, 'index.html')
    elif landing_used == 'original':
        counter_click.update('o')
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')



def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    template_requested = request.GET.get('ab-test-arg', '')
    if template_requested == 'test':
        sutable_template = 'landing_alternate.html'
        counter_show.update('t')
        return render(request, sutable_template)
    elif template_requested == 'original':
        sutable_template = 'landing.html'
        counter_show.update('o')
        return render(request, sutable_template)
    else:
        return render(request, 'index.html')



def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    if counter_click['o'] != 0:
        original_conversion = round(counter_click['o'] / counter_show['o'], 1)
    else:
        original_conversion = 'данные отсутствуют, т.к. не было переходов'
    if counter_click['t'] != 0:
        test_conversion = round(counter_click['t'] / counter_show['t'], 1)
    else:
        test_conversion = 'данные отсутствуют, т.к. не было переходов'
    context = {
            'test_conversion': test_conversion,
            'original_conversion': original_conversion
        }
    return render(request, 'stats.html', context)
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
    if request.GET.get('from-landing', ''):
        if request.GET['from-landing'] == 'test':
            counter_click.update('t')
        else:
            counter_click.update('o')
    # print(f'counter_click: {counter_click}')
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    template_requested = request.GET['ab-test-arg']
    if template_requested == 'test':
        sutable_template = 'landing_alternate.html'
        counter_show.update('t')
    else:
        sutable_template = 'landing.html'
        counter_show.update('o')
    # print(f'counter_show: {counter_show}')
    return render(request, sutable_template)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    if counter_click['o'] != 0:
        original_conversion = counter_click['o'] / counter_show['o']
    else:
        original_conversion = 'данные отсутствуют, т.к. не было переходов'
    if counter_click['t'] != 0:
        test_conversion = counter_click['t'] / counter_show['t']
    else:
        test_conversion = 'данные отсутствуют, т.к. не было переходов'
    print(f'original_conversion: {original_conversion}')
    print(f'test_conversion: {test_conversion}')
    context = {
            'test_conversion': test_conversion,
            'original_conversion': original_conversion
        }

    return render(request, 'stats.html', context)
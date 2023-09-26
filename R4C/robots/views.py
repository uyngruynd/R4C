import re
from datetime import datetime
from http import HTTPStatus

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot
from services.reports_service import RobotsReport, get_date, get_serial


def is_datetime_valid(text: str) -> bool:
    """Текстовое представление даты должно соответствовать формату datetime."""
    try:
        datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False


def is_name_valid(text: str) -> bool:
    """
    Часть имени должна состоять из двух символов: заглавная буква и цифра.
    """
    pattern = r'^[A-Z]\d$'
    return bool(re.fullmatch(pattern, text))


@csrf_exempt
def create(request):
    """Валидация данных запроса и запись нового робота в базу"""
    if not request.method == 'POST':
        raise PermissionDenied

    if not all(key in request.POST for key in ('model', 'version', 'created')):
        return HttpResponse('Проверьте наличие обязательных полей в запросе!',
                            status=HTTPStatus.BAD_REQUEST)

    model = request.POST['model'].strip().upper()
    version = request.POST['version'].strip().upper()
    created = request.POST['created'].strip()

    if not is_datetime_valid(created):
        return HttpResponse('Неверный формат даты!',
                            status=HTTPStatus.BAD_REQUEST)

    if not is_name_valid(model):
        return HttpResponse('Неверный формат модели!',
                            status=HTTPStatus.BAD_REQUEST)

    if not is_name_valid(version):
        return HttpResponse('Неверный формат версии!',
                            status=HTTPStatus.BAD_REQUEST)

    created = get_date(created)

    existing_models = Robot.objects.values_list('model', flat=True)

    if model not in existing_models:
        return HttpResponse(f'Модель {model} не зарегистрирована!',
                            status=HTTPStatus.BAD_REQUEST)

    serial = get_serial(model, version)

    is_robot_exists = Robot.objects.filter(serial=serial,
                                           created=created).exists()

    if is_robot_exists:
        return HttpResponse(
            f'Робот {serial} уже зарегистрирован на дату {created}!',
            status=HTTPStatus.BAD_REQUEST)

    robot = Robot(model=model,
                  version=version,
                  created=created,
                  serial=serial)
    robot.save()

    return HttpResponse('Новый робот успешно зарегистрирован!')


def report(request):
    """Вызов сервиса по формированию отчета по выпущенной продукции."""
    if not request.method == 'GET':
        raise PermissionDenied

    new_report = RobotsReport()
    return new_report.execute()

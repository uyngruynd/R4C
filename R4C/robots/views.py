from django.http import HttpResponse
from robots.models import Robot
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus
from datetime import datetime
from services.reports_service import RobotsReport


def is_datetime_valid(value: str) -> bool:
    try:
        datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False


def get_serial(model: str, version: str) -> str:
    return f'{model}-{version}'


@csrf_exempt
def create(request):
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
    if not request.method == 'GET':
        raise PermissionDenied

    new_report = RobotsReport()
    return new_report.execute()

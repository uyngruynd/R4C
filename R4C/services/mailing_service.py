from smtplib import SMTPException

from django.core.mail import send_mail

import orders.models


class CustomersMailing:
    def __init__(self, serial):
        self.serial = serial

    def execute(self):
        """
        Уведомляю пользователя, ожидающего поступления робота,
        появившегося на складе.
        """
        order = orders.models.Order.objects.filter(robot_serial=self.serial,
                                                   is_pending=True).first()

        if order:
            robot_serial_parts = order.robot_serial.split('-')
            subject = 'Ваш робот уже на нашем складе!'
            text = (f'Добрый день!\n'
                    f'Недавно вы интересовались нашим роботом '
                    f'модели {robot_serial_parts[0]}, '
                    f'версии {robot_serial_parts[1]}.\n'
                    f'Этот робот теперь в наличии. Если вам подходит этот '
                    f'вариант - пожалуйста, свяжитесь с нами)')

            try:
                send_mail(
                    subject,
                    text,
                    None,
                    [order.customer.email],
                    fail_silently=False,
                )
            except SMTPException:
                raise
            else:
                order.is_pending = False
                order.save()

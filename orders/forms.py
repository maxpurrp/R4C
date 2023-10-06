from django.forms import ModelForm, TextInput
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from robots.models import Robot
import smtplib
from .mail_conf import USER, PASSWRD, SERVER, PORT, CHARSET, MIME


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'robot_serial']
        widgets = {
                'customer': TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Ваш Email'}),
                'robot_serial': TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Желаемая Серия Робота в формате XX-YY'}
                        )}


def send_mail(model, version, client):
    subj = 'Robots Store'
    to = client
    text = f'Добрый День!\n Недавно вы заинтересовались нашим роботом модели {model}, версии {version}.\n Этот робот теперь в наличии. Если вам подходит этот вариант - свяжитесь с нами'
    body = "\r\n".join((f"From: {USER}", f"To: {to}", f"Subject: {subj}", MIME, CHARSET, "", text))
    try:
        smtp = smtplib.SMTP(SERVER, PORT)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(USER, PASSWRD)
        smtp.sendmail(USER, to, body.encode('utf-8'))
    except smtplib.SMTPException:
        print('so bad')
    finally:
        smtp.quit()
        print('successfuly send')


def get_customer(serial: str) -> str | None:
    robots = Order.objects.all().filter(robot_serial=serial)
    lst = None
    for robot in robots:
        if robot.robot_serial == serial:
            lst = robot.customer.email
    return lst


@receiver(pre_save, sender=Robot)
def my_callback(instance, **kwargs):
    serial = instance.serial
    client = get_customer(serial)
    if client:
        model = serial.split('-')[0]
        version = serial.split('-')[1]
        send_mail(model, version, client)

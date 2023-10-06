from django.shortcuts import render
from .forms import OrderForm
from customers.forms import CustomerForm
from customers.models import Customer


def check_robot(robot: str) -> bool:
    if robot[2] == '-':
        return True
    return False


# Create your views here.
def saving_order(request):
    if request.method == 'POST':
        data_custm = {'email': request.POST.get('customer')}
        form_custm = CustomerForm(data_custm)
        robot = request.POST.get('robot_serial')
        if check_robot(robot):
            if form_custm.is_valid():
                form_custm.save()
                person = Customer.objects.all().filter(email=request.POST.get('customer'))

                data_ord = {'customer': person[0],
                            'robot_serial': request.POST.get('robot_serial')}
                form_order = OrderForm(data_ord)
                if form_order.is_valid():
                    form_order.save()
                    success = {'success': f'Заявка отправлена успешно, при поступлении {request.POST.get("robot_serial")} на склад вам придет письмо на почту'}
                    return render(request, 'application.html', {'form': OrderForm(),
                                                                'success': success})
            else:
                errors = {}
                for eror in form_custm.errors:
                    errors[eror] = 'Данные указаны неверно'
                return render(request, 'application.html', {'form': OrderForm(),
                                                            'errors': errors})
        else:
            errors = {'robot_serial': 'Неверный формат ввода серии и модели робота. Например R2-DS'}
            return render(request, 'application.html', {'form': OrderForm(),
                                                        'errors': errors})
    form = OrderForm()
    data = {'form': form}
    return render(request, 'application.html', data)

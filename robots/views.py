from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot
from .forms import RobotForm


def get_serial(model: str, version: str) -> str:
    bar = "-"
    serial = model + bar + version
    return serial


# Create your views here.
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def update(request):
    if request.method == "POST":
        model = request.POST.get('model')
        version = request.POST.get('version')
        serial = get_serial(model, version)
        created = request.POST.get('created')

        form = RobotForm(data={'serial': serial,
                               'model': model,
                               'version': version,
                               'created': created})
        if form.is_valid():
            res, created = Robot.objects.get_or_create(
                serial=serial,
                model=model,
                version=version,
                created=created)
            if created:
                return HttpResponse('Succesfuly updated')
            return HttpResponse('already exists')
        return HttpResponse('Invalid data')
    return HttpResponse('Unsupported request type')

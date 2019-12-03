from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', )


def index(request):
    return render(request, 'account/index.html', )

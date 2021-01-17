from django.shortcuts import render


# Create your views here.
def index_demo(request):
    return render(request, 'demo/index.html')

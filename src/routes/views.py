from django.shortcuts import render

# Create your views here.
def main_route(request):
    return render(request, 'main_route.html')

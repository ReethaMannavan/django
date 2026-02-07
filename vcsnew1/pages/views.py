from django.shortcuts import render

def home_view(request):
    request.session.pop('registration_success', None)
    return render(request, 'pages/home.html')

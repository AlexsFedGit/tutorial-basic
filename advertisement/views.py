from django.shortcuts import render


def advertisement_list(request):
    return render(request, 'advertisement/advertisement_list.html')

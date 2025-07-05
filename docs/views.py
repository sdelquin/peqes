from django.shortcuts import render


def api_docs(request):
    return render(request, 'docs/api.html')


def disclaimer_docs(request):
    return render(request, 'docs/disclaimer.html')

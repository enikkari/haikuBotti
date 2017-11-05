from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


# Create your views here.
def indexx(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {
    #    'latest_question_list': latest_question_list,
    #}
    return render(request, 'ui/index.html')
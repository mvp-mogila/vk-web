from django.http import HttpRequest, HttpResponse 
from django.shortcuts import render

def index_view(request):
    questions = [
        {
            'id': i,
            'title': f"Title {i}",
            'user': f"User {i}",
            'datetime': '01.01.2023 10:10',
            'content': f"Some text {i} ?",
            'rating': -i * 2,
            'tags': [f"tag {j}" for j in range(3)]
        } for i in range(10)
    ]
    context = {'questions': questions}
    return render(request, "index.html", context)
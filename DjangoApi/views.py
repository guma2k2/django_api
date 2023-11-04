from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from unidecode import unidecode
import joblib
from urllib.parse import unquote
from sklearn.metrics import accuracy_score

stop_words = ['bai', 'hat', 'nay', 'nhac', 'nao', 'ma', 'no', 'ca','khuc','cac','cai','can','chi','va','vua','rat','nhung','ban']
def remove_custom_stop_words(text):
    words = text.lower().split()
    
    filtered_words = [word for word in words if word not in stop_words]
    
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

@csrf_exempt
def my_get_view(request):
    param_value = request.GET.get('text', '')
    model = joblib.load('/Applications/workspace/python_project/DjangoApi/DjangoApi/chandoan.pkl')
    text = unidecode(unquote(param_value))
    text = remove_custom_stop_words(text)
    print(text)
    new_text = [text]
    predicted = model.predict(new_text)
    print(predicted[0])
    return JsonResponse(predicted[0],safe=False)
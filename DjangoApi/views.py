from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from unidecode import unidecode
import joblib
from urllib.parse import unquote
@csrf_exempt
def my_get_view(request):
    param_value = request.GET.get('text', '')
    print(unquote(param_value))
    X_train = joblib.load('/Applications/workspace/python_project/DjangoApi/DjangoApi/X_train.pkl')
    y_train = joblib.load('/Applications/workspace/python_project/DjangoApi/DjangoApi/y_train.pkl')
    model = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SVC(kernel="rbf", C=1.0))
    ])

    model.fit(X_train, y_train)  # Fit the model with the training data

    text = unidecode(unquote(param_value))
    new_text = [text]
    predicted = model.predict(new_text)
    print(predicted[0])
    return JsonResponse(predicted[0],safe=False)
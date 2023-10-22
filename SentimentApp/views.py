from SentimentApp.models import Sentiment
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from unidecode import unidecode
import joblib

stop_words = ['bai', 'hat', 'nay', 'nhac', 'nao', 'ma', 'no', 'ca','khuc','cac','cai','can','chi','va','vua','rat','nhung']

@csrf_exempt
def handleRequest(request):
    if request.method == 'GET':
        sentiments=Sentiment.objects.all()
        save_dir = '/Applications/workspace/python_project/DjangoApi/DjangoApi/'
        train_data(sentiments,save_dir)
        return JsonResponse("Ok",safe=False)
    

def remove_custom_stop_words(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def parse(s):
    return unidecode(s)

def train_data(queryset, save_dir):
    data = [{'text': sentiment.text, 'sentiment': sentiment.sentiment} for sentiment in queryset]
    
    # Create a Pandas DataFrame
    df = pd.DataFrame(data)
    df['text'] = df['text'].apply(parse)
    df['text'] = df['text'].apply(remove_custom_stop_words)
    X, y = df['text'].tolist(), df['sentiment'].tolist()
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    print(X_train)
    
    # Save the training data to files
    joblib.dump(X_train, save_dir + 'X_train.pkl')
    joblib.dump(y_train, save_dir + 'y_train.pkl')
    
    # Create and fit the pipeline
    model = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SVC(kernel="rbf", C=1.0))
    ])
    model.fit(X_train, y_train)
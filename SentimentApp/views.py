from SentimentApp.models import Sentiment
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from unidecode import unidecode
import joblib
from rest_framework.parsers  import JSONParser
from SentimentApp.serializers import SentimentSerializer
stop_words = ['bai', 'hat', 'nay', 'nhac', 'nao', 'ma', 'no', 'ca','khuc','cac','cai','can','chi','va','vua','rat','nhung','ban']

@csrf_exempt
def handleRequest(request):
    if request.method == 'GET':
        sentiments=Sentiment.objects.all()
        save_dir = '/Applications/workspace/python_project/DjangoApi/DjangoApi/'
        score = train_data(sentiments,save_dir)
        return JsonResponse(score,safe=False)
    
@csrf_exempt    
def handleRequestAdmin(request):
    if request.method == 'GET':
        sentiments=Sentiment.objects.all()
        sentimentSerializer = SentimentSerializer(sentiments,many=True);
        return JsonResponse(sentimentSerializer.data,safe=False)
    elif request.method == 'POST':
        sentimentRequest = JSONParser().parse(request)
        sentimentSerializer = SentimentSerializer(data=sentimentRequest)
        check = Sentiment.objects.filter(text = sentimentRequest['text']).values()
        if check.exists():
            return JsonResponse("a text is duplicate",safe=False)
        else:
            if sentimentSerializer.is_valid():
                sentimentSerializer.save()
                return JsonResponse("save success",safe=False)

        
    

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

    model = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SVC(kernel="rbf", C=1.0))
    ])
    model.fit(X_train, y_train)

    predicted = model.predict(X_test)
    score =accuracy_score(predicted,y_test)*100
    print(score)
    joblib.dump(model, save_dir + 'chandoan.pkl')
    return score
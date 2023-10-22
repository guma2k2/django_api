from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from unidecode import unidecode
import joblib


X_train = joblib.load('X_train.pkl')
y_train = joblib.load('y_train.pkl')
model = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC(kernel="rbf", C=1.0))
])

model.fit(X_train, y_train)  # Fit the model with the training data

text = unidecode("bài hát ko buồn lắm")
new_text = [text]
predicted = model.predict(new_text)
print("predicted" , predicted)
print(accuracy_score(predicted,["buồn"])*100)






# fileName = "/Applications/workspace/python_project/predict.sav"
# pickle.dump(model,open(fileName,'wb'))


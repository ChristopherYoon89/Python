import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from sklearn import feature_extraction, model_selection, naive_bayes, pipeline, manifold, preprocessing, feature_selection, metrics
from sklearn.metrics import plot_confusion_matrix
import pickle

# cd C:\Users\yoc.HEROLD\OneDrive - dogado group\Dokumente\Developing\Python\Branch Classifyer


# Load dataset into program

dtf = pd.read_csv('Training_Data_Raw_Clean_True_Sample_500_FINAL.csv', sep=',', encoding='utf-8')


# Plot distribution of classes

fig, ax = plt.subplots()

fig.suptitle('Class', fontsize=12)

dtf['Class'].reset_index().groupby('Class').count().sort_values(by='index').plot(kind='barh', legend=False, ax=ax).grid(axis='x')

plt.show()


# Split dataset into training and test dataset

dtf_train, dtf_test = model_selection.train_test_split(dtf, test_size=0.1)

y_train = dtf_train['Class'].values

y_test = dtf_test['Class'].values


# Feature engineering using Tfid Vectorizer with a maximum limit of 30000 words and fit on training corpus

vectorizer = feature_extraction.text.TfidfVectorizer(max_features=30000, ngram_range=(1,2))

corpus = dtf_train["Text_Top50"]

vectorizer.fit(corpus)

X_train = vectorizer.transform(corpus)

dic_vocabulary = vectorizer.vocabulary_


# Feature extraction by performing a Chi-Square test in order to determine whether features and binary target are independent

y = dtf_train['Class']

X_names = vectorizer.get_feature_names()

p_value_limit = 0.95

dtf_features = pd.DataFrame()

for cat in np.unique(y):
    chi2, p = feature_selection.chi2(X_train, y==cat)
    dtf_features = dtf_features.append(pd.DataFrame({"feature":X_names, "score":1-p, "y":cat}))
    dtf_features = dtf_features.sort_values(["y","score"], ascending=[True,False])
    dtf_features = dtf_features[dtf_features["score"]>p_value_limit]

X_names = dtf_features["feature"].unique().tolist()

for cat in np.unique(y):
   print("# {}:".format(cat))
   print("  . selected features:", len(dtf_features[dtf_features["y"]==cat]))
   print("  . top features:", ",".join(dtf_features[dtf_features["y"]==cat]["feature"].values[:10]))
   print(" ")


# Refit the vectorizer on the corpus using the extracted words

vectorizer = feature_extraction.text.TfidfVectorizer(vocabulary=X_names)

vectorizer.fit(corpus)

X_train = vectorizer.transform(corpus)

dic_vocabulary = vectorizer.vocabulary_


# Define machine learning model using a Naive Bayes algorithm and create a pipeline with vectorizer and algorithm

classifier = naive_bayes.MultinomialNB()

model = pipeline.Pipeline([("vectorizer", vectorizer), ("classifier", classifier)])

model["classifier"].fit(X_train, y_train) # train model


# Test algorithm on testing dataset and evaluate performance

X_test = dtf_test["Text_Top50"].values

predicted = model.predict(X_test)

predicted_prob = model.predict_proba(X_test)

classes = np.unique(y_test)

y_test_array = pd.get_dummies(y_test, drop_first=False).values


## Accuracy, Precision, Recall

accuracy = metrics.accuracy_score(y_test, predicted)

auc = metrics.roc_auc_score(y_test, predicted_prob, multi_class="ovr")

print("Accuracy:",  round(accuracy,2))

print("Auc:", round(auc,2))

print("Detail:")

print(metrics.classification_report(y_test, predicted))


## Plot confusion matrix

cm = metrics.confusion_matrix(y_test, predicted)

fig, ax = plt.subplots()

sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap=plt.cm.Blues, cbar=False)

ax.set(xlabel="Pred", ylabel="True", xticklabels=classes, yticklabels=classes, title="Confusion matrix")

plt.yticks(rotation=0)


## Plot roc curve and precision-recall curve

fig, ax = plt.subplots(nrows=1, ncols=2)

for i in range(len(classes)):
    fpr, tpr, thresholds = metrics.roc_curve(y_test_array[:,i], predicted_prob[:,i])
    ax[0].plot(fpr, tpr, lw=2, label='{0} (area={1:0.2f})'.format(classes[i], metrics.auc(fpr, tpr)))

ax[0].plot([0,1], [0,1], color='navy', lw=2, linestyle='--')
ax[0].set(xlim=[-0.05,1.0], ylim=[0.0,1.05], xlabel='False Positive Rate', ylabel="True Positive Rate (Recall)", title="Receiver operating characteristic")
ax[0].grid(True)


for i in range(len(classes)):
    precision, recall, thresholds = metrics.precision_recall_curve(y_test_array[:,i], predicted_prob[:,i])
    ax[1].plot(recall, precision, lw=2, label='{0} (area={1:0.2f})'.format(classes[i], metrics.auc(recall, precision)))

ax[1].set(xlim=[0.0,1.05], ylim=[0.0,1.05], xlabel='Recall', ylabel="Precision", title="Precision-Recall curve")
ax[1].grid(True)
plt.tight_layout()
plt.show()


# Save model as pickle file

filename = 'Classification_Model1.sav'
pickle.dump(model, open(filename, 'wb'))


## load pickle file from directory

loaded_model = pickle.load(open(filename, 'rb'))

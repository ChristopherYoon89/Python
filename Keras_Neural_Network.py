import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.layers import Dropout
import pickle


# Load dataset into program

df = pd.read_csv('Training_Data_Raw_Clean_True_Sample_500_FINAL.csv', sep=',', encoding='utf-8')


# Define the maximum number of most frequent words used for training

MAX_NB_WORDS = 50000

# Define the maximum number of words in each document

MAX_SEQUENCE_LENGTH = 100

# Define size of embedding layer 

EMBEDDING_DIM = 100


# Clean and preprocess data

tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)

tokenizer.fit_on_texts(df['Text_Top100'].values)

word_index = tokenizer.word_index

print('Dataset includes %s unique tokens.' % len(word_index))


# Use tokenizer to reduce features and put them into same length for the model

X = tokenizer.texts_to_sequences(df['Text_Top100'].values)

X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)

print('Shape of data tensor:', X.shape)


# Convert branches/categories to dummies

Y = pd.get_dummies(df['Class']).values

print('Shape of label tensor:', Y.shape)


# Split dataset into train and test dataset

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.10, random_state = 42)

print(X_train.shape,Y_train.shape)

print(X_test.shape,Y_test.shape)


# Define the neural network model and add layers

model = Sequential()
model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X.shape[1]))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(30, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# Define parameters for the training process

epochs = 10
batch_size = 64

history = model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size,validation_split=0.1,callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)])

"""
Epoch 1/10
190/190 [==============================] - 48s 233ms/step - loss: 3.3299 - accuracy: 0.0568 - val_loss: 2.7465 - val_accuracy: 0.1616

Epoch 2/10
190/190 [==============================] - 46s 243ms/step - loss: 2.6218 - accuracy: 0.2174 - val_loss: 2.4607 - val_accuracy: 0.2276

Epoch 3/10
190/190 [==============================] - 55s 287ms/step - loss: 2.1239 - accuracy: 0.3501 - val_loss: 1.9390 - val_accuracy: 0.3988

Epoch 4/10
190/190 [==============================] - 47s 249ms/step - loss: 1.5604 - accuracy: 0.5294 - val_loss: 1.5267 - val_accuracy: 0.5448

Epoch 5/10
190/190 [==============================] - 46s 242ms/step - loss: 1.0613 - accuracy: 0.6898 - val_loss: 1.4558 - val_accuracy: 0.5589

Epoch 6/10
190/190 [==============================] - 47s 249ms/step - loss: 0.7276 - accuracy: 0.7973 - val_loss: 1.2062 - val_accuracy: 0.6679

Epoch 7/10
190/190 [==============================] - 46s 240ms/step - loss: 0.4754 - accuracy: 0.8782 - val_loss: 1.0980 - val_accuracy: 0.7116

Epoch 8/10
190/190 [==============================] - 45s 236ms/step - loss: 0.3312 - accuracy: 0.9184 - val_loss: 1.3245 - val_accuracy: 0.6575

Epoch 9/10
190/190 [==============================] - 46s 242ms/step - loss: 0.3163 - accuracy: 0.9246 - val_loss: 1.1268 - val_accuracy: 0.7079

Epoch 10/10
190/190 [==============================] - 45s 237ms/step - loss: 0.2286 - accuracy: 0.9479 - val_loss: 1.0447 - val_accuracy: 0.7487

"""


# Evalute the accuracy of the model and print result

accr = model.evaluate(X_test,Y_test)

print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))


# Plot loss function of the model

plt.title('Loss')
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show();


# Plot accuracy function of the model

plt.title('Accuracy')
plt.plot(history.history['accuracy'], label='train')
plt.plot(history.history['val_accuracy'], label='test')
plt.legend()
plt.show();


# Test the model on new data

New_Website = ['Publikationen Nachhaltigkeit Public Hansen Lehre Erdbau Altlasten Umwelttechnik Design Engineering Abdichtung Jobbörse Investor Relations Compliance Einkauf Karrierewege Weiterbildung Images flags czech eská Republika e tina Organisation Magazin Digitales Fachmagazin Länderseiten Français Polska Polski România Român Slovensko Sloven Revitalisierung Palais Hotel Bauüberwachung Großprojekte Einkaufszentren Industrie Sonderbauten Bauten Stadien Wohnbau Bahnbau Brückenbau Ingenieurbau Kraftwerksbau Leitungsbau Spezialtiefbau Straßenbau Tunnelbau Überregionaler Wasserbau Rückbau Deponie Kies Transport Umweltlabor Architektur Bauphysik Bauvorbereitung Brandschutz Building Modeling Generalplanung LEAN Techn Tragwerksplanung Beschichtung Betondeckenbau Facility Fassadenbau Feste Fahrbahn Flughafenbau Health Care Hochgebirgsbau Hochhäuser Partnership Property Stahlbau Broschüren Ansprechpersonen Öffentliche Abbruch Traineeprogramm']

seq = tokenizer.texts_to_sequences(New_Website)

padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)

pred = model.predict(padded)

labels = ['Class_10', 'Class_11', 'Class_12', 'Class_13', 'Class_14', 'Class_15', 'Class_16', 'Class_17', 'Class_1', 'Class_20', 'Class_21', 'Class_22', 'Class_23', 'Class_24', 'Class_25', 'Class_26', 'Class_27', 'Class_28', 'Class_29', 'Class_2', 'Class_30', 'Class_31', 'Class_32', 'Class_33', 'Class_3', 'Class_4', 'Class_5', 'Class_6', 'Class_8', 'Class_9']

print(pred, labels[np.argmax(pred)])


# Save model to your directory

model.save('C:/Users/Dokumente/Developing/Python/ANN_Classifyer')


# Save Tokenizer to your directory as pickle file

filename = 'Tokenizer_ANN.sav'

pickle.dump(tokenizer, open(filename, 'wb'))


# Load model

model = keras.models.load_model('C:/Users/Dokumente/Developing/Python/ANN_Classifyer')


# Load tokenizer

tokenizer = pickle.load(open('Tokenizer_ANN.sav', 'rb'))

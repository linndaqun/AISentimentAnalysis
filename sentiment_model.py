import tensorflow as tf
import pandas as pd
import re
import ast
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM
from sklearn.model_selection import train_test_split

"""
WORK IN PROGRESS
"""

# Get data
data = pd.read_csv("trainingandtestdata/norm_training_vectors.csv")
# Remove quotations from vector lists (result of converting lists to csv)
data['vector'] = data['vector'].apply(ast.literal_eval)

X_train = data['vector']
target = data['sentiment']

X_train, X_valid, y_train, y_valid = train_test_split(X_train, target, random_state=0)
print(X_train[0])

""" LSTM """

def create_lstm_model(embed_dim, lstm_out, batch_size):
    model = Sequential()
    model.add(Embedding(2500, embed_dim, input_length = 100, dropout = 0.2))
    model.add(LSTM(lstm_out, dropout = 0.2, recurrent_dropout = 0.2))
    model.add(Dense(1,activation='softmax'))
    model.compile(loss = 'sparse_categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
    print(model.summary())
    return model

def create_simple_model():
    model = Sequential()
    model.add(Dense(12, input_dim=1, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1, activation='softmax'))
    model.compile(loss = 'sparse_categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
    print(model.summary())
    return model

# model = create_lstm_model(128, 200, 32)
model = create_simple_model()
model.fit(X_train, y_train, batch_size = 50, nb_epoch = 1,  verbose = 5)
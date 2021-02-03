# -*- coding: utf-8 -*-
"""artificial_neural_network_implementation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18_bYyJt7Lh7o9xN-qBROamlXigbedkBC

# Artificial Neural Network

### Importing the libraries
"""

import numpy as np
import tensorflow as tf
import pandas as pd

tf.__version__

"""## Part 1 - Data Preprocessing

### Importing the dataset
"""

dataset = pd.read_csv('Churn_Modelling.csv')

#Extracting all the features (from the dataset, I am removing columns which doesnt affect the target like first 3 in the dataset)
X = dataset.iloc[:, 3:-1].values
#Extracting the target variable (Exited) (Binary Variable)
y = dataset.iloc[:, -1].values

#taking a look at features from the dataset
print(X)

#taking a look at target variable
print(y)

"""### Encoding categorical data

Label Encoding the "Gender" column
"""

from sklearn.preprocessing import LabelEncoder
# label encoding the gender column as it is a categorical variable.
le = LabelEncoder()
X[:,2] = le.fit_transform(X[:,2])

print(X)

"""One Hot Encoding the "Geography" column"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

#One-Hot encoding the Geography columns as it is a categorical variable.
#can do other encoding but for a practice, I did label encoding to 'Gender' column and One-hot to 'Geography' column
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')

#fit and transforming the features
X = np.array(ct.fit_transform(X))

print(X)

"""### Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
#Splitting the dataset into train and test with  4:1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""### Feature Scaling"""

# In deep learning, feature scaling is necessary and crucial. 
# I used standard scaling, we can use other scalers also like MinMaxScaler.
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""## Part 2 - Building the ANN

### Initializing the ANN
"""

ann =tf.keras.models.Sequential()

"""### Adding the input layer and the first hidden layer

We can add any number of layers with any number of neurons or nodes. There is no fixed-procedure to get the values of them. It is the job of practitioner to experiment and get the best model. 

**Note:** Keras is included in Tensorflow 2.0 and higher versions.

**PS** : *Neurons individually cannot do much but layers of them combined together possess super-power. Just like an ant cannot do much but colony of them can build an anthill.*
"""

# the first hidden layer with 6 neurons or nodes with rectifier activation function. 'relu' is the code for it.
 ann.add(tf.keras.layers.Dense(units=6,activation='relu'))

"""### Adding the second hidden layer"""

# adding another hidden layer with 6 neurons or nodes with rectifier activation function.
ann.add(tf.keras.layers.Dense(units=6,activation='relu'))

"""### Adding the output layer"""

# finally, adding the output layer with only one node as the target is binary which mean only one value is predicted. 
 # also , the activation function is sigmoid coz its a binary classification. 
 ann.add(tf.keras.layers.Dense(units=1,activation='sigmoid'))

"""## Part 3 - Training the ANN

### Compiling the ANN
"""

#compiling the neural network means configuring it with some default settings.(those settings are provided as kwargs as below)
#To get optimal weights , optimisation is necessary. I used 'adam' optimizer here.
# as its a binary classification, loss function should be 'binary_crossentropy'

ann.compile(optimizer = 'adam', loss='binary_crossentropy', metrics=['accuracy'])

"""**Note** : If its non-binary classification, then loss function would be '*categorical_crossentropy*' and activation function would be '*softmax*'.

### Training the ANN on the Training set
"""

#this part is favourite. fitting the model with training set. 
# i did batch learning with batch_size =32, and epochs =100

#we can play with those kwargs.

ann.fit(X_train,y_train,batch_size= 32,epochs=54)

"""## Part 4 - Making the predictions and evaluating the model

### Predicting the result of a single observation

**Just for practice**

Use the ANN model to predict if the customer with the following informations will leave the bank: 

Geography: France

Credit Score: 600

Gender: Male

Age: 40 years old

Tenure: 3 years

Balance: \$ 60000

Number of Products: 2

Does this customer have a credit card? Yes

Is this customer an Active Member: Yes

Estimated Salary: \$ 50000

So, should we say goodbye to that customer?

**Solution**
"""

print(ann.predict(
   sc.transform([[1,0,0,600,1,40,3,60000,2,1,1,50000]])
)> 0.5)

#to get boolean if we cross the 50% probability

"""Note : As our model is fit with scaled training data, we need to scale our test observation also.

Therefore, our ANN model predicts that this customer stays in the bank!

**Important note 1:** Notice that the values of the features were all input in a double pair of square brackets. That's because the "predict" method always expects a 2D array as the format of its inputs. And putting our values into a double pair of square brackets makes the input exactly a 2D array.

**Important note 2:** Notice also that the "France" country was not input as a string in the last column but as "1, 0, 0" in the first three columns. That's because of course the predict method expects the one-hot-encoded values of the state, and as we see in the first row of the matrix of features X, "France" was encoded as "1, 0, 0". And be careful to include these values in the first three columns, because the dummy variables are always created in the first columns.

### Predicting the Test set results
"""

y_pred = ann.predict(X_test)
# Just setting a threshold of 50 % upon predictions
y_pred= (y_pred > 0.5)
print(
    np.concatenate((y_pred.reshape(len(y_pred),1),
                    y_test.reshape(len(y_test),1)),1)
)

"""### Making the Confusion Matrix"""

#Confusion Matrx gives an overview of model's predictions.
# tt, tf
# ft, ff
# t -true, f-false

from sklearn.metrics import confusion_matrix,accuracy_score
cm = confusion_matrix(y_test,y_pred)

print(cm)

accuracy = accuracy_score(y_test,y_pred)
print('accuracy : ',accuracy)
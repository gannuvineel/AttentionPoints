#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import all the required libraries

import pandas as pd
import sklearn as sk
from keras.utils import normalize
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import pickle
import seaborn as sns


# # Dataset 
#    We created the dataset using the Unity software and Tobii eye tracker 4C which tracks the gaze position.
#    
#    We used 6 different images that represents happiness and neural emotions. Two different images with different emotions      are used to create the dataset. 
#    
#    Altogether, we created 1000 data instances along with the labels. It includes 33 different features, of which 3 are        target features.

# In[2]:


# Loads the train and test data from train_data.csv and test_data.csv files respectively.
def load_traindata():
    input_file = pd.read_csv('train_data.csv')
    return input_file
def load_testdata():
    test_file = pd.read_csv('test_data.csv')
    return test_file


# In[3]:


features = ['object1position_x','object1position_y','object1position_z','object1scaling_x',
            'object1scaling_y','object1scaling_z','object2position_x','object2position_y',
            'object2position_z','object2scaling_x','object2scaling_y','object2scaling_z',
            'cameraposition_x','cameraposition_y','cameraposition_z','camerascaling_x',
            'camerascaling_y','camerascaling_z','wallposition_x','wallposition_y',
            'wallposition_z','wallscaling_x','wallscaling_y','wallscaling_z',
            'planeposition_x','planeposition_y','planeposition_z',
            'planescaling_x','planescaling_y','planescaling_z']
output_label=['attentionposition_x','attentionposition_y','attentionposition_z']


# # Exploratory data analysis (EDA) for the dataset to visualize the data
# 

# ## Shape of the dataset (Number of instances, Number of features)
# <br>
# The shape property is used to get the current shape of an array.
# 
# 

# In[4]:


print(load_traindata().shape)
print(load_testdata().shape)


# ## Features in the dataset
# <br>
# The column property is used to get the columns for a given data.

# In[5]:


print(load_traindata().columns)


# ## First few instances in the dataset
# <br>
# Using the head method, the first three instances of the dataset is printed.

# In[6]:


print(load_traindata().head(3))


# ## 3D Scatter Plot between the positions of two different objects (features)
# <br>
# From the first few datapoints, we can see the random scaling in the dataset. Thus we need to normalize the data before giving it to the model.
# <br>

# In[7]:


from mpl_toolkits import mplot3d

def scatter_Plot():
    ax = plt.axes(projection='3d')
    
    # Data for three-dimensional scattered points
    
    zdata = load_traindata()['object1position_z']
    xdata = load_traindata()['object1position_x']
    ydata = load_traindata()['object1position_y']
    z = load_traindata()['object2position_z']
    x = load_traindata()['object2position_x']
    y = load_traindata()['object2position_y']
    ax.scatter3D(xdata, ydata, zdata,cmap='Greens');
    ax.scatter3D(x, y, z,cmap='Oranges');

scatter_Plot()


# ## Correlation Matrix
# <br>
# Heatmap and corr functions are used to plot the correlation matrix.

# In[8]:


def correlation_matrix():
    f, ax = plt.subplots(figsize=(10, 8))
    position_features = ['object1position_x','object1position_y','object1position_z','object2position_x',
                         'object2position_y','object2position_z','attentionposition_x',
                         'attentionposition_y','attentionposition_z']
    input = load_traindata()[position_features]
    corr = input.corr()
    sns.heatmap(corr, mask = np.zeros_like(corr, dtype = np.bool), 
                cmap = sns.diverging_palette(240,10,as_cmap = True),square = True, ax = ax)
    
correlation_matrix()


# ## Pair plot
# <br>
# Pair plot is used to plot the pairwise relationships in a dataset.

# In[9]:


def pair_plot():
    plt.close();
    sns.set_style("whitegrid");
    obj_position = ['object1position_x','object1position_y','object1position_z','object2position_x',
                  'object2position_y','object2position_z']
    eye_position = ['attentionposition_x','attentionposition_y','attentionposition_z']
    input1 = load_traindata()[eye_position]
    sns.pairplot(load_traindata()[obj_position]);
    sns.set(style = "ticks", color_codes = True)
    plt.show()

pair_plot()


# ## Data Normalization
# <br>
# All the input features are normalized using MinMaxScaler.

# In[10]:


def data_normalize():
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    dataset = load_traindata()
    dataset[features] = pd.DataFrame(scaler_x.fit_transform(dataset[features]))
    dataset[output_label] = pd.DataFrame(scaler_y.fit_transform(dataset[output_label]))
    x_test = pd.DataFrame(scaler_x.fit_transform(load_testdata()[features]))
    y_test = pd.DataFrame(scaler_y.fit_transform(load_testdata()[output_label]))
    return dataset[features],dataset[output_label],x_test,y_test


# ## Split Data
# <br>
# The input data is split into trianing and validation data.

# In[11]:


def split_data():
    data = data_normalize()
    x_train, x_valid, y_train, y_valid = train_test_split(data[0], data[1], 
                                                          test_size = 0.3, random_state = 42)    
    return x_train,x_valid,y_train,y_valid


# # Model Buildling
# <br>
# Multilayer perceptron model is built using Adam optimizer and mean squared error as the loss function.  

# In[12]:


def build_model():
    model = Sequential()
    model.add(Dense(30, input_dim=30, activation='tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(16,activation='tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(8, activation='tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='tanh'))
    opt = Adam(learning_rate=0.0001, beta_1 = 0.88, beta_2 = 0.911, amsgrad=False)
    model.compile(loss = 'mean_squared_error', optimizer = opt, metrics = ['mse'])
    return model


# # Model Training
# <br>
# The built model is compiled and serialized using pickle.

# In[13]:


def train_model():
    X_train,X_valid,y_train,y_valid=split_data()
    built_model = build_model()
    # fit the keras model on the dataset
    #model.fit(X_train, y_train, epochs=20, batch_size=1)
    history = built_model.fit(X_train, y_train, epochs = 350, validation_data = (X_valid, y_valid))
    filename = 'finalized_model.sav'
    pickle.dump(built_model, open(filename, 'wb'))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc ='upper left')
    plt.show()
    plt.savefig('loss')
    return built_model


# # Model Evaluation
# <br>
# The built model is de-serialized using pickle and evaluated.
# 

# In[14]:


def model_evaluate():
    filename = 'finalized_model.sav'
    Trained_model = pickle.load(open(filename, 'rb'))
    scaler_y = MinMaxScaler()
    scaler_y.fit_transform(load_testdata()[output_label])
    
    X_train,y_train = split_data()[0],split_data()[2]
    
    pred_train = Trained_model.predict(X_train)
    print('Training MSE',mean_squared_error(y_train,pred_train))
    
    X_test,y_test = data_normalize()[2],data_normalize()[3]
    predicted_value = Trained_model.predict(X_test)
    print('Test MSE',mean_squared_error(y_test,predicted_value))
    
    #predicted_scaler = MinMaxScaler()
    #scaler.fit(predicted_value)
    print("Predicted Value\n ",predicted_value,"\n Denormalized Value\n ", 
          scaler_y.inverse_transform(predicted_value).round(1))
    #print(output[0][0],output[0][1],output[0][2])
    #print(predicted)
   
    
    #visualizing object1 and object2 positions in 3D


# In[15]:


train_model()


# In[16]:


model_evaluate()


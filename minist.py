import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import keras
#Handwritten Labelled Dataset
from keras.datasets import mnist
from keras.models import Sequential
#Dense Means fully connected layers , Dropout is a technique to improve convergence ,
# Flatten is to reshape the matrix for giving to different layers
from keras.layers import Dense,Dropout,Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import keras.optimizers as optimizers

#mini batch gradient descent ftw
batch_size = 128
#10 difference characters
num_classes = 10
#very short training time
epochs = 12

#input image dimensions
#28x28 pixel images.
img_rows, img_cols = 28, 28

# the data downloaded, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data(path='/home/liwensh2/code/mnist/mnist.npz')

#this assumes our data format
#For 3D data, "channels_last" assumes (conv_dim1, conv_dim2, conv_dim3, channels) while
#"channels_first" assumes (channels, conv_dim1, conv_dim2, conv_dim3).
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)


#more reshaping
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
#convolutional layer with rectified linear unit activation
model.add(Conv2D(64, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))

#again
model.add(Conv2D(128, (3, 3), activation='relu'))
#choose the best features via pooling
model.add(MaxPooling2D(pool_size=(2, 2)))

#randomly turn neurons on and off to improve convergence
model.add(Dropout(0.25))
#flatten since too many dimensions, we only want a classification output
model.add(Flatten())

#fully connected to get all relevant data
model.add(Dense(128, activation='relu'))
#one more dropout for convergence' sake :)
model.add(Dropout(0.5))


# sgd = optimizers.SGD(lr=0.01, nesterov=False)
# sgd = optimizers.SGD(lr=0.3, nesterov=True)
# sgd = optimizers.SGD(lr=0.01, nesterov=True)
sgd = optimizers.SGD(lr=0.3, nesterov=False)

#output a softmax to squash the matrix into output probabilities
model.add(Dense(num_classes, activation='softmax'))
#Adaptive learning rate (adaDelta) is a popular form of gradient descent rivaled only by adam and adagrad
#categorical ce since we have multiple classes (10)
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=sgd,
              metrics=['accuracy'])

#train that ish!
result=model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=100,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
loss=result.history['loss']
accuracy = result.history['acc']
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print(loss)
print(accuracy)

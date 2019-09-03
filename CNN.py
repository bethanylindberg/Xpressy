# Dependencies to Visualize the model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Filepaths, numpy, and Tensorflow
import os
import numpy as np
import keras

# Preprocessing imports
import glob
import os.path as path
import imageio
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

# Model Imports
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from sklearn.metrics import accuracy_score, f1_score

from datetime import datetime

# root = 'samples'
root = 'Data'

# Load the images
file_paths = []
labels = []
targets = []

emotions = ['angry','disgust','fear','happy','neutral','sad','surprise']
x=0
e=0
for emotion in emotions:
    print(emotion)
    for filename in glob.glob(f"{root}/{emotion}/*.jpg"):
        path = filename.split('\\')[0]+'/'+filename.split("\\")[1]
        file_paths.append(path)
        labels.append(e)
        targets.append(emotion)
        x+=1
        print(x)
        # if x == 10:
        #     x = 0
        #     break
            
    for filename in glob.glob(f"{root}/{emotion}/*.png"):
        path = filename.split('\\')[0]+'/'+filename.split("\\")[1]
        file_paths.append(path)
        labels.append(e)
        targets.append(emotion)
        x+=1
        print(x)
        # if x == 10:
        #     x=0
        #     break
    e+=1
    x=0

# Load the images
images = []
image_size = (48,48)

for path in file_paths:
    print(f"{x} of {len(file_paths)}")
    x+=1
    img = load_img(path,target_size = image_size,color_mode='grayscale')
    img = img_to_array(img)
    images.append(img)

images = np.asarray(images)       

# Get image size
image_size = np.asarray([images.shape[1], images.shape[2], images.shape[3]])

# df = pd.DataFrame(list(zip(targets, labels,images,file_paths)),columns=["emotions","labels","images","paths"])
# df.to_csv('emotions.csv')

# Scale
images = images / 255

#Split into training and testing data
X = images
y = labels
from sklearn.model_selection import train_test_split
# 80/10/10 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.111, random_state=1)


from keras.utils import to_categorical
num_classes=7

# Prepare y data
y_binary_train = to_categorical(y_train, num_classes=num_classes, dtype='float32')
y_binary_test = to_categorical(y_test, num_classes=num_classes, dtype='float32')

# Define hyperparamters
KERNEL = (3, 3)
num_features = 64
# Training hyperparamters
EPOCHS = 500
BATCH_SIZE = 500
PATIENCE = 3
width, height = 48,48

#desinging the CNN
model = Sequential()

model.add(Conv2D(num_features, KERNEL, activation='relu', input_shape=(width, height, 1)))
model.add(Conv2D(num_features, KERNEL, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(2*num_features, KERNEL, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(2*num_features, KERNEL, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(2*2*num_features, KERNEL, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(2*2*num_features, KERNEL, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(2*2*2*num_features, KERNEL, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(2*2*2*num_features, KERNEL, activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(2*2*2*num_features, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(2*2*num_features, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(2*num_features, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Print a summary of the model
model.summary()

# Early stopping callback
early_stopping = EarlyStopping(monitor='loss', min_delta=0, patience=PATIENCE, verbose=3, mode='auto')

# TensorBoard callback
# LOG_DIRECTORY_ROOT = ''
# now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
# log_dir = "{}/run-{}/".format(LOG_DIRECTORY_ROOT, now)
# tensorboard = TensorBoard(log_dir=log_dir, write_graph=True, write_images=True)

# Place the callbacks in a list
callbacks = [early_stopping]

# Train the model
model.fit(np.array(X_train), np.array(y_train), epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks, verbose=3)

# Make a prediction on the test set
test_predictions = model.predict(X_test)
test_predictions = np.argmax(test_predictions , axis=1)
test_predictions

# Report the accuracy
accuracy = accuracy_score(y_test, test_predictions)
print("Accuracy: " + str(accuracy))

# Save the model
model.save("emotion_model_trained.h5")
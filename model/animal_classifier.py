#!/usr/bin/python

import numpy as np
import tensorflow as tf

class AnimalClassifier():
    def __init__(self, batch_size=64, img_size=128, directory='/kaggle/input/animals10/raw-img'):
        self.batch_size = batch_size
        self.img_size = img_size
        self.directory = directory

        self._class_names = ['dog', 'horse', 'elephant', 'butterfly', 'chicken', 'cat', 'cow', 'sheep', 'spider', 'squirrel']
        self._model = None

    def preprocess_data(self):
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1/255.,
            zoom_range=0.2,
            horizontal_flip=True,
            validation_split=0.1
        )

        train_generator = datagen.flow_from_directory(
            self.directory,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            shuffle=True,
            subset='training',
            class_mode='categorical'
        )

        validation_generator = datagen.flow_from_directory(
            self.directory,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            shuffle=False,
            subset='validation',
            class_mode='categorical'
        )

        return train_generator, validation_generator

    def build_model(self):
        self.model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', input_shape=(self.img_size, self.img_size, 3)),
                tf.keras.layers.MaxPooling2D(pool_size=2),

                tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu'),
                tf.keras.layers.MaxPooling2D(pool_size=2),

                tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu'),
                tf.keras.layers.MaxPooling2D(pool_size=2),

                tf.keras.layers.Flatten(),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dropout(0.1),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dropout(0.3),

                tf.keras.layers.Dense(10, activation='softmax')
            ]
        )

        self.model.compile(
            loss=tf.keras.losses.categorical_crossentropy,
            optimizer=tf.keras.optimizers.Adadelta(learning_rate=0.1),
            metrics=['accuracy']
        )

    def train_model(self, train_generator, validation_generator):
        early_stop = tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            mode='max',
            verbose=1,
            patience=30,
            restore_best_weights=True
        )
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_accuracy',
            factor=0.1,
            patience=10,
            verbose=1,
            min_delta=1e-4
        )

        with tf.device('/GPU:0'):
            self.model.fit(
                train_generator,
                validation_data=validation_generator,
                batch_size=self.batch_size,
                epochs=200,
                callbacks=[early_stop, reduce_lr]
            )

    def save_model(self, save_path):
        self._model.save(save_path)

    def preprocess_input_data(self, path):
        process_image = tf.io.read_file(path)
        process_image = tf.image.decode_image(process_image, channels=3)  

        resized_image = tf.image.resize(process_image, size=(self.img_size, self.img_size))

        input_tensor = tf.convert_to_tensor(resized_image, dtype=tf.float32)
        input_tensor = tf.expand_dims(input_tensor, 0)  # Add a batch dimension if needed

        return input_tensor
    
    def run_predict(self, input_data):
        
        prediction_result = self._model.predict(input_data)
        predicted_class = np.argmax(prediction_result, axis=1)

        predicted_class = predicted_class[0]

        return self._class_names[predicted_class]
    
    def load_model(self, path='./classifier_model/model_2.h5'):
        self._model =  tf.keras.models.load_model(path)
        return self._model
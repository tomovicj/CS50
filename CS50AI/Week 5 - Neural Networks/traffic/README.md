### First run:
Same as shown in lecture, digits handwriting project
```python
model = tf.keras.models.Sequential([
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),

    # Add an output layer with output output categories
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
```
Results: `accuracy: 0.0551 - loss: 3.5058`

---

### Second run:
After adding a second hidden layer (128 units, activation="relu"):
Results: `accuracy: 0.8242 - loss: 0.6566`

---

### Third run:
After adding a third hidden layer (128 units, activation="relu") or increasing the number of units in the first and second hidden layer to 256, Did not improve the accuracy by much.

---

### Fourth run:
Adding convolutional layers and max pooling layers before the flatten layer, increased the accuracy to `accuracy: 0.9606 - loss: 0.1601`

---

### Fifth run:
After increasing the number of filters in the convolutional layers to 64, accuracy is not improved. `accuracy: 0.9359 - loss: 0.2646`

---

### Final run:
My best model is the fourth run, which has 2 convolutional layers and 2 max pooling layers before the flatten layer. The final model architecture is as follows:

```python
model = tf.keras.models.Sequential([
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT / 2, IMG_WIDTH / 2, 3)
    ),
            
    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layers with dropout
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),
            
    # Add an output layer with output categories
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
```

Results:

```
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 8s 11ms/step - accuracy: 0.3539 - loss: 2.6685  
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.7105 - loss: 0.9717 
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.8404 - loss: 0.5359 
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.8889 - loss: 0.3817 
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 10ms/step - accuracy: 0.9229 - loss: 0.2712 
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.9329 - loss: 0.2400 
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.9382 - loss: 0.2271 
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.9572 - loss: 0.1530 
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.9595 - loss: 0.1578 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 11ms/step - accuracy: 0.9626 - loss: 0.1427 
333/333 - 2s - 5ms/step - accuracy: 0.9618 - loss: 0.1792
```

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt


(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()


# print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0

y_train = to_categorical(y_train, 10)
y_test  = to_categorical(y_test, 10)

fig, axes = plt.subplots(2, 5, figsize=(10, 5))
class_names = ["airplane","automobile","bird","cat","deer",
               "dog","frog","horse","ship","truck"]
for i, ax in enumerate(axes.flatten()):
    ax.imshow(x_train[i])
    label = tf.math.argmax(y_train[i]).numpy()
    ax.set_title(class_names[label])
    ax.axis("off")
plt.show()


model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(32,32,3)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax"),
])
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model.summary()


model.fit(x_train, y_train, epochs=20, batch_size=64,
          validation_split=0.1)

model.evaluate(x_test, y_test)
import tensorflow as tf
import tf2onnx


inputs = tf.keras.Input(shape=(32, 32, 3), name="my_input")
x = tf.keras.layers.Conv2D(16, 3, activation="relu")(inputs)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
outputs = tf.keras.layers.Dense(10, activation="softmax", name="preds")(x)
model = tf.keras.Model(inputs, outputs)


spec = (
    tf.TensorSpec([None, 32, 32, 3], tf.float32, name="my_input"),
)


onnx_model_proto, external_tensor_storage = tf2onnx.convert.from_keras(
    model,
    input_signature=spec,
    opset=13,
)


with open("model.onnx", "wb") as f:
    f.write(onnx_model_proto.SerializeToString())

print("ONNX export complete. Saved to model.onnx")

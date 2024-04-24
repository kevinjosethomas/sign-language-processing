from keras import ops
import tensorflow as tf

LETTERS = "ABCDEFGHIKLMNOPQRSTUVWXY"


class Classifier:
    def __init__(self):
        self.model = tf.keras.models.load_model("asl/model.keras")

    def classify(self, points):
        predictions = self.model.predict(points, verbose=0)
        prediction = ops.argmax(predictions, -1)
        probability = predictions[0][prediction[0]]
        letter = LETTERS[prediction[0]]

        return letter, probability

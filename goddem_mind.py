import numpy as np 
from tensorflow.keras.datasets import mnist

#импорт данных мнист
(x_train, y_train), (x_test, y_test) = mnist.load_data()

#из диапозона 255 переводим в диапазон 0 ... 1
x_train = x_train / 255.0
x_test = x_test / 255.0

#нужный формат
x_train = x_train.reshape(-1, 784)
x_test = x_test.reshape(-1, 784)

#Переводим цифры от 1 до 9 в массив
def to_one_hot(y, num_classes=10):
    one_hot = np.zeros((len(y), num_classes))
    one_hot[np.arange(len(y)), y] = 1
    return one_hot

#применение
y_train_one_hot = to_one_hot(y_train)
y_test_one_hot = to_one_hot(y_test)


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        #Рандомно назначаем нейроны маленькими числами
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    #оставляет онли положительные числа
    def relu(self, x):
        return np.maximum(0, x)
    
    def softmax(self, x):
        #Вычитаем максмум для точных вычислений
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        #принятие данных
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
    
    #перевод в циферки
    def predict(self, X):
        output = self.forward(X)
        return np.argmax(output, axis=1)
    
    #Вычисление ошибки
    def backward(self, X, y, output, learning_rate):
        m = X.shape[0]
        dz2 = output - y
        dw2 = (1 / m) * np.dot(self.a1.T, dz2)
        db2 = (1 / m) * np.sum(dz2, axis=0, keepdims=True)
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * (self.z1 > 0)
        dw1 = (1 / m) * np.dot(X.T, dz1)
        db1 = (1 / m) * np.sum(dz1, axis=0, keepdims=True)
        self.W1 -= learning_rate * dw1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dw2
        self.b2 -= learning_rate * db2

    #работа над ошибками
    def compute_loss(self, y, output):
        m = y.shape[0]
        log_probs = -np.log(output + 1e-8)
        loss = np.sum(log_probs * y) / m
        return loss
    
    #астрология
    def accuracy(self, X, y_true):
        predictions = self.predict(X)
        true_labels = np.argmax(y_true, axis=1)
        acc = np.mean(predictions == true_labels)
        return acc
        
#Обучение
nn = NeuralNetwork(784, 128, 10)
learning_rate = 0.1
epochs = 50
batch_size = 64
num_batches = len(x_train) // batch_size

for epoch in range(epochs):
    epoch_loss = 0
    #перемешивание данных
    indices = np.random.permutation(len(x_train))
    x_shuffled = x_train[indices]
    y_shuffled = y_train_one_hot[indices]

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = start_idx +batch_size
        x_batch = x_shuffled[start_idx:end_idx]
        y_batch = y_shuffled[start_idx:end_idx]

        output = nn.forward(x_batch)
        batch_loss = nn.compute_loss(y_batch, output)
        epoch_loss += batch_loss
        nn.backward(x_batch, y_batch, output, learning_rate)

    avg_loss = epoch_loss / num_batches
    test_acc = nn.accuracy(x_test, y_test_one_hot)
    print(f"Epoch {epoch+1}/{epoch}, Loss: {avg_loss:.4f}, Test Accuracy: {test_acc:.4f}")

#test
simple_idx = 0
simpl_image = x_test[simple_idx].reshape(1, -1)
prediction = nn.predict(simpl_image)
print(f"Godden answer: {prediction[0]}")
print(f"True answer: {y_test[simple_idx]}")
print(f"Pixsels: {x_test[simple_idx][:10]}")



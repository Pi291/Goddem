import numpy as np #алгебра
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
    def reul(self, x):
        return np.maximum(0, x)
    
    def softmax(self, x):
        #Вычитаем максмум для точных вычислений
        exp_x = np.exp(x - np.max(x, axis=1, keedims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        #принятие данных
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
    
#Наказание
    def backward(self, X, y, output, learning_rate):
        m = X.shape[0]
        
    



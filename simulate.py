from time import sleep
import numpy as np
import h5py
import tflearn
from tflearn import *
import tensorflow as tf

from redgo.board import Board, Color

batch_size = 128
n_classes = 19 * 19

network = input_data(shape=[None, 19, 19, 7], dtype=tf.float32)
network = conv_2d(network, 48, 3, activation='relu')
network = conv_2d(network, 32, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 64, 3, activation='relu')
network = max_pool_2d(network, 2)
network = fully_connected(network, 512, activation='relu')
network = fully_connected(network, n_classes, activation='softmax')
network = regression(network, optimizer='sgd',
                     loss='categorical_crossentropy',
                     learning_rate=0.05)

model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='./log', max_checkpoints=1)
model.load('./log-333000')

board = Board(size=19)
current_color = Color.white
while True:
    current_color = Color.white if current_color == Color.black else Color.black
    probs = board.get_features(current_color, None)[0]
    probs = np.reshape(probs, [1, 19, 19, 7])
    result = np.argmax(model.predict(probs)[0])
    move = board.decode_move(result)
    board.move(current_color, move)
    print(str(board))
    sleep(3)

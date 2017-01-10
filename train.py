import h5py
import tflearn
from tflearn import *
import tensorflow as tf

h5f = h5py.File('data.h5', 'r')
X = h5f['X']
Y = h5f['Y']
batch_size = 128
n_classes = 19 * 19
# Build network
network = input_data(shape=[None, 19, 19, 7], dtype=tf.float32)
network = conv_2d(network, 32, 3, activation='relu')
network = conv_2d(network, 32, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 64, 3, activation='relu')
network = max_pool_2d(network, 2)
network = fully_connected(network, 512, activation='relu')
network = dropout(network, 0.5)
network = fully_connected(network, n_classes, activation='softmax')
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

# Training
model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='./log', max_checkpoints=1)
model.fit(X, Y, n_epoch=100, shuffle=True, validation_set=0.1, snapshot_step=500,
          show_metric=True, batch_size=batch_size, run_id='redgo3')

h5f.close()

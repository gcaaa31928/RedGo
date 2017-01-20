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
network = input_data(shape=[None, 19, 19, 8], dtype=tf.float32)
network = conv_2d(network, 256, 7, activation='relu')
network = conv_2d(network, 256, 5, activation='relu')
network = conv_2d(network, 256, 5, activation='relu')
network = conv_2d(network, 256, 5, activation='relu')
network = conv_2d(network, 256, 3, activation='relu')
network = fully_connected(network, 512, activation='relu')
network = fully_connected(network, n_classes, activation='softmax')
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.05)

# Training
model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='./log', max_checkpoints=1)
model.fit(X, Y, n_epoch=100, shuffle=True, validation_set=0.1, snapshot_step=500,
          show_metric=True, batch_size=batch_size, run_id='redgo5')
model.save('save')
h5f.close()

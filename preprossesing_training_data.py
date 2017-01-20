from redgo.definitions import ROOT_DIR
from redgo.processor import Processor
import h5py, os
import numpy as np
from tflearn.data_utils import to_categorical

processor = Processor()
h5f = h5py.File('data.h5', 'w')
x_dataset = h5f.create_dataset('X', (0, 19, 19, 8), maxshape=(None, 19, 19, 8))
y_dataset = h5f.create_dataset('Y', (0, 19 * 19), maxshape=(None, 19 * 19))
zip_file = os.path.join(ROOT_DIR, './kgs/KGS-2016_12-19-1208-.zip')

for probs, sols in processor.get_total_samples_in_dir():
    probs = np.array(probs)
    sols = np.array(sols)
    sols = to_categorical(sols, nb_classes=19 * 19)
    x_dataset.resize(x_dataset.shape[0] + probs.shape[0], axis=0)
    y_dataset.resize(y_dataset.shape[0] + sols.shape[0], axis=0)
    x_dataset[-probs.shape[0]:] = probs
    y_dataset[-sols.shape[0]:] = sols

# probs, sols = processor.get_total_samples_in_zip(zip_file)
# probs = np.array(probs)
# sols = np.array(sols)
# sols = to_categorical(sols, nb_classes=19 * 19)
h5f.close()

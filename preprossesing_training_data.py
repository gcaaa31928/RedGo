from redgo.definitions import ROOT_DIR
from redgo.processor import Processor
import h5py, os
import numpy as np
from tflearn.data_utils import to_categorical

processor = Processor()
h5f = h5py.File('data.h5', 'w')
zip_file = os.path.join(ROOT_DIR, './kgs/KGS-2016_12-19-1208-.zip')
probs, sols = processor.get_total_samples_in_zip(zip_file)
probs = np.array(probs)
sols = np.array(sols)
print(sols.shape)
print(sols)
sols = to_categorical(sols, nb_classes=19*19)
print(sols.shape)
h5f.create_dataset('X', data=probs)
h5f.create_dataset('Y', data=sols)
h5f.close()
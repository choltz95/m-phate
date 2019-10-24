import matplotlib
matplotlib.use("Agg")  # noqa
import numpy as np
import matplotlib.pyplot as plt

import m_phate
import scprep
import os
import sys

from scipy.io import loadmat

###############
# Load data
###############
try:
    data_dir = os.path.expanduser(sys.argv[1])
except IndexError:
    data_dir = "./data"

try:
    dataset = sys.argv[2]
except IndexError:
    dataset = "mnist"

data = loadmat(os.path.join(
    data_dir, "generalization/{}_classifier_vanilla.mat".format(dataset)))
trace = data['trace']

###############
# Extract metadata
###############
n = trace.shape[0]
m = trace.shape[1]

neuron_ids = np.tile(np.arange(m), n)
layer_ids = np.tile(data['layer'], n)
epoch = np.repeat(np.arange(n), m)

digit_ids = np.repeat(np.arange(10), 10)
digit_activity = np.array([np.sum(np.abs(trace[:, :, digit_ids == digit]), axis=2)
                           for digit in np.unique(digit_ids)])
most_active_digit = np.argmax(digit_activity, axis=0).flatten()

###############
# Embed multislice graph
###############
m_phate_op = m_phate.M_PHATE()
m_phate_data = m_phate_op.fit_transform(trace)

###############
# Plot results
###############
plt.rc('font', size=14)
fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3, figsize=(18, 6), sharex='all', sharey='all')
scprep.plot.scatter2d(m_phate_data, c=epoch, ax=ax1, ticks=False,
                      title='Epoch', label_prefix="M-PHATE")
scprep.plot.scatter2d(m_phate_data, c=layer_ids, ax=ax2, title='Layer',
                      ticks=False, label_prefix="M-PHATE")
scprep.plot.scatter2d(m_phate_data, c=most_active_digit, ax=ax3,
                      title='Most active digit',
                      ticks=False, label_prefix="M-PHATE")
plt.tight_layout()
plt.savefig("{}_demonstration.png".format(dataset))

###############
# 3D plot
###############
m_phate_op.set_params(n_components=3)
m_phate_data = m_phate_op.transform()

scprep.plot.rotate_scatter3d(m_phate_data, c=most_active_digit,
                             title='Most active digit',
                             ticks=False, label_prefix="M-PHATE",
                             filename="{}_demonstration.gif".format(dataset))

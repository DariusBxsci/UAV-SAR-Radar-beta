# -*- coding: utf-8 -*-
"""
PulsON 440 message formats.
"""

import numpy as np
from collections import OrderedDict

# Radar internal configuration format; ordered dictionary order is the order 
# of the configuration fields; values are the data types; refer to API for more
# details
CONFIG_MSG_FORMAT = OrderedDict([
    ('node_id', np.dtype(np.uint32)), # Node ID
    ('scan_start', np.dtype(np.int32)), # Scan start time (ps)
    ('scan_stop', np.dtype(np.int32)), # Scan stop time (ps)
    ('scan_res', np.dtype(np.uint16)), # Scan resolution (bins); recommended value used
    ('pii', np.dtype(np.uint16)), # Pulse integration index
    ('seg_1_samp', np.dtype(np.uint16)), # Segment 1 samples; not used
    ('seg_2_samp', np.dtype(np.uint16)), # Segment 2 samples; not used
    ('seg_3_samp', np.dtype(np.uint16)), # Segment 3 samples; not used
    ('seg_4_samp', np.dtype(np.uint16)), # Segment 4 samples; not used
    ('seg_1_int', np.dtype(np.uint8)), # Segment 1 integration; not used
    ('seg_2_int', np.dtype(np.uint8)), # Segment 2 integration; not used
    ('seg_3_int', np.dtype(np.uint8)), # Segment 3 integration; not used
    ('seg_4_int', np.dtype(np.uint8)), # Segment 4 integration; not used
    ('ant_mode', np.dtype(np.uint8)), # Antenna mode; recommended value used
    ('tx_gain_ind', np.dtype(np.uint8)), # Transmit gain index
    ('code_channel', np.dtype(np.uint8)), # Code channel
    ('persist_flag', np.dtype(np.uint8))]) # Persist flag
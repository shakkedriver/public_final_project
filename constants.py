FRAME_RATE = 30
BUFFER_SIZE = 10000
FRAME_SHAPE = (400, 300)  # (x, y)
FRAME_SIZE = (FRAME_SHAPE[0] * FRAME_SHAPE[1])

DELTA_BOUND_CIRCULAR = 0.03  # z_ratio in [OPTIMAL_Z_RATIO-delta_bound_circular, OPTIMAL_Z_RATIO+delta_bound_circular] circular_tracker
DELTA_BOUND_TRACKER = 0.09  # z_ratio not in [OPTIMAL_Z_RATIO-delta_bound_tracker, OPTIMAL_Z_RATIO+delta_bound_tracker] tracker

OPTIMAL_Z_RATIO = 0.09 #0.13 before

SIDE_MOTION = 40
SEEK_YAW = 10 # the speed in which the drone will turn when a tracked person left the frame
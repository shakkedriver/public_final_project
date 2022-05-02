FRAME_RATE = 30
FRAME_SHAPE = (400, 300)
FRAME_SIZE = (FRAME_SHAPE[0] * FRAME_SHAPE[1])

DELTA_BOUND_CIRCULAR = 0.01  # z_ratio in [OPTIMAL_Z_RATIO-delta_bound_circular, OPTIMAL_Z_RATIO+delta_bound_circular] circular_tracker
DELTA_BOUND_TRACKER = 0.05  # z_ratio not in [OPTIMAL_Z_RATIO-delta_bound_tracker, OPTIMAL_Z_RATIO+delta_bound_tracker] tracker

OPTIMAL_Z_RATIO = 0.13
SIDE_MOTION = 40

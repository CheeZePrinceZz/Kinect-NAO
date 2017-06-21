import cmath
import kinecthandler
import joints
import numpy as np
import utils


def get_robot_world(kinect_pos):
    hip_right = kinect_pos[kinecthandler.joints_map[joints.HIP_RIGHT]]
    hip_left = kinect_pos[kinecthandler.joints_map[joints.HIP_LEFT]]
    spine_shoulder = kinect_pos[kinecthandler.joints_map[joints.SPINE_SHOULDER]]
    hip_vector = utils.get_vector(hip_right, hip_left)
    spine_shoulder_to_hip = utils.get_vector(hip_right, spine_shoulder)
    z = utils.normalized_cross(hip_vector, spine_shoulder_to_hip)
    x = utils.normalize(hip_vector)
    y = np.cross(z, x)
    z_0 = np.array([0, 0, 1])
    y_0 = np.array([0, 1, 0])
    x_0 = np.array([1, 0, 0])

    x1 = utils.normalized_dot(x, x_0)
    x2 = utils.normalized_dot(x, y_0)
    x3 = utils.normalized_dot(x, z_0)
    y1 = utils.normalized_dot(y, x_0)
    y2 = utils.normalized_dot(y, y_0)
    y3 = utils.normalized_dot(y, z_0)
    z1 = utils.normalized_dot(z, x_0)
    z2 = utils.normalized_dot(z, y_0)
    z3 = utils.normalized_dot(z, z_0)
    A = np.matrix([[x1, x2, x3], [y1, y2, y3], [z1, z2, z3]])
    return [A, np.array([x, y, z])]


def get_right_elbow_roll(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_RIGHT]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_RIGHT]]
    wrist = kinect_pos[kinecthandler.joints_map[joints.WRIST_RIGHT]]
    shoulder_elbow = utils.get_vector(elbow, shoulder, transform=world[0])
    elbow_wrist = utils.get_vector(wrist, elbow, transform=world[0])
    res = np.arccos(utils.normalized_dot(shoulder_elbow, elbow_wrist))
    res = max(res, 0.069)
    res = min(res, 1.483)
    return res


def get_left_elbow_roll(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_LEFT]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_LEFT]]
    wrist = kinect_pos[kinecthandler.joints_map[joints.WRIST_LEFT]]
    shoulder_elbow = utils.get_vector(elbow, shoulder, transform=world[0])
    elbow_wrist = utils.get_vector(wrist, elbow, transform=world[0])
    res = -np.arccos(utils.normalized_dot(shoulder_elbow, elbow_wrist))
    res = min(res, -0.069)
    res = max(res, -1.483)
    return res


def get_right_shoulder_pitch(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_RIGHT]]
    spine_shoulder = kinect_pos[kinecthandler.joints_map[joints.SPINE_SHOULDER]]
    spine_mid = kinect_pos[kinecthandler.joints_map[joints.SPINE_MID]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_RIGHT]]
    finger_tip = kinect_pos[kinecthandler.joints_map[joints.HAND_TIP_RIGHT]]
    head = kinect_pos[kinecthandler.joints_map[joints.HEAD]]
    wrist = kinect_pos[kinecthandler.joints_map[joints.WRIST_RIGHT]]

    shoulder_elbow = utils.get_vector(elbow, shoulder, transform=world[0])
    shoulder_elbow = utils.normalize(shoulder_elbow)
    shoulder_spin_shoulder = utils.get_vector(spine_shoulder, shoulder, transform=world[0])
    shoulder_spin_shoulder = utils.normalize(shoulder_spin_shoulder)
    modified_spine_mid = [shoulder[0], spine_mid[1], spine_mid[2]]
    # spine_shoulder_spine_mid = utils.get_vector(modified_spine_mid, spine_shoulder, transform=world[0])
    spine_shoulder_spine_mid = utils.get_vector(modified_spine_mid, shoulder, transform=world[0])
    spine_shoulder_spine_mid = utils.normalize(spine_shoulder_spine_mid)
    cross = np.cross(spine_shoulder_spine_mid, shoulder_spin_shoulder)
    cross = np.reshape(utils.normalize(cross), (3, 1))
    # Only z and y needed
    cross = [cross[2], cross[1]]
    cross = utils.normalize(cross)
    # Only z and y needed
    shoulder_elbow = [shoulder_elbow[2], shoulder_elbow[1]]
    shoulder_elbow = utils.normalize(shoulder_elbow)
    sign = 1
    # If the elbow is higher than the shoulder
    if shoulder_elbow[1] < 0 or finger_tip[1] > head[1] or wrist[1] > shoulder[1]:
        sign = -1
    res = sign * np.arccos(np.dot(shoulder_elbow, cross)[0])
    res = max(res, -1.57)
    res = min(res, 1.57)
    return res


def get_left_shoulder_pitch(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_LEFT]]
    spine_shoulder = kinect_pos[kinecthandler.joints_map[joints.SPINE_SHOULDER]]
    spine_mid = kinect_pos[kinecthandler.joints_map[joints.SPINE_MID]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_LEFT]]
    finger_tip = kinect_pos[kinecthandler.joints_map[joints.HAND_TIP_LEFT]]
    head = kinect_pos[kinecthandler.joints_map[joints.HEAD]]
    wrist = kinect_pos[kinecthandler.joints_map[joints.WRIST_LEFT]]

    shoulder_elbow = utils.get_vector(elbow, shoulder, transform=world[0])
    shoulder_elbow = utils.normalize(shoulder_elbow)
    shoulder_spin_shoulder = utils.get_vector(spine_shoulder, shoulder, transform=world[0])
    shoulder_spin_shoulder = utils.normalize(shoulder_spin_shoulder)
    modified_spine_mid = [shoulder[0], spine_mid[1], spine_mid[2]]
    # spine_shoulder_spine_mid = utils.get_vector(modified_spine_mid, spine_shoulder, transform=world[0])
    spine_shoulder_spine_mid = utils.get_vector(modified_spine_mid, shoulder, transform=world[0])
    spine_shoulder_spine_mid = utils.normalize(spine_shoulder_spine_mid)
    cross = np.cross(shoulder_spin_shoulder, spine_shoulder_spine_mid)
    cross = np.reshape(utils.normalize(cross), (3, 1))
    # Only z and y needed
    cross = [cross[2], cross[1]]
    cross = utils.normalize(cross)
    # Only z and y needed
    shoulder_elbow = [shoulder_elbow[2], shoulder_elbow[1]]
    shoulder_elbow = utils.normalize(shoulder_elbow)
    sign = 1
    # If the elbow is higher than the shoulder
    if shoulder_elbow[1] < 0 or finger_tip[1] > head[1] or wrist[1] > shoulder[1]:
        sign = -1
    res = sign * np.arccos(np.dot(shoulder_elbow, cross)[0])
    res = max(res, -1.57)
    res = min(res, 1.57)
    return res


def get_right_shoulder_roll(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    cross = np.cross(world[1][1], world[1][2])
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_RIGHT]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_RIGHT]]
    shoulder_elbow = utils.get_vector(elbow, shoulder, transform=world[0])
    res = -1 * ((np.pi / 2.) - np.arccos(utils.normalized_dot(shoulder_elbow, cross)))
    res = min(res, 0.085)
    res = max(res, -1.13)
    return res


def get_left_shoulder_roll(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    cross = np.cross(world[1][1], world[1][2])
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_LEFT]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_LEFT]]
    shoulder_elbow = utils.get_vector(elbow, shoulder, transform=world[0])
    res = -1 * ((np.pi / 2.) - np.arccos(utils.normalized_dot(shoulder_elbow, cross)))
    res = max(res, -0.085)
    res = min(res, 1.13)
    return res


def get_right_elbow_yaw(kinect_pos, shoulder_roll=None, shoulder_pitch=None, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    if shoulder_roll is None:
        shoulder_roll = get_right_shoulder_roll(kinect_pos, world)
    if shoulder_pitch is None:
        shoulder_pitch = get_right_shoulder_pitch(kinect_pos, world)
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_RIGHT]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_RIGHT]]
    wrist = kinect_pos[kinecthandler.joints_map[joints.WRIST_RIGHT]]
    pitch_matrix = np.matrix([[1, 0, 0],
                              [0, np.cos(shoulder_pitch), -np.sin(shoulder_pitch)],
                              [0, np.sin(shoulder_pitch), np.cos(shoulder_pitch)]])
    roll_matrix = np.matrix([[np.cos(shoulder_roll), 0, np.sin(shoulder_roll)],
                             [0, 1, 0],
                             [-np.sin(shoulder_roll), 0, np.cos(shoulder_roll)]])
    transform = world[0] * pitch_matrix * roll_matrix
    elbow_shoulder = utils.get_vector(shoulder, elbow, transform=transform)
    elbow_shoulder = utils.normalize(elbow_shoulder)
    modified_elbow = [elbow[0], elbow[1] + 2, elbow[2]]
    elbow_vertical = utils.get_vector(modified_elbow, elbow, transform=transform)
    elbow_wrist = utils.get_vector(wrist, elbow, transform=transform)
    elbow_wrist = utils.normalize([elbow_wrist[0], elbow_wrist[1]])
    cross_arm = np.cross(elbow_shoulder, elbow_vertical)
    cross_arm = utils.normalize([cross_arm[0], cross_arm[1]])
    # cross_arm = np.array([cross_arm[0], cross_arm[1]])
    # elbow_wrist = np.array([elbow_wrist[0], elbow_wrist[1]])
    sign = 1
    if elbow_wrist[1] > 0:
        sign = -1
    dot = utils.normalized_dot(elbow_wrist, cross_arm)
    return sign * (np.arccos(dot))


def get_left_elbow_yaw(kinect_pos, shoulder_roll=None, shoulder_pitch=None, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    if shoulder_roll is None:
        shoulder_roll = get_left_shoulder_roll(kinect_pos, world)
    if shoulder_pitch is None:
        shoulder_pitch = get_left_shoulder_pitch(kinect_pos, world)
    shoulder = kinect_pos[kinecthandler.joints_map[joints.SHOULDER_LEFT]]
    elbow = kinect_pos[kinecthandler.joints_map[joints.ELBOW_LEFT]]
    wrist = kinect_pos[kinecthandler.joints_map[joints.WRIST_LEFT]]
    pitch_matrix = np.matrix([[1, 0, 0],
                              [0, np.cos(shoulder_pitch), -np.sin(shoulder_pitch)],
                              [0, np.sin(shoulder_pitch), np.cos(shoulder_pitch)]])
    roll_matrix = np.matrix([[np.cos(shoulder_roll), 0, np.sin(shoulder_roll)],
                             [0, 1, 0],
                             [-np.sin(shoulder_roll), 0, np.cos(shoulder_roll)]])
    transform = world[0] * pitch_matrix * roll_matrix
    elbow_shoulder = utils.get_vector(shoulder, elbow, transform=transform)
    elbow_shoulder = utils.normalize(elbow_shoulder)
    modified_elbow = [elbow[0], elbow[1] + 2, elbow[2]]
    elbow_vertical = utils.get_vector(modified_elbow, elbow, transform=transform)
    elbow_wrist = utils.get_vector(wrist, elbow, transform=transform)
    elbow_wrist = utils.normalize([elbow_wrist[0], elbow_wrist[1]])
    cross_arm = np.cross(elbow_vertical, elbow_shoulder)
    cross_arm = utils.normalize([cross_arm[0], cross_arm[1]])
    # cross_arm = np.array([cross_arm[0], cross_arm[1]])
    # elbow_wrist = np.array([elbow_wrist[0], elbow_wrist[1]])
    sign = -1
    if elbow_wrist[1] > 0:
        sign = 1
    dot = utils.normalized_dot(elbow_wrist, cross_arm)
    return sign * (np.arccos(dot))


def get_right_wrist_yaw(kinect_rot, elbow_yaw):
    wrist_yaw = -kinect_rot[kinecthandler.joints_map[joints.HAND_RIGHT]][2]
    wrist_yaw += elbow_yaw - 80
    wrist_yaw = min(wrist_yaw, 100)
    wrist_yaw = max(wrist_yaw, -100)
    return wrist_yaw


def get_left_wrist_yaw(kinect_rot, elbow_yaw):
    wrist_yaw = -kinect_rot[kinecthandler.joints_map[joints.HAND_LEFT]][2]
    wrist_yaw -= elbow_yaw + 80
    wrist_yaw = min(wrist_yaw, 100)
    wrist_yaw = max(wrist_yaw, -100)
    return wrist_yaw


def get_right_arm(kinect_pos, kinect_rot, must_filter=True):
    # Get the conversion matrix and the axes in the "robot world"
    world = get_robot_world(kinect_pos)
    # Compute the angle for every part of the arm
    shoulder_roll = utils.valid_angle(get_right_shoulder_roll(kinect_pos, world=world) * 180 / np.pi)
    shoulder_pitch = utils.valid_angle(get_right_shoulder_pitch(kinect_pos, world=world) * 180 / np.pi)
    elbow_roll = utils.valid_angle(get_right_elbow_roll(kinect_pos, world=world) * 180 / np.pi)
    elbow_yaw = utils.valid_angle(get_right_elbow_yaw(kinect_pos,
                                    shoulder_pitch=shoulder_pitch * np.pi / 180,
                                    shoulder_roll=shoulder_roll * np.pi / 180,
                                    world=world) * 180 / np.pi)
    # Is the elbow angle enough to bend it on the robot ?
    if elbow_roll > 50:
        elbow_yaw += shoulder_pitch
    # Else, flat arm
    else:
        elbow_yaw = 80
        elbow_roll = 7.5
    elbow_yaw = max(-110, elbow_yaw)
    elbow_yaw = min(110, elbow_yaw)
    # Compute Wrist yaw given the other angles + rotation list
    wrist_yaw = get_right_wrist_yaw(kinect_rot, elbow_yaw)
    if must_filter:
        shoulder_roll = utils.value_filter("r_s_roll", shoulder_roll)
        shoulder_pitch = utils.value_filter("r_s_pitch", shoulder_pitch)
        elbow_roll = utils.value_filter("r_e_roll", elbow_roll)
        elbow_yaw = utils.value_filter("r_e_yaw", elbow_yaw)
        wrist_yaw = utils.value_filter("r_w_yaw", wrist_yaw)
    return [shoulder_roll, shoulder_pitch, elbow_roll, elbow_yaw, wrist_yaw]


def get_left_arm(kinect_pos, kinect_rot, must_filter=True):
    # Get the conversion matrix and the axes in the "robot world"
    world = get_robot_world(kinect_pos)
    # Compute the angle for every part of the arm
    shoulder_roll = utils.valid_angle(get_left_shoulder_roll(kinect_pos, world=world) * 180 / np.pi)
    shoulder_pitch = utils.valid_angle(get_left_shoulder_pitch(kinect_pos, world=world) * 180 / np.pi)
    elbow_roll = utils.valid_angle(get_left_elbow_roll(kinect_pos, world=world) * 180 / np.pi)
    elbow_yaw = utils.valid_angle(get_left_elbow_yaw(kinect_pos,
                                   shoulder_pitch=shoulder_pitch * np.pi / 180,
                                   shoulder_roll=shoulder_roll * np.pi / 180,
                                   world=world) * 180 / np.pi)
    # Is the elbow angle enough to bend it on the robot ?
    if elbow_roll < -50:
        elbow_yaw -= shoulder_pitch + 15
    # Else, flat arm
    else:
        elbow_yaw = -80
        elbow_roll = -7.5
    elbow_yaw = max(-110, elbow_yaw)
    elbow_yaw = min(110, elbow_yaw)
    # Compute Wrist yaw given the other angles + rotation list
    wrist_yaw = get_left_wrist_yaw(kinect_rot, elbow_yaw)
    if must_filter:
        shoulder_roll = utils.value_filter("l_s_roll", shoulder_roll)
        shoulder_pitch = utils.value_filter("l_s_pitch", shoulder_pitch)
        elbow_roll = utils.value_filter("l_e_roll", elbow_roll)
        elbow_yaw = utils.value_filter("l_e_yaw", elbow_yaw)
        wrist_yaw = utils.value_filter("l_w_yaw", wrist_yaw)
    return [shoulder_roll, shoulder_pitch, elbow_roll, elbow_yaw, wrist_yaw]


def get_head_pitch(kinect_pos, world=None, must_filter=True):
    if world is None:
        world = get_robot_world(kinect_pos)
    head = kinect_pos[kinecthandler.joints_map[joints.HEAD]]
    neck = kinect_pos[kinecthandler.joints_map[joints.NECK]]
    modified_neck = [neck[0], neck[1] - 1, neck[2]]
    neck_head = utils.get_vector(head, neck, transform=world[0])
    modified_neck_head = utils.get_vector(head, modified_neck, transform=world[0])
    res = np.arccos(utils.normalized_dot(neck_head, modified_neck_head))
    sign = 1
    if head[2] > neck[2]:
        sign = -1
    res *= sign
    res = max(res, -0.66)
    res = min(res, 0.5)
    if must_filter:
        res = utils.value_filter("h_pitch", res)
    return res


def get_hand_state(hand_value):
    if hand_value == 0 or hand_value == 1 or hand_value == 3:
        return 0.00
    else:
        return 0.99


def get_head(kinect_pos):
    world = get_robot_world(kinect_pos)
    pitch = get_head_pitch(kinect_pos, world)*180./np.pi
    return pitch


def get_hands(hands):
    #right_hand = get_hand_state(hands[0])
    right_hand = utils.smooth_right_hand(hands[0])
    #left_hand = get_hand_state(hands[1])
    left_hand = utils.smooth_left_hand(hands[1])
    return [right_hand, left_hand]


def get_right_knee_pitch(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    hip = kinect_pos[kinecthandler.joints_map[joints.HIP_RIGHT]]
    knee = kinect_pos[kinecthandler.joints_map[joints.KNEE_RIGHT]]
    ankle = kinect_pos[kinecthandler.joints_map[joints.ANKLE_RIGHT]]
    hip_knee = utils.get_vector(knee, hip, transform=world[0])
    knee_ankle = utils.get_vector(ankle, knee, transform=world[0])
    res = np.arccos(utils.normalized_dot(hip_knee, knee_ankle))
    res = min(np.pi/2., res)
    return res


def get_left_knee_pitch(kinect_pos, world=None):
    if world is None:
        world = get_robot_world(kinect_pos)
    hip = kinect_pos[kinecthandler.joints_map[joints.HIP_LEFT]]
    knee = kinect_pos[kinecthandler.joints_map[joints.KNEE_LEFT]]
    ankle = kinect_pos[kinecthandler.joints_map[joints.ANKLE_LEFT]]
    hip_knee = utils.get_vector(knee, hip, transform=world[0])
    knee_ankle = utils.get_vector(ankle, knee, transform=world[0])
    res = np.arccos(utils.normalized_dot(hip_knee, knee_ankle))
    res = min(np.pi/2., res)
    return res


def get_right_ankle_pitch(kinect_pos, world=None):
    # TODO : Test
    if world is None:
        world = get_robot_world(kinect_pos)
    knee = kinect_pos[kinecthandler.joints_map[joints.KNEE_RIGHT]]
    ankle = kinect_pos[kinecthandler.joints_map[joints.ANKLE_RIGHT]]
    foot = kinect_pos[kinecthandler.joints_map[joints.FOOT_RIGHT]]
    ankle_foot = utils.get_vector(foot, ankle, transform=world[0])
    ankle_knee = utils.get_vector(knee, ankle, transform=world[0])
    res = -1*(np.pi/2 - np.arccos(utils.normalized_dot(ankle_foot, ankle_knee)))
    res = max(-np.pi/4., res)
    res = min(0, res)
    return res


def get_left_ankle_pitch(kinect_pos, world=None):
    # TODO : Test
    if world is None:
        world = get_robot_world(kinect_pos)
    knee = kinect_pos[kinecthandler.joints_map[joints.KNEE_LEFT]]
    ankle = kinect_pos[kinecthandler.joints_map[joints.ANKLE_LEFT]]
    foot = kinect_pos[kinecthandler.joints_map[joints.FOOT_LEFT]]
    ankle_foot = utils.get_vector(foot, ankle, transform=world[0])
    ankle_knee = utils.get_vector(knee, ankle, transform=world[0])
    res = -1*(np.pi/2 - np.arccos(utils.normalized_dot(ankle_foot, ankle_knee)))
    res = max(-np.pi/4., res)
    res = min(0, res)
    return res


def get_hip_pitch(kinect_pos, ankle_pitch=None, world=None):
    # TODO : Test
    if world is None:
        world = get_robot_world(kinect_pos)
    if ankle_pitch is None:
        ankle_pitch = get_right_ankle_pitch(kinect_pos, world=world)
    spine_base = kinect_pos[kinecthandler.joints_map[joints.SPINE_BASE]]
    spine_shoulder = kinect_pos[kinecthandler.joints_map[joints.SPINE_SHOULDER]]
    modified_spine_base = [spine_base[0], spine_base[1] - 1, spine_base[2]]
    spine = utils.get_vector(spine_shoulder, spine_base, transform=world[0])
    vertical_spine = utils.get_vector(spine_base, modified_spine_base, transform=world[0])
    angle = -np.arccos(utils.normalized_dot(vertical_spine, spine))
    res = angle + ankle_pitch
    res = min(res, 0.34)
    res = max(res, -1.39)
    return res


def get_right_leg(kinect_pos):
    world = get_robot_world(kinect_pos)
    ankle_pitch = get_right_ankle_pitch(kinect_pos, world) * 180./np.pi
    knee_pitch = get_right_knee_pitch(kinect_pos, world) * 180./np.pi
    hip_pitch = get_hip_pitch(kinect_pos, ankle_pitch, world) * 180./np.pi
    return [ankle_pitch, knee_pitch, hip_pitch]


def get_left_leg(kinect_pos):
    world = get_robot_world(kinect_pos)
    ankle_pitch = get_left_ankle_pitch(kinect_pos, world) * 180./np.pi
    knee_pitch = get_left_knee_pitch(kinect_pos, world) * 180./np.pi
    hip_pitch = get_hip_pitch(kinect_pos, ankle_pitch, world) * 180./np.pi
    return [ankle_pitch, knee_pitch, hip_pitch]

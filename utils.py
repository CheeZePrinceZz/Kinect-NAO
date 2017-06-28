import numpy as np
from math import *
from collections import deque


#
# All copyright to Connor Johnson
# Copied from http://connor-johnson.com/2014/02/01/smoothing-with-exponentially-weighted-moving-averages/
#
def holt_winters_second_order_ewma(x, span, beta):
    N = len(x)
    alpha = 2.0 / ( 1 + span )
    s = np.zeros((N, ))
    b = np.zeros((N, ))
    s[0] = x[0]
    for i in range( 1, N ):
        s[i] = alpha * x[i] + (1 - alpha)*(s[i-1] + b[i-1])
        b[i] = beta * (s[i] - s[i-1]) + (1 - beta) * b[i-1]
    return s


last_movements = {"r_s_pitch": 0,
                  "r_s_roll" : 0,
                  "r_e_roll" : 0,
                  "r_e_yaw" : 0,
                  "r_w_yaw" : 0,
                  "l_s_pitch": 0,
                  "l_s_roll": 0,
                  "l_e_roll": 0,
                  "l_e_yaw": 0,
                  "l_w_yaw": 0,
                  "h_pitch": 0,
                  "h_yaw": 0,
                  }

FILTER_SPAN = 4
FILTER_BETA = 0.45
FILTER_SIZE = 25

smoothing_dict = {"r_s_pitch": deque(),
                  "r_s_roll": deque(),
                  "r_e_roll": deque(),
                  "r_e_yaw": deque(),
                  "r_w_yaw": deque(),
                  "l_s_pitch": deque(),
                  "l_s_roll": deque(),
                  "l_e_roll": deque(),
                  "l_e_yaw": deque(),
                  "l_w_yaw": deque(),
                  "h_pitch": deque(),
                  "h_yaw": deque(),
                  }

right_hand = None
left_hand = None


# def value_filter(move, res):
#     if len(smoothing_dict[move]) == FILTER_SIZE:
#         smoothing_dict[move].popleft()
#     smoothing_dict[move].append(res)
#     res = holt_winters_second_order_ewma(smoothing_dict[move], FILTER_SPAN, FILTER_BETA)[-1]
#     if abs(res-last_movements[move]) < 7:
#         res = last_movements[move]
#     else:
#         last_movements[move] = res
#     return res


def value_filter(move, res):
    if len(smoothing_dict[move]) == FILTER_SIZE:
        smoothing_dict[move].popleft()
    smoothing_dict[move].append(res)
    res = holt_winters_second_order_ewma(smoothing_dict[move], FILTER_SPAN, FILTER_BETA)[-1]
    if abs(res-last_movements[move]) < 7:
        res = last_movements[move]
    else:
        last_movements[move] = res
    smoothing_dict[move].pop()
    smoothing_dict[move].append(res)
    return res


def smooth_right_hand(hand_value):
    threshold = 10
    global  right_hand
    if right_hand is None:
        if hand_value == 1 or hand_value == 3:
            #hand_value == 0 or
            right_hand = (0.00, threshold)
        else:
            right_hand = (0.99, threshold)
    else:
        if hand_value == 0 or hand_value == 1:
            return right_hand[0]
        else:
            if hand_value == 3:
                hand_value = 0.00
            else:
                hand_value = 0.99
            if abs(right_hand[0] - hand_value) < 0.01:
                right_hand = (hand_value, threshold)
            else:
                if right_hand[1] != 0:
                    right_hand = (right_hand[0], right_hand[1]-1)
                else:
                    right_hand = (hand_value, threshold)
    return right_hand[0]


def smooth_left_hand(hand_value):
    threshold = 10
    global left_hand
    if left_hand is None:
        if hand_value == 1 or hand_value == 3:
            #hand_value == 0 or
            left_hand = (0.00, threshold)
        else:
            left_hand = (0.99, threshold)
    else:
        if hand_value == 0 or hand_value == 1:
            return left_hand[0]
        else:
            if hand_value == 3:
                hand_value = 0.00
            else:
                hand_value = 0.99
            if abs(left_hand[0] - hand_value) < 0.01:
                left_hand = (hand_value, threshold)
            else:
                if left_hand[1] != 0:
                    left_hand = (left_hand[0], left_hand[1]-1)
                else:
                    left_hand = (hand_value, threshold)
    return left_hand[0]


def quat_to_axisangle(q):
    angle = 2.0*acos(q[0])
    x = q[1]/(sqrt(1-(q[0]*q[0])))
    y = q[2]/(sqrt(1-(q[0]*q[0])))
    z = q[3]/(sqrt(1-(q[0]*q[0])))
    return [angle/pi*180.0, x, y, z]


def cart_to_spher(vector):
    r = np.linalg.norm(vector)
    unit = map(lambda x: x/r, vector)
    theta = acos(unit[2])/pi*180.
    phi = atan2(unit[1], unit[0])/pi*180.
    return [r, theta, phi]


def valid_angle(value):
    if value > 180:
        value = -180 + (value - 180)
        return valid_angle(value)
    if value < -180:
        value = 180 + (value + 180)
        return valid_angle(value)
    return value


# coord_tab: tab of coordinates to rotate, given the angles tab
# angles : the angles to rotate (tab must have the same length than order)
# order: the rotation order, examples : xyx. or xy, etc...
# return a tab with all the coord rotated
def rotate(coord_tab, angles, order="xyz"):
    m = []
    for i in range(len(order)):
        angle = angles[i]
        if order[i] == 'x':
            m.append(np.matrix([[1, 0, 0], [0, cos(angle), -sin(angle)], [0, sin(angle), cos(angle)]]))
        elif order[i] == 'y':
            m.append(np.matrix([[cos(angle), 0, sin(angle)], [0, 1, 0], [-sin(angle), 0, cos(angle)]]))
        elif order[i] == 'z':
            m.append(np.matrix([[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]]))
    matrix = reduce(lambda a, b: a * b, m)
    new_coord_tab = []
    for coord in coord_tab:
        [x, y, z] = coord
        vector = np.matrix([[x], [y], [z]])
        [x, y, z] = (matrix*vector).getA()
        new_coord_tab.append([x[0], y[0], z[0]])
    return new_coord_tab


def get_vector(final, start, transform=None):
    x = final[0]-start[0]
    y = final[1]-start[1]
    z = final[2]-start[2]
    if transform is None:
        return [x, y, z]
    else:
        temp = transform*np.matrix([[x], [y], [z]])
        return np.transpose(temp)[0].getA()[0]


def normalized_cross(vect1, vect2):
    cross = np.cross(vect1, vect2)
    return normalize(cross)


def normalized_dot(vect1, vect2):
    vect1 = normalize(vect1)
    vect2 = normalize(vect2)
    dot = np.dot(vect1, vect2)
    return dot


def normalize(vect):
    norm = np.linalg.norm(vect)
    return map(lambda x: x/norm, vect)


def angle_between(vector1, vector2):
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    vector1 = map(lambda x: x/norm1, vector1)
    vector2 = map(lambda x: x/norm2, vector2)
    return acos(vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2])*180./pi

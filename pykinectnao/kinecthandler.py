from time import sleep

__author__ = 'Angeall'
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import joints
from math import *

NO_DATA = -1

joints_map = {joints.SPINE_BASE: 0,
              joints.SPINE_MID: 1,
              joints.NECK: 2,
              joints.HEAD: 3,
              joints.SHOULDER_LEFT: 4,
              joints.ELBOW_LEFT: 5,
              joints.WRIST_LEFT: 6,
              joints.HAND_LEFT: 7,
              joints.SHOULDER_RIGHT: 8,
              joints.ELBOW_RIGHT: 9,
              joints.WRIST_RIGHT: 10,
              joints.HAND_RIGHT: 11,
              joints.HIP_LEFT: 12,
              joints.KNEE_LEFT: 13,
              joints.ANKLE_LEFT: 14,
              joints.FOOT_LEFT: 15,
              joints.HIP_RIGHT: 16,
              joints.KNEE_RIGHT: 17,
              joints.ANKLE_RIGHT: 18,
              joints.FOOT_RIGHT: 19,
              joints.SPINE_SHOULDER: 20,
              joints.HAND_TIP_LEFT: 21,
              joints.THUMB_LEFT: 22,
              joints.HAND_TIP_RIGHT: 23,
              joints.THUMB_RIGHT: 24, }

bones_map = {(joints.SPINE_BASE, joints.SPINE_MID): 0,
             (joints.SPINE_MID, joints.SPINE_SHOULDER): 1,
             (joints.SPINE_SHOULDER, joints.NECK): 2,
             (joints.NECK, joints.HEAD): 3,
             (joints.SPINE_SHOULDER, joints.SHOULDER_LEFT): 4,
             (joints.SHOULDER_LEFT, joints.ELBOW_LEFT): 5,
             (joints.ELBOW_LEFT, joints.WRIST_LEFT): 6,
             (joints.WRIST_LEFT, joints.HAND_LEFT): 7,
             (joints.HAND_LEFT, joints.HAND_TIP_LEFT): 8,
             (joints.WRIST_LEFT, joints.THUMB_LEFT): 9,
             (joints.SPINE_SHOULDER, joints.SHOULDER_RIGHT): 10,
             (joints.SHOULDER_RIGHT, joints.ELBOW_RIGHT): 11,
             (joints.ELBOW_RIGHT, joints.WRIST_RIGHT): 12,
             (joints.WRIST_RIGHT, joints.HAND_RIGHT): 13,
             (joints.HAND_RIGHT, joints.HAND_TIP_RIGHT): 14,
             (joints.WRIST_RIGHT, joints.THUMB_RIGHT): 15,
             (joints.SPINE_BASE, joints.HIP_LEFT): 16,
             (joints.HIP_LEFT, joints.KNEE_LEFT): 17,
             (joints.KNEE_LEFT, joints.ANKLE_LEFT): 18,
             (joints.ANKLE_LEFT, joints.FOOT_LEFT): 19,
             (joints.SPINE_BASE, joints.HIP_RIGHT): 20,
             (joints.HIP_RIGHT, joints.KNEE_RIGHT): 21,
             (joints.KNEE_RIGHT, joints.ANKLE_RIGHT): 22,
             (joints.ANKLE_RIGHT, joints.FOOT_RIGHT): 23}

last_positions = []


class KinectHandler():
    def __init__(self):
        self.device = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)
                                                    #| PyKinectV2.FrameSourceTypes_Color)
        self.bodies = None
        self.active_bodies_indices = []
        self.positions = None
        self.orientations = None
        self.positions_pattern_list = []
        for i in range(len(joints_map)):
            self.positions_pattern_list.append(None)

    def close(self):
        self.device.close()

    # Get a list made of [positions (list of [x, y, z]), orientation (list of [Roll, Pitch, Yaw])]
    def get_movement(self, nb_of_body=1):
        if self.device.has_new_body_frame():
            self.bodies = self.device.get_last_body_frame()
        if self.bodies is not None:
            for index in self.active_bodies_indices:
                if not self.bodies.bodies[index].is_tracked:
                    self.active_bodies_indices.remove(index)
                    sleep(3)
            # Search after bodies Kinect might have detected
            for i in range(0, self.device.max_body_count):
                body = self.bodies.bodies[i]
                if not body.is_tracked:
                    continue
                else:
                    if i not in self.active_bodies_indices:
                        self.active_bodies_indices.append(i)
            if len(self.active_bodies_indices) == 0:
                return NO_DATA
            res = []
            for j in range(nb_of_body):
                body = self.bodies.bodies[self.active_bodies_indices[j]]
                self.positions = body.joints
                self.orientations = body.joint_orientations
                hands = [body.hand_right_state, body.hand_left_state]
                res.append([self.convert_positions(), self.convert_orientation(), hands])
            return res
        else:
            return NO_DATA

    # Get the [Roll, Pitch, Yaw] from the Kinect orientation quaternion
    def convert_orientation(self):
        orientations = []
        for i in range(25):
            orientations.append(None)
        for joint in joints_map.keys():
            tab = [None, None, None]
            index = joints_map[joint]
            x = self.orientations[index].Orientation.x
            y = self.orientations[index].Orientation.y
            z = self.orientations[index].Orientation.z
            w = self.orientations[index].Orientation.w
            quaternion = [w, x, y, z]
            tab[0] = self.compute_roll(quaternion)
            tab[1] = self.compute_pitch(quaternion)
            tab[2] = self.compute_yaw(quaternion)
            orientations[joints_map[joint]] = tab
        return orientations

    # Get the Yaw from a rotation quaternion
    @staticmethod
    def compute_roll(quaternion):
        [w, x, y, z] = quaternion
        roll = asin(2 * ((w * y) - (x * z))) / pi * 180.0
        return roll

    # Get the Pitch from a rotation quaternion
    @staticmethod
    def compute_pitch(quaternion):
        [w, x, y, z] = quaternion
        pitch = atan2(2 * ((y * z) + (w * x)), 1-2*((x*x) + (y*y))) / pi * 180.0
        return pitch

    # Get the Roll from a rotation quaternion
    @staticmethod
    def compute_yaw(quaternion):
        [w, x, y, z] = quaternion
        yaw = atan2(2 * ((x * y) + (w * z)), 1-2*((y*y)+(z*z))) / pi * 180.0
        return yaw

    # Get an array [x, y, z] from the Kinect Position object
    def convert_positions(self):
        positions = self.positions_pattern_list[:]
        for joint in joints_map.keys():
            x = self.positions[joints_map[joint]].Position.x
            y = self.positions[joints_map[joint]].Position.y
            z = self.positions[joints_map[joint]].Position.z
            if joint == joints.ELBOW_RIGHT:
                shoulder_z = self.positions[joints_map[joints.SHOULDER_RIGHT]].Position.z
                if z > shoulder_z:
                    z = shoulder_z
            elif joint == joints.ELBOW_LEFT:
                shoulder_z = self.positions[joints_map[joints.SHOULDER_LEFT]].Position.z
                if z > shoulder_z:
                    z = shoulder_z
            positions[joints_map[joint]] = [x, y, z]
        return positions


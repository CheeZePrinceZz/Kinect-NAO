import motion
import threading
from naoqi import ALProxy

global IP
IP = "169.254.168.203"
#IP = "192.168.11.32"

global PORT
PORT = 9559
global motionproxy
motionproxy = ALProxy("ALMotion", IP, PORT)


class NAOCommander():
    def __init__(self, IP, PORT):
        global motionproxy
        motionproxy = ALProxy("ALMotion", IP, PORT)
        postureproxy = ALProxy("ALRobotPosture", IP, PORT)
        # Wake up robot
        motionproxy.wakeUp()
        postureproxy.goToPosture("Stand", 0.5)
        #############################################################
        pNames          = "LLeg"
        pStiffnessLists = 1.0
        pTimeLists      = 1.0
        motionproxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        pNames          = "RLeg"
        pStiffnessLists = 1.0
        pTimeLists      = 1.0
        motionproxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        #############################################################
        motionproxy.setCollisionProtectionEnabled("Arms", True)

        self.device = motionproxy
        self.postureProxy = postureproxy

    # TODO move with motors and positions
    # def move(self):

    def go_to_zero(self):
        self.postureProxy.goToPosture("Stand", 0.5)
        self.user_right_arm_articular()
        self.user_left_arm_articular()

    def wave_your_left_hand(self):
        # Arms motion from user have always the priority than walk arms motion
        jointnames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LHand"]
        arm1 = [-90, 55, -6, -3.]
        arm1 = [x * motion.TO_RAD for x in arm1]
        # The hand is not in degree, we need to add it after the conversion
        arm1.append(0.98)

        arm2 = [-90, 55, -6, -85.]
        arm2 = [x * motion.TO_RAD for x in arm2]
        # The hand is not in degree, we need to add it after the conversion
        arm2.append(0.98)

        arm0 = [87, 0, -70, -34.]
        arm0 = [x * motion.TO_RAD for x in arm0]
        # The hand is not in degree, we need to add it after the conversion
        arm0.append(0.28)

        pfractionmaxspeed = 0.6

        self.device.angleInterpolationWithSpeed(jointnames, arm1, pfractionmaxspeed)
        self.device.angleInterpolationWithSpeed(jointnames, arm2, pfractionmaxspeed)
        self.device.angleInterpolationWithSpeed(jointnames, arm1, pfractionmaxspeed)
        self.device.angleInterpolationWithSpeed(jointnames, arm2, pfractionmaxspeed)
        self.device.angleInterpolationWithSpeed(jointnames, arm0, pfractionmaxspeed)

    def move_robot(self, right_shoulder_pitch=80.5, right_shoulder_roll=-6.5, right_elbow_yaw=80,
                         right_elbow_roll=2.5, right_wrist_yaw=0., right_hand=0.00,
                         left_shoulder_pitch=80.5, left_shoulder_roll=6.5, left_elbow_yaw=-80,
                         left_elbow_roll=-2.5, left_wrist_yaw=0., left_hand=0.00,
                         head_pitch = 0.0, head_yaw = 0.0,
                         pfractionmaxspeed=0.6):
        if not self.device.moveIsActive():
            self.device.wbEnable(True)
            self.device.wbFootState("Fixed", "Legs")
            self.device.wbEnableBalanceConstraint(True, "Legs")
            #jointnames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
            #              "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
            #              "HeadPitch","HeadYaw"]
            jointnames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
                          "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand","HeadPitch","HeadYaw"]
            movement = [right_shoulder_pitch, right_shoulder_roll, right_elbow_yaw, right_elbow_roll, right_wrist_yaw]
            movement = [x * motion.TO_RAD for x in movement]
            # The hand is not in degree, we need to add it after the conversion
            movement.append(right_hand)
            l_arm = [left_shoulder_pitch, left_shoulder_roll, left_elbow_yaw, left_elbow_roll, left_wrist_yaw]
            l_arm = [x * motion.TO_RAD for x in l_arm]
            l_arm.append(left_hand)
            movement.extend(l_arm)
            movement.append(head_pitch)
            movement.append(head_yaw)
            #print "Head Pitch: ",head_pitch, "\n"
            #print "Head Yaw: ",head_yaw, "\n"
            #movement.append(head_yaw * motion.TO_RAD)

            #self.device.angleInterpolationWithSpeed(jointnames, movement, pfractionmaxspeed)  ### UNUSED

            ###################################################################
            self.device.setAngles(jointnames, movement, pfractionmaxspeed)
            #name = ["HeadYaw", "HeadPitch"]
            #time = 0.6
            #isAbsolute = True
            #self.motionproxy.angleInterpolation(names, angleLists, time, isAbsolute)

            #angleLists = [head_yaw * motion.TO_RAD ,head_pitch * motion.TO_RAD]
            #angleLists = [head_pitch * motion.TO_RAD]
            #self.threadingMovement(jointnames, movement, angleLists)
            ####################################################################


    # def bodyMovement(self, jointnames, movement):
    #     pfractionmaxspeed = 0.6
    #     self.device.setAngles(jointnames, movement, pfractionmaxspeed)


    # def headMovement(self, angleLists):
    #     #names = ["HeadYaw", "HeadPitch"]
    #     names = "HeadPitch"
    #     time = 0.4
    #     isAbsolute = True
    #     motionproxy.angleInterpolation(names, angleLists, time, isAbsolute)
    #
    #
    # def threadingMovement(self, jointnames, movement, angleLists):
    #     process1 = threading.Thread(target = self.bodyMovement(jointnames, movement))
    #     process1.daemon = True
    #     process2 = threading.Thread(target = self.headMovement(angleLists))
    #     process2.daemon = True
    #     process1.start()
    #     process2.start()


    def user_right_arm_articular(self, shoulder_pitch=80.5, shoulder_roll=-6.5, elbow_yaw=80,
                                 elbow_roll=2.5, wrist_yaw=0., hand=0.00, pfractionmaxspeed=0.6):
        if not self.device.moveIsActive():
            if shoulder_pitch > 115:
                shoulder_pitch = 115
            if shoulder_pitch < -117:
                shoulder_pitch = -117
            if shoulder_roll > 5:
                shoulder_roll = 5
            if shoulder_roll < -65:
                shoulder_roll = -65
            if elbow_roll > 85:
                elbow_roll = 85
            if elbow_roll < 4:
                elbow_roll = 4
            if elbow_yaw > 115:
                elbow_yaw = 115
            if elbow_yaw < -115:
                elbow_yaw = -115
            if wrist_yaw < -100:
                wrist_yaw = -100
            if wrist_yaw > 100:
                wrist_yaw = 100

            # Arms motion from user have always the priority than walk arms motion
            jointnames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
            arm1 = [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_roll, wrist_yaw]
            arm1 = [x * motion.TO_RAD for x in arm1]
            # The hand is not in degree, we need to add it after the conversion
            arm1.append(hand)

            self.device.angleInterpolationWithSpeed(jointnames, arm1, pfractionmaxspeed)

    def user_left_arm_articular(self, shoulder_pitch=80, shoulder_roll=6.5, elbow_yaw=-80,
                                elbow_roll=-3.7, wrist_yaw=0., hand=0.00, pfractionmaxspeed=0.6):
        if not self.device.moveIsActive():
            if shoulder_pitch > 115:
                shoulder_pitch = 115
            if shoulder_pitch < -117:
                shoulder_pitch = -117
            if shoulder_roll < -5:
                shoulder_roll = -5
            if shoulder_roll > 65:
                shoulder_roll = 65
            if elbow_roll < -85:
                elbow_roll = -85
            if elbow_roll > -4:
                elbow_roll = -4
            if elbow_yaw > 115:
                elbow_yaw = 115
            if elbow_yaw < -115:
                elbow_yaw = -115
            if wrist_yaw < -100:
                wrist_yaw = -100
            if wrist_yaw > 100:
                wrist_yaw = 100

            # Arms motion from user have always the priority than walk arms motion
            jointnames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"]
            arm1 = [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_roll, wrist_yaw]
            arm1 = [x * motion.TO_RAD for x in arm1]
            # The hand is not in degree, we need to add it after the conversion
            arm1.append(hand)
            self.device.angleInterpolationWithSpeed(jointnames, arm1, pfractionmaxspeed)

    def user_right_leg_articular(self, knee_pitch=-5, hip_pitch=3, ankle_pitch=5):
        is_enabled = True
        self.device.wbEnable(is_enabled)
        state_name = "Fixed"
        support_leg = "Legs"
        self.device.wbFootState(state_name, support_leg)
        is_enabled = True
        support_leg = "Legs"
        self.device.wbEnableBalanceConstraint(is_enabled, support_leg)
        jointnames = ["RKneePitch", "RHipPitch", "RAnklePitch"]
        leg = [knee_pitch, hip_pitch, ankle_pitch]
        leg = [x * motion.TO_RAD for x in leg]
        support_leg = "Legs"
        duration = 3600.0
        self.motion.wbGoToBalance(support_leg, duration)

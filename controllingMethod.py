import kinecthandler as kinecthandler
import naocommander as naocommander
import converter as converter
#import SkeletonDisplay as SkeletonDisplay
#import threading

#robotIP = "192.168.2.24"
# robotIP = "127.0.0.1"
robotIP = "169.254.168.203"
#robotIP = "169.254.15.210"
PORT = 9559
# PORT = 8352
nb_of_body = 1



class controllingMethod():
    def __init__(self):
        #_sensor = kinecthandler.KinectHandler()
        #_avatar = naocommander.NAOCommander(robotIP, PORT)
        #kinect_test(_sensor, _avatar)
        kinect_h = kinecthandler.KinectHandler()
        nao_c = naocommander.NAOCommander(robotIP, PORT)

#    def kinect_test(kinect_h, nao_c):
        while True:
            nao_c.device.waitUntilMoveIsFinished()
            res = kinect_h.get_movement(nb_of_body)
            if res == kinecthandler.NO_DATA:
                continue
            for i in range(nb_of_body):
                [r_s_roll, r_s_pitch, r_e_roll, r_e_yaw, r_w_yaw] = converter.get_right_arm(res[i][0], res[i][1])
                [l_s_roll, l_s_pitch, l_e_roll, l_e_yaw, l_w_yaw] = converter.get_left_arm(res[i][0], res[i][1])
                h_pitch = converter.get_head_PITCH(res[i][0])
                h_yaw = converter.get_head_YAW(res[i][0])
                [r_hand, l_hand] = converter.get_hands(res[i][2])
                nao_c.move_robot(right_shoulder_roll=r_s_roll, right_shoulder_pitch=r_s_pitch,
                                right_elbow_roll=r_e_roll, right_elbow_yaw=r_e_yaw,
                                right_wrist_yaw=r_w_yaw,
                                left_shoulder_roll=l_s_roll, left_shoulder_pitch=l_s_pitch,
                                left_elbow_roll=l_e_roll, left_elbow_yaw=l_e_yaw,
                                left_wrist_yaw=l_w_yaw,
                                head_pitch=h_pitch, head_yaw=h_yaw, right_hand=r_hand, left_hand=l_hand,
                                pfractionmaxspeed=0.4)

#def main():
#    print "In main"
#    SkeletonDisplay.BodyGameRuntime()
#    _sensor = kinecthandler.KinectHandler()
#    _avatar = naocommander.NAOCommander(robotIP, PORT)
#    kinect_test(_sensor, _avatar)
    # process1 = threading.Thread(target = SkeletonDisplay.BodyGameRuntime())
    # process1.daemon = True
    # process2 = threading.Thread(target = kinecthandler.KinectHandler())
    # process2.daemon = True
    # process3 = threading.Thread(target = naocommander.NAOCommander(robotIP, PORT))
    # process3.daemon
    # process1.start()
    # process2.start()
    # process3.start()
    # _sensor = process2
    # _avatar = process3
    # kinect_test(_sensor, _avatar)

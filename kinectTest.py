import kinecthandler as kinecthandler
import naocommander as naocommander
import converter as converter

#robotIP = "192.168.2.24"
# robotIP = "127.0.0.1"
robotIP = "169.254.168.203"
#robotIP = "169.254.15.210"
PORT = 9559
# PORT = 8352
nb_of_body = 1


def kinect_test(kinect_h):
    while True:
        res = kinect_h.get_movement(nb_of_body)
        if res == kinecthandler.NO_DATA:
            continue
        for i in range(nb_of_body):
                [r_s_roll, r_s_pitch, r_e_roll, r_e_yaw, r_w_yaw] = converter.get_right_arm(res[i][0], res[i][1])
                [l_s_roll, l_s_pitch, l_e_roll, l_e_yaw, l_w_yaw] = converter.get_left_arm(res[i][0], res[i][1])
                h_pitch = converter.get_head_PITCH(res[i][0])
                h_yaw = converter.get_head_YAW(res[i][0])
                [r_hand, l_hand] = converter.get_hands(res[i][2])

if __name__ == '__main__':
    _sensor = kinecthandler.KinectHandler()
    kinect_test(_sensor)

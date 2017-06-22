
import controllingMethod as controllingMethod
import SkeletonDisplay as SkeletonDisplay
import threading

if __name__ == '__main__':
    SkeletonDisplay.BodyGameRuntime()
    _sensor = kinecthandler.KinectHandler()
    _avatar = naocommander.NAOCommander(robotIP, PORT)
    kinect_test(_sensor, _avatar)

    process1 = threading.Thread(target = SkeletonDisplay.BodyGameRuntime())
    process1.daemon = True
    process2 = threading.Thread(target = controllingMethod.main ())
    # process2.daemon = True
    # process3 = threading.Thread(target = naocommander.NAOCommander(robotIP, PORT))
    # process3.daemon
    # process1.start()
    # process2.start()
    # process3.start()
    # _sensor = process2
    # _avatar = process3
    # kinect_test(_sensor, _avatar)

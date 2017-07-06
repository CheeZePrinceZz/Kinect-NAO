# -*- encoding: UTF-8 -*-

import time
import os
import sys
import datetime
import argparse
import math
import threading
import random
import numpy
import motion
import almath
import qi

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from optparse import OptionParser
from collections import Counter
from rapp_robot_api import RappRobot

rh = RappRobot()
########## CHANGE IP OF NAO HERE ###########
# IP = "169.254.1.189"   #WIRE
IP = "169.254.168.203"   #WIRE
#IP = "192.168.11.32"      #Wireless 

# IP = "169.254.246.118"     #WIRE
# IP = "169.254.201.66"
#IP = "169.254.128.114"      #WIRELESS
PORT = 9559
############################################

######### Global Variable #################
global memory
global faceProxy
global videoRecorderProxy
global motionProxy
global gazeProxy
global Flag
global TouchBehavior
global animatedSpeechProxy
global cont
global counter
global Headcont
global tts
global gazeStorage
global isFace
global facePositionX
global facePositionY
global facePositionZ
global faceTrackingProxy
global faceTrackingFlag
global Condition
global firstFlag
global secondFlag
global postureProxy
global blinkingProxy
global ContentChoice
global Content
global Closing


# Global variable to store the ReactToTouch module instance
ReactToTouch = None
memory = None

gazeStorage = []
Headcont = 1
counter = 1
firstFlag = 1
secondFlag = 0
faceTrackingFlag = 1
isFace = False
facePositionX = 0
facePositionY = 0
facePositionZ = 0

##################################################################################################################################
######################################################## CONTENT ZONE ############################################################
##################################################################################################################################
##################################################################################################################################
Content1 = """Hi am NAO. Today I want to start by asking you to pay attention to what posture you are doing right now. I hope that if you learn to tweak this a little bit, it could significantly change the way your life unfolds.
So, we are really fascinated with body language, and we are particularly interested in other peoples body language.
You know, we are interested in an awkward interaction, or a smile, or a contemptuous glance, or maybe a very awkward wink,
or maybe even something like a handshake. So obviously when we think about nonverbal behavior, or body language.
We think about communication. When we think about communication, we think about interactions.
So what is your body language communicating to me? What's mine communicating to you?
So social scientists have spent a lot of time looking at the effects of our body language, or other peoples body language, on judgments.
And we make sweeping judgments and inferences from body language. And those judgments can predict really meaningful life outcomes like who we hire or promote, who we ask out on a date.
For example, Nalini Ambady, a researcher at Tufts University, shows that when people watch 30 seconds soundless clips of real physician-patient interactions, 
their judgments of the physician's niceness predict whether or not that physician will be sued. 
So it doesn't have to do so much with whether or not that physician was incompetent, but do we like that person and how they interacted. And this is the end for this session."""

Content2 = """Okay, let’s continue. Another dramatic example is from the study of Alex Todorov which shows that judgments of political candidates' faces in just one second predict 70 percent of U.S. Senate
and gubernatorial race outcomes. Well, when we think of nonverbals, we think of how we judge others, how they judge us and what the outcomes are. 
We tend to forget, though, the other audience that's influenced by our nonverbals, and that's ourselves. We are also influenced by our nonverbals, our thoughts and our feelings and our physiology.
Here, I’m talking about nonverbal expressions of power and dominance. And what are nonverbal expressions of power and dominance? Well, in the animal kingdom, they are about expanding.
So you make yourself big, you stretch out, you take up space, you're basically opening up. It's about opening up. And this is true across the animal kingdom. It's not just limited to primates.
And humans do the same thing. So they do this both when they have power sort of chronically, and also when they're feeling powerful in the moment.
And this one is especially interesting because it really shows us how universal and old these expressions of power are. This expression, which is known as pride, Jessica Tracy has studied.
She shows that people who are born with sight and people who are congenitally blind do this when they win at a physical competition.
So when they cross the finish line and they've won, it doesn't matter if they've never seen anyone do it. They do this. So the arms up in the V, the chin is slightly lifted.
And this is the end for this session."""

Content3 = """Let’s continue to our third part. What do we do when we feel powerless? We do exactly the opposite. We close up. We wrap ourselves up. We make ourselves small.
We don't want to bump into the person next to us. So again, both animals and humans do the same thing. And this is what happens when you put together high and low power. 
So what we tend to do when it comes to power is that we complement the other's nonverbals. So if someone is being really powerful with us, we tend to make ourselves smaller.
We don't mirror them. We do the opposite of them. When noticing the behavior in the classroom, we can notice that the students really exhibit the full range of power nonverbals. 
So you have people who are like caricatures of alphas, really coming into the room, they get right into the middle of the room before class even starts, like they really want to occupy space.
When they sit down, they're sort of spread out. They raise their hands. You have other people who are virtually collapsing when they come in.
As soon they come in, they sit in their chair and they make themselves tiny. Well, you're not going to be surprised. It seems to be related to gender. 
So women are much more likely to do this kind of thing than men. Women feel chronically less powerful than men, so this is not surprising.
And this is the end for this session."""

Content4 = """Now let’s move on to the forth part. the other thing I noticed, other than gender, is that it also seemed to be related to the extent to which the students were participating,
and how well they were participating. You get these equally qualified women and men coming in and then you get these differences in grades, and it seems to be partly attributable to participation.
So we started to wonder, Is it possible that we could get people to fake it and would it lead them to participate more? In Dana Carney’s study, he really wanted to know,
can you fake it till you make it? Like, can you do this just for a little while and actually experience a behavioral outcome that makes you seem more powerful? 
So we know that our nonverbals govern how other people think and feel about us. There's a lot of evidence. But our question really was, do our nonverbals govern how we think and feel about ourselves?
There's some evidence that they do. For example, we smile when we feel happy, but also, when we're forced to smile by holding a pen in our teeth, it makes us feel happy.
So it goes both ways. When it comes to power, it also goes both ways. So when you feel powerful, you're more likely to go big, but it's also possible that when you pretend to be powerful,
you are more likely to actually feel powerful.
And this is the end for this session."""

Content5 = """Next. Now we know that our minds change our bodies, but is it also true that our bodies change our minds? And when I say minds, in the case of the powerful.
I'm talking about thoughts and feelings and the sort of physiological things that make up our thoughts and feelings, and in my case, that's hormones.
So what do the minds of the powerful versus the powerless look like? So powerful people tend to be, not surprisingly, more assertive and more confident, more optimistic.
They actually feel they're going to win even at games of chance. They also tend to be able to think more abstractly. So there are a lot of differences. They take more risks.
There are a lot of differences between powerful and powerless people. Physiologically, there also are differences on two key hormones:
testosterone, which is the dominance hormone, and cortisol, which is the stress hormone. So what we find is that high-power alpha males in primate hierarchies have high testosterone
and low cortisol, and powerful and effective leaders also have high testosterone and low cortisol. So what does that mean? When you think about power, 
people tended to think only about testosterone, because that was about dominance. But really, power is also about how you react to stress. 
So do you want the high-power leader that's dominant, high on testosterone, but really stress reactive? Probably not. 
You want the person who's powerful and assertive and dominant, but not very stress reactive, the person who's laid back.
And this is the end for this session."""

Content6 = """Okay. Let’s continue. So we know that in primate hierarchies, if an alpha needs to take over, if an individual needs to take over an alpha role sort of suddenly, within a few days,
that individual's testosterone has gone up significantly and his cortisol has dropped significantly. So we have this evidence, both that the body can shape the mind, at least at the facial level,
and also that role changes can shape the mind. But. What happens if you do that at a really minimal level? In Amy’s study, they decided to bring people into the lab and run an experiment,
and these people adopted, for two minutes, either high-power poses or low-power poses. And this is what happens. They came in and the experimenters took their saliva sample.
Then, asked them to do the poses for two minutes and then ask them, How powerful do you feel? on a series of items. After that the experimenter gave them an opportunity to gamble,
and took another saliva sample. That's it. That's the whole experiment. So this is what we find. Risk tolerance, which is the gambling, we find that when you are in the high-power pose condition, 
86 percent of the participant will gamble. When you're in the low-power pose condition, only 60 percent, and that's a whopping significant difference. Here's what we find on testosterone.
From their baseline when they come in, high-power people experience about a 20 percent increase, and low-power people experience about a 10 percent decrease.
So again, only two minutes, we can see the changes.
And this is the end for this session."""

Content7 = """Next, here's what they found in cortisol. High-power people experience about a 25 percent decrease, and the low-power people experience about a 15 percent increase.
So two minutes lead to these hormonal changes that configure your brain to basically be either assertive, confident and comfortable, or really stress-reactive, and feeling sort of shut down.
So it seems that our nonverbals do govern how we think and feel about ourselves, so it's not just others, but it's also ourselves. Also, our bodies change our minds.
But the next question is can power posing for a few minutes really change your life in meaningful ways? Where can you actually apply this?
The answer is the evaluative situations, like social threat situations. Where are you being evaluated by your friends? For example, at the lunchroom table, at a meeting or a job interview.
Again, the researcher, Amy, bring people into a lab, and they do either high or low-power poses again, they go through a very stressful job interview.
It's five minutes long and is video recorded. They're being judged also, and the judges are trained to give no nonverbal feedback. So for five minutes, nothing. People hate this.
So this really spikes their cortisol.  Four coders look at the recorded tapes, and they say, We want to hire these people, which are all the high-power posers. 
But what's driving it? It's not about the content of the speech. It's about the presence that they're bringing to the speech. People are bringing their true selves, basically.
They bring their ideas as themselves, with no residue over them. So this is what's driving the effect, or mediating the effect.
And this is the end for this session."""

Content8 = """Well, let’s continue. The reason why Amy insists that our bodies change our minds and our minds can change our behavior, and our behavior can change our outcomes is according to her own experience.
That’s why she continues her study on this path. When she was a teenager, she was in a really bad car accident and got head injury which causes her brain trauma and changes her from a smart girl to low IQ person
so she was taken out of college. Due to her injury condition, everyone said she’s not going to finish college. Since then she felt entirely powerless.
But she still tried to struggle with this and continued her study and she ended up at Princeton by begging for her advisor to accept her.
However, with the mindset that she is not supported to be here and she is an imposter. And the night before her first-year talk, a 20 minutes talk in front of 20 people.
She was so afraid of being found out the next day that she called her advisor and said, I’m quitting. Then her advisor replied, “You are not quitting because I took a gamble on you.
You’re going to stay, and this is what you’re going todo. You are going to fake it even if you’re terrified, until you have the moment where you say
Oh my gosh, I’m actually doing it and I have become this ! So that’s what Amy did, empowering herself. And you know what, at this moment, she is now a professor at Harvard.
And this is the end for this session."""


Content9 = """Now, this is the last part of my talk. Let’s continue with Amy’s story. At the end of her first year at Harvard, a student came into her office, looked totally defeated,
and the student said I’m not supposed to be here and that is the moment for Amy that she realized, oh my gosh, she doesn’t feel like that anymore but her student does. So she told her student,
Yes, you are supposed to be here! and tomorrow you’re going to fake it, you’re going to make yourself powerful. And you’re going to give the best comment in classroom ever
And her student did so and everyone started to notice her in classroom. Months later, Amy realized that her student had not just faked it till she made it,
she had actually faked it till she became it. So she had changed. From Amy’s and her student’s story, we all learn that don't fake it till you make it. Fake it till you become it.
Do it enough until you actually become it and internalize. Tiny tweaks can lead to big changes. So, from now on before you go into the next stressful evaluative situation, for two minutes,
try to empower yourself like doing high power postures, in the elevator, in a toilet, or at your desk. Configure your brain to cope the best in that situation. Get your testosterone up.
Get your cortisol down. Leave that situation feeling like, I really feel like I got to say who I am and show who I am. Just two minutes to empower yourself, 
and it can significantly change the outcomes of your life. And this is the end of my talk. Thank you very much for your kind attention."""
##################################################################################################################################
###################################################### MAIN MODULE ZONE ##########################################################
##################################################################################################################################

############################################
####  MAIN MODULE for Touch Behavior   #####
############################################
# - Touch Human's shoulder                 #
# - Face tracking                          #
# - Gesture                                #
############################################
# class TouchBehavior(ALModule):
#     #### INITIAL FUNCTION ####
#     # def __init__(self, name):
#     #     ALModule.__init__(self, name)
#     #     self.tts = ALProxy("ALTextToSpeech")
#     #     global memory
#     #     memory = ALProxy("ALMemory")
#     #     memory.subscribeToEvent("ALChestButton/DoubleClickOccurred","TouchBehavior","onChestButtonPressed")
#     # ########################
#     #
#     # def onChestButtonPressed(self, *_args):
#         global motionProxy
#         global firstFlag
#         global secondFlag
#         global cont
#         global tts
#         global animatedSpeechProxy
#         # global memory
#         # memory = ALProxy("ALMemory")
#         motionProxy = ALProxy("ALMotion", IP, PORT)
#         # postureProxy = ALProxy("ALRobotPosture", IP, PORT)
#         # postureProxy.goToPosture("Stand", 0.5)
#         if firstFlag == 1:
#             # memory.unsubscribeToEvent("ALChestButton/DoubleClickOccurred","TouchBehavior")
#             # memory.subscribeToEvent("ALChestButton/DoubleClickOccurred", "TouchBehavior", "onChestButtonPressed")
#             firstFlag = 0
#             secondFlag = 1
#
#             process1 = threading.Thread(target = LectureWithMovement)
#             process1.daemon = True
#             process2 = threading.Thread(target = FaceTracking)
#             process2.daemon = True
#             # process3 = threading.Thread(target = TouchOnShoulder)
#             # process3.deamon = True
#
#             process1.start()
#             process2.start()
#             # process3.start()
#
#         elif secondFlag == 1:
#             # memory.unsubscribeToEvent("ALChestButton/DoubleClickOccurred","TouchBehavior")
#             secondFlag = 0
#             cont = 0
#             counter = 0
#
#             process1 = threading.Thread(target = StopLecturing)
#             process1.daemon = True
#
#             process2 = threading.Thread(target = StopMotion)
#             process2.daemon = True
#
#             process3 = threading.Thread(target = StopFaceTracking)
#             process3.daemon = True
#
#             process1.start()
#             process2.start()
#             process3.start()
#
#             exit()
#             quit()
#             os._exit(1)
#     ########################
##################################################################################################################################


##################################################################################################################################
######################################################### FUNCTION ZONE ##########################################################
##################################################################################################################################


############################################
#######    SITPOSITION FUNCTION    #######
############################################
def WordDetection():
    global motionProxy
    time.sleep(90)
    while True:
        detected = rh.audio.speechDetection(["sit", "rest", "stop"], 100, "English")
        global asr
        asr = ALProxy("ALSpeechRecognition", IP, PORT)
        if len(detected) > 1:
            print "Word Detection Probability: ",detected['probability']
            if detected['probability'] >= 0.1:
                asr.subscribe("Test_ASR")
                asr.unsubscribe("Test_ASR")
                rh.humanoid_motion.goToPosture('Crouch', 0.3)
                motionProxy.rest()
        else:
            asr.subscribe("Test_ASR")
            asr.unsubscribe("Test_ASR")
############################################

############################################
########## GazeBehaviour FUNCTION ##########
############################################
def GazeBehaviour():
    global faceTrackingProxy
    global faceTrackingFlag
    global isFace
    global facePositionX
    global facePositionY
    global facePositionZ
    # global motionProxy
    try:
        faceTrackingProxy = ALProxy("ALFaceTracker", IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALFaceTracker"
        print "Error was: ", e
    isFaceCount = 0
    faceTrackingProxy.startTracker()
    faceTrackingFlag = 1
    firstFlag = 1
    selectedDuration = 5
    durationChoices = [5, 7, 9, 11]
    # selectedDuration = numpy.random.choice([5, 7, 9, 11], 1, p=[0.4, 0.3, 0.2, 0.1])
    selectedDuration = random.randrange(5, 11, 2)
    while faceTrackingFlag == 1:
        time.sleep(0.1)
        isFace = faceTrackingProxy.isNewData()
        if isFace == True:
            isFaceCount = isFaceCount+1
        else:
            isFaceCount = 0
            durationChoices = [5, 7, 9, 11]
            selectedDuration = random.randrange(5, 11, 2)
            # selectedDuration = numpy.random.choice([5, 7, 9, 11], 1, p=[0.4, 0.3, 0.2, 0.1])
        if isFaceCount > selectedDuration:
            GazeShifting()
            isFaceCount = 0
############################################


############################################
########## GAZE SHIFTING FUNCTION ##########
############################################
def GazeShifting():
    global motionProxy
    name = "HeadYaw"
    useSensors  = True
    sensorAngles = motionProxy.getAngles(name, useSensors)
    angle = sensorAngles[0]
    frequency = random.randint(1,2)
    print "Gaze Shifting: ",frequency
    isAbsolute = True
    # StiffnessOn(motionProxy)
    if frequency == 1:
        angleLists = [angle+0.1, angle]
        times      = [0.1, 1]
    elif frequency == 2:
        angleLists = [angle-0.1, angle]
        times      = [0.1, 1]
    motionProxy.angleInterpolation(name, angleLists, times, isAbsolute)
############################################

############################################
###### HeadNoddingImitation FUNCTION #######
############################################
def HeadNoddingImitation():
    global faceTrackingProxy
    global faceTrackingFlag
    global isFace
    global facePositionX
    global facePositionY
    global facePositionZ
    global noddingTimer
    # global motionProxy
    try:
        faceTrackingProxy = ALProxy("ALFaceTracker", IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALFaceTracker"
        print "Error was: ", e
    isFaceCount = 0
    faceTrackingProxy.startTracker()
    faceTrackingFlag = 1
    firstFlag = 1
    selectedDuration = 5
    while faceTrackingFlag == 1:
        time.sleep(0.1)
        facePosition = faceTrackingProxy.getPosition()
        facePositionX = round(facePosition[0],4)
        facePositionY = round(facePosition[1],4)
       ########### HEAD NODDING ATTIVATION ##########
        if firstFlag == 1:
            previousFacePositionY = facePositionY
            firstFlag = 0
        else:
            print str(abs(facePositionY - previousFacePositionY))+"\n"
            if abs(facePositionY - previousFacePositionY) > 0.03:
                previousFacePositionY = facePositionY
                HeadNodding()
                print "Nodding Imitation"
                noddingTimer = 0
        ################################
        # facePositionZ = round(facePosition[2],4)
        # print str(facePositionX) + " : " +str(facePositionY) + " : " + str(facePositionZ)
        # print "*******"
        # print str(isFaceCount)
############################################

############################################
###### HeadNoddingInitiation FUNCTION #######
############################################
def HeadNoddingInitiation():
    global noddingTimer
    noddingTimer = 0
    HselectedDuration = random.randrange(10, 20, 5)
    while True:
        time.sleep(1)
        noddingTimer += 1
        if noddingTimer > HselectedDuration:
            HeadNodding()
            print "Nodding Initiation"
            noddingTimer = 0
            HselectedDuration = random.randrange(10, 20, 5)
############################################

############################################
########## HEAD NODDING FUNCTION ###########
############################################
def HeadNodding():
    frequency = random.randint(1,6)
    name = "HeadPitch"
    isAbsolute = True
    # StiffnessOn(motionProxy)
    if frequency == 1:
        angleLists = [-0.1, 0.1, -0.1, 0.1, 0.0]
        times      = [0.2, 0.4, 0.6, 0.8, 1.0]
    elif frequency == 2:
        angleLists = [-0.2, 0.2, -0.2, 0.2, 0.0]
        times      = [0.3, 0.6, 0.9, 1.2, 1.5]
    elif frequency == 3:
        angleLists = [-0.2, 0.2, 0.0]
        times      = [0.3, 0.6, 0.9]
    elif frequency == 4:
        angleLists = [-0.1, 0.1, 0.0]
        times      = [0.2, 0.4, 0.6]
    elif frequency == 5:
        angleLists = [-0.1, 0.1, 0.0]
        times      = [0.3, 0.6, 0.9]
    elif frequency == 6:
        angleLists = [-0.1, 0.1, -0.1, 0.1, 0.0]
        times      = [0.3, 0.6, 0.9, 1.2, 1.5]
    motionProxy.angleInterpolation(name, angleLists, times, isAbsolute)
############################################

############################################
####### SpeakingWithGesture FUNCTION #######
############################################
def SpeakingWithGesture():
    global animatedSpeechProxy
    global tts
    global motionProxy
    global motion
    global SpeechRecognitionProxy
    AutonomousMoves.setExpressiveListeningEnabled(True)
    AutonomousMoves.setBackgroundStrategy("backToNeutral")
    motionProxy.setBreathEnabled('Body', True)
    try:
        tts = ALProxy("ALTextToSpeech", IP, PORT)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ",e
        sys.exit(1)
    animatedSpeechProxy = ALProxy("ALAnimatedSpeech", IP, PORT)
    tts.setParameter("pitchShift", 1.0)
    configuration = {"bodyLanguageMode":"contextual"}
    animatedSpeechProxy.say(Content, configuration)
    StopFaceTracking()
############################################

############################################
####### LectureWithMovement FUNCTION #######
############################################
def LectureWithMovement():
    global animatedSpeechProxy
    global tts
    global motionProxy
    global motion
    global SpeechRecognitionProxy

    motionProxy.setBreathEnabled('Body', True)
    try:
        tts = ALProxy("ALTextToSpeech", IP, PORT)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ",e
        sys.exit(1)
    animatedSpeechProxy = ALProxy("ALAnimatedSpeech", IP, PORT)
    tts.setParameter("pitchShift", 1.0)
    # asr = ALProxy("ALSpeechRecognition", IP, PORT)


    # ttw = { "hello" : ["hey", "yo"],
    #         "everything" : ["everybody"] }
    #
    # animatedSpeechProxy.addTagsToWords(ttw)

    configuration = {"bodyLanguageMode":"contextual"}
    animatedSpeechProxy.say(Content, configuration)

    # configuration = {"bodyLanguageMode":"disabled"}
    # animatedSpeechProxy.say(Content, configuration)
    # rh.motion.enableMotors()
    # rh.humanoid_motion.setJointAngles(['LShoulderPitch','LShoulderRoll','LElbowYaw','LElbowRoll'], [0,0,0,-0.0349], 0.3)

    # JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    # Arm1 = [24, 0, -119.5, -2]
    # Arm1 = [ x * motion.TO_RAD for x in Arm1]
    # # pFractionMaxSpeed = 0.3
    # timeLists  = [1.0, 10.0]
    # isAbsolute = True
    # motionProxy.angleInterpolation(JointNames, Arm1, timeLists, isAbsolute)
    # motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
    # autonomousProxy.setState("disabled")
    autonomousProxy.setBackgroundStrategy("none")

    motionProxy.setStiffnesses("LArm", 1.0)

    names  = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    # Each joint can have lists of different lengths, but the number of
    # angles and the number of times must be the same for each joint.
    # Here, the second joint ("HeadPitch") has three angles, and
    # three corresponding times.
    angleLists = [24, 0, -119.5, -2]
    angleLists = [ x * motion.TO_RAD for x in angleLists]
    timeLists   = [[5.0], [5.0], [5.0], [5.0]]
    isAbsolute  = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    motionProxy.setStiffnesses("LArm", 1.0)
    rh.audio.speak("Do you want to touch or hold my hand?")
    res = rh.audio.speechDetection(['yes', 'no', 'okay'], 10)
    print res
    word = ''
    if res['error'] == None:
         word = res['word']
         HoldHand(word)
    else:
        SpeechRecognitionProxy.pause(True)
        rh.audio.speak("Don't you want to hold my hand?")
        res = rh.audio.speechDetection(['yes', 'no', 'okay'], 10)
        print res
        word = ''
        if res['error'] == None:
             word = res['word']
             HoldHand(word)
        else:
            TouchOnShoulder()
############################################

############################################
#######     SpeakingOnly FUNCTION    #######
############################################
def SpeakingOnly():
    global tts
    global motionProxy
    try:
        tts = ALProxy("ALTextToSpeech", IP, PORT)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ",e
        sys.exit(1)

    tts.setParameter("pitchShift", 1.0)
    tts.say(Content)
    StopFaceTracking()
############################################

############################################
#######      HoldHand FUNCTION       #######
############################################
def HoldHand(word):
    if word == 'yes' or word == 'okay':
        print 'yes'
        SpeechRecognitionProxy.pause(True)
        rh.humanoid_motion.openHand("Left")
        rh.audio.speak("Let's hold hand !")
        global ReactToTouch
        ReactToTouch = ReactToTouch("ReactToTouch")
        ##### WHEN SENSOR IS TOUCHED, ASK TO TOUCH HUMAN #####

        if touched_bodies != None:
            JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
            Arm1 = [90, 0, 0, -2]
            Arm1 = [ x * motion.TO_RAD for x in Arm1]
            pFractionMaxSpeed = 0.3
            motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
            rh.humanoid_motion.closeHand("Left")
            TouchOnShoulder()
        ####### Wait for 10 secs ######
        else:
            time.sleep(10)
            JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
            Arm1 = [90, 0, 0, -2]
            Arm1 = [ x * motion.TO_RAD for x in Arm1]
            pFractionMaxSpeed = 0.3
            motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
            rh.humanoid_motion.closeHand("Left")
            TouchOnShoulder()
    elif word == 'no':
        print 'no'
        SpeechRecognitionProxy.pause(True)
        rh.humanoid_motion.closeHand("Left")
        rh.audio.speak("Okay, I'm sorry to bother you")
        JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
        Arm1 = [90, 0, 0, -2]
        Arm1 = [ x * motion.TO_RAD for x in Arm1]
        pFractionMaxSpeed = 0.3
        motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
        TouchOnShoulder()
############################################

############################################
#######   TouchOnShoulder FUNCTION   #######
############################################
def TouchOnShoulder():
    asking = "Now You touched me already. Would you allow me to touch you on your shoulder ?"
    configuration = {"bodyLanguageMode":"contextual"}
    animatedSpeechProxy.say(asking, configuration)
    res2 = rh.audio.speechDetection(['yes', 'no', 'okay'], 10)
    print res2
    word2 = ''
    if res2['error'] == None:
        word = res2['word']
        SpeechRecognitionProxy.pause(True)
        TowardShoulder(word2)
        configuration = {"bodyLanguageMode":"contextual"}
        animatedSpeechProxy.say(ClosingComplete, configuration)
        rh.humanoid_motion.goToPosture('Crouch', 0.3)
        rh.motion.disableMotors()
    else:
        SpeechRecognitionProxy.pause(True)
        rh.audio.speak("Can I touch your shoulder?")
        res2 = rh.audio.speechDetection(['yes', 'no', 'okay'], 10)
        print res2
        word2 = ''
        if res2['error'] == None:
            word2 = res2['word']
            TowardShoulder(word2)
            configuration = {"bodyLanguageMode":"contextual"}
            animatedSpeechProxy.say(ClosingComplete, configuration)
            rh.humanoid_motion.goToPosture('Crouch', 0.3)
            rh.motion.disableMotors()
        else:
            configuration = {"bodyLanguageMode":"contextual"}
            animatedSpeechProxy.say(Closing, configuration)
            rh.humanoid_motion.goToPosture('Crouch', 0.3)
            rh.motion.disableMotors()
############################################

############################################
#######   TowardShoulder FUNCTION   #######
############################################
# def TowardShoulder(word2):
#     touched_bodies = None
#     if word == 'yes' or word == 'okay':
#         print 'yes'
#         SpeechRecognitionProxy.pause(True)
#         rh.audio.speak("Okay! I will go and touch your shoulder now.")
#         global ReactToTouch
#         ReactToTouch = ReactToTouch("ReactToTouch")
#         ##### WHEN SENSOR IS TOUCHED, ASK TO TOUCH HUMAN #####
#         AngleAcc = 0
#         TimeAcc = 0.1
#         JointName = "LShoulderPitch"
#         while touched_bodies == None:
#                 AngleAcc = AngleAcc-0.1
#                 # TimeAcc = TimeAcc+0.1
#                 motionProxy.angleInterpolation(JointName, AngleAcc, TimeAcc, isAbsolute)
#         motionProxy.angleInterpolation(JointName, AngleAcc+0.1, 0.2, isAbsolute)
#         motionProxy.angleInterpolation(JointName, AngleAcc-0.1, 0.2, isAbsolute)
#         motionProxy.angleInterpolation(JointName, AngleAcc+0.1, 0.2, isAbsolute)
#         motionProxy.angleInterpolation(JointName, AngleAcc-0.1, 0.2, isAbsolute)
#         JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
#         Arm1 = [90, 0, 0, -2]
#         Arm1 = [ x * motion.TO_RAD for x in Arm1]
#         pFractionMaxSpeed = 0.3
#         motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
#         else:
#             time.sleep(10)
#             pass
#
#     elif word == 'no':
#         pass
############################################

############################################
########## FACE TRACKING FUNCTION ##########
############################################
def FaceTracking():
    global faceTrackingProxy
    global faceTrackingFlag
    global isFace
    global facePositionX
    global facePositionY
    global facePositionZ
    global motionProxy
    global faceProxy
    try:
        faceTrackingProxy = ALProxy("ALFaceTracker", IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALFaceTracker"
        print "Error was: ", e
    isFaceCount = 0
    faceTrackingProxy.startTracker()

    try:
        faceProxy = ALProxy("ALFaceDetection", IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALFaceDetection"
        print "Error was: ", e
    tracking_enabled = True
    # Enable or disable tracking.
    faceProxy.enableTracking(tracking_enabled)
############################################

############################################
######## NODDING IMITATION FUNCTION ########
############################################
def TouchOnShoulderr():
    global faceProxy
    global cont
    global isFace
    global facePositionX
    global facePositionY
    global facePositionZ
    global motionProxy
    global memory
    global touchTriggerred

    try:
      faceProxy = ALProxy("ALFaceDetection", IP, PORT)
    except Exception, e:
      print "Error when creating face detection proxy:"
      print str(e)
      exit(1)
    firstFlag = 1
    #### CHANGE PERIOD HERE ####
    period = 100
    faceProxy.subscribe("Test_Face", period, 0.0 )
    ############################
    memValue = "FaceDetected"
    tracking_enabled = True
    faceProxy.enableTracking(tracking_enabled)
    try:
      memoryProxy = ALProxy("ALMemory", IP, PORT)
    except Exception, e:
      print "Error when creating memory proxy:"
      print str(e)
      exit(1)
    round1 = 0
    cont = 1
    sameposition = 0
    framecount = 0
    position = []
    position2 = []
    framecount2 = 0
    roundcount = 0
    isAbsolute = True
    t0 = time.clock()
    val = memoryProxy.getData(memValue)
    if(val and isinstance(val, list) and len(val) >= 2):
    # We detected faces !
        faceInfoArray = val[1]
        try:
            faceInfo = faceInfoArray[0]
            faceShapeInfo = faceInfo[0]
            nothing = round(faceShapeInfo[0], 2)
            alpha = round(faceShapeInfo[1],2)*180/math.pi
            beta = round(faceShapeInfo[2],2)*180/math.pi
            sizeX = round(faceShapeInfo[3],2)*180/math.pi
            sizeY = round(faceShapeInfo[4],2)*180/math.pi
            faceExtraInfo = faceInfo[1]
            nosePoint = faceExtraInfo[7]
            ReferencePoint = round(nosePoint[1],2)
        except Exception, e:
            print "face detected, but it seems getData is invalid. ALValue ="
            print val
            print "Error msg %s" % (str(e))
        JointName = ["LShoulderPitch","LShoulderRoll"]
        angleLists = [[ReferencePoint+0.3],[0.3]]
        times      = [[1.5],[1.5]]
        motionProxy.angleInterpolation(JointName, angleLists, times, isAbsolute)
        rh.humanoid_motion.openHand('Left')

        AngleAcc = 0
        TimeAcc = 0.1
        JointName = "LShoulderPitch"

        # Subscribe to TouchChanged event:
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("TouchChanged","ReactToTouch","onTouched")

        CountTouchTriggered = len(touchTriggered)

        ######################################
        ######################################
        # while CountTouchTriggered == 0
        # ####SENSOR IS NOT TRIGGERED ####
        # ######################################
        # ######################################
        #     AngleAcc = AngleAcc-0.1
        #     TimeAcc = TimeAcc+0.1
        #     motionProxy.angleInterpolation(JointName, AngleAcc, TimeAcc, isAbsolute)
        # ######################################
        # JointName = ["LHand","LShoulderPitch","LShoulderRoll"]
        # angleLists = [["Close"],[1.5],[0]]
        # times      = [[0.2],[1.5],[1.5]]
        # motionProxy.angleInterpolation(JointName, angleLists, times, isAbsolute)
    else:
        print "Can't detect face"
############################################

############################################
######### DETECT TOUCHING FUNCTION #########
############################################
def onTouched(self, strVarName, value):
    """ This will be called each time a touch
    is detected."""
    # Unsubscribe to the event when talking,
    # to avoid repetitions
    memory.unsubscribeToEvent("TouchChanged",
        "ReactToTouch")
    global touchTriggerred
    touchTriggerred = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])

    # self.say(touchTriggerred)

    # # Subscribe again to the event
    # memory.subscribeToEvent("TouchChanged",
    #     "ReactToTouch",
    #     "onTouched")
############################################

############################################
######### Stop Lecturing FUNCTION ##########
############################################
def StopLecturing():
    global tts
    tts.stopAll()
############################################

############################################
####### Stop Face Detection FUNCTION #######
############################################
def StopFaceDetection():
    global faceProxy
    faceProxy.unsubscribe("Test_Face")
############################################

############################################
######## Stop Face Tracking FUNCTION #######
############################################
def StopFaceTracking():
    global faceTrackingProxy
    faceTrackingProxy.stopTracker()
############################################

############################################
########### Stop Motion FUNCTION ###########
############################################
def StopMotion():
    global motionProxy
    motionProxy.rest()
    motionProxy.killMove()
############################################

############################################
########### SET TRACKING FUNCTION ##########
############################################
def set_nao_face_detection_tracking(IP, PORT, tracking_enabled):
    global faceProxy
    faceProxy = ALProxy("ALFaceDetection", IP, PORT)
    # Enable or disable tracking.
    faceProxy.enableTracking(tracking_enabled)
    # Just to make sure correct option is set.
############################################

############################################
#######    ReactToTouch FUNCTION     #######
############################################
class ReactToTouch(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        # Subscribe to TouchChanged event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

    def onTouched(self, strVarName, value):
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("TouchChanged",
            "ReactToTouch")
        global touched_bodies
        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])
        self.say(touched_bodies)
        # Subscribe again to the event
        memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

    def say(self, bodies):
        if (bodies == []):
            return

        sentence = "My " + bodies[0]

        for b in bodies[1:]:
            sentence = sentence + " and my " + b

        if (len(bodies) > 1):
            sentence = sentence + " are"
        else:
            sentence = sentence + " is"
        sentence = sentence + " touched."

        # self.tts.say(sentence)
        print sentence
############################################

##################################################################################################################################

##################################################################################################################################
###################################################### MAIN FUNCTION ZONE ########################################################
##################################################################################################################################
############################################
####               MAIN                #####
############################################
def main():
    global Condition
    global postureProxy
    global motionProxy
    global trackerProxy
    global autonomousProxy
    global basic_awareness
    global SpeechRecognitionProxy
    global lifeProxy

    parser = OptionParser()
    parser.add_option("--pip",
        help = "Parent broker port. The IP address or your robot",
        dest = "pip")
    parser.add_option("--pport",
        help = "Parent broker port. The port NAOqi is listening to",
        dest = "pport",
        type = "int")
    parser.set_defaults(
        pip = IP,
        pport = PORT)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    rh.motion.enableMotors()
    motionProxy = ALProxy("ALMotion", IP, PORT)
    rh.humanoid_motion.goToPosture('Stand', 0.3)
    global AutonomousMoves
    AutonomousMoves = ALProxy("ALAutonomousMoves", IP, PORT)
    AutonomousMoves.setExpressiveListeningEnabled(False)
    AutonomousMoves.setBackgroundStrategy("none")

    # motionProxy.setStiffnesses('Body', 1.0)

    global Condition
    Condition = input("Enter Condition Choice (1 for Only Speaking, 2 for Speaking + FaceTracking, 3 for Speaking + NoddingImitation, 4 for Speaking + FaceTracking + NoddingImitation, 5 for Speaking + Gesture, 6 for Speaking + Gesture + FaceTracking+GazeShifting, 7 for Speaking + Gesture + NoddingImitation + NoddingInitiation, 8 for Speaking + Gesture + FaceTracking + GazeShifting + NoddingImitation + NoddingInitiation): ")
    global Content
    Content = input("Enter Content Choice: ")
    if Content == 1:
        Content = Content1
    elif Content == 2:
        Content = Content2
    elif Content == 3:
        Content = Content3
    elif Content == 4:
        Content = Content4
    elif Content == 5:
        Content = Content5
    elif Content == 6:
        Content = Content6
    elif Content == 7:
        Content = Content7
    elif Content == 8:
        Content = Content8
    elif Content == 9:
        Content = Content9

    if Condition == 1:
        process1 = threading.Thread(target = SpeakingOnly)
        process1.daemon = True
        process2 = threading.Thread(target = WordDetection)
        process2.daemon = True
        process1.start()
        process2.start()
    elif Condition == 2:
        process1 = threading.Thread(target = SpeakingOnly)
        process1.daemon = True
        process2 = threading.Thread(target = FaceTracking)
        process2.daemon = True
        process3 = threading.Thread(target = WordDetection)
        process3.daemon = True
        process1.start()
        process2.start()
        process3.start()
    elif Condition == 3:
        process1 = threading.Thread(target = SpeakingOnly)
        process1.daemon = True
        process2 = threading.Thread(target = HeadNoddingImitation)
        process2.daemon = True
        process3 = threading.Thread(target = WordDetection)
        process3.daemon = True
        process1.start()
        process2.start()
        process3.start()
    elif Condition == 4:
        autonomousProxy = ALProxy("ALAutonomousMoves", IP, PORT)
        process1 = threading.Thread(target = SpeakingOnly)
        process1.daemon = True
        process2 = threading.Thread(target = FaceTracking)
        process2.daemon = True
        process3 = threading.Thread(target = HeadNoddingImitation)
        process3.daemon = True
        process4 = threading.Thread(target = WordDetection)
        process4.daemon = True
        process1.start()
        process2.start()
        process3.start()
        process4.start()
    elif Condition == 5:
        autonomousProxy = ALProxy("ALAutonomousMoves", IP, PORT)
        process1 = threading.Thread(target = SpeakingWithGesture)
        process1.daemon = True
        process2 = threading.Thread(target = WordDetection)
        process2.daemon = True
        process1.start()
        process2.start()
    elif Condition == 6:
        autonomousProxy = ALProxy("ALAutonomousMoves", IP, PORT)
        process1 = threading.Thread(target = SpeakingWithGesture)
        process1.daemon = True
        process2 = threading.Thread(target = GazeBehaviour)
        process2.daemon = True
        process3 = threading.Thread(target = WordDetection)
        process3.daemon = True
        process1.start()
        process2.start()
        process3.start()
    elif Condition == 7:
        autonomousProxy = ALProxy("ALAutonomousMoves", IP, PORT)
        process1 = threading.Thread(target = SpeakingWithGesture)
        process1.daemon = True
        process2 = threading.Thread(target = HeadNoddingImitation)
        process2.daemon = True
        process3 = threading.Thread(target = HeadNoddingInitiation)
        process3.daemon = True
        process4 = threading.Thread(target = WordDetection)
        process4.daemon = True
        process1.start()
        process2.start()
        process3.start()
        process4.start()
    elif Condition == 8:
        autonomousProxy = ALProxy("ALAutonomousMoves", IP, PORT)
        process1 = threading.Thread(target = SpeakingWithGesture)
        process1.daemon = True
        process2 = threading.Thread(target = HeadNoddingImitation)
        process2.daemon = True
        process3 = threading.Thread(target = HeadNoddingInitiation)
        process3.daemon = True
        process4 = threading.Thread(target = GazeBehaviour)
        process4.daemon = True
        process5 = threading.Thread(target = WordDetection)
        process5.daemon = True
        process1.start()
        process2.start()
        process3.start()
        process4.start()
        process5.start()
    else:
        autonomousProxy = ALProxy("ALAutonomousMoves", IP, PORT)
        process1 = threading.Thread(target = SpeakingWithGesture)
        process1.daemon = True
        process2 = threading.Thread(target = WordDetection)
        process2.daemon = True
        process1.start()
        process2.start()
    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
##################################################################################################################################

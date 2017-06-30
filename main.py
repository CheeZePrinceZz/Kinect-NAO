# -*- coding: utf-8 -*-


#################### TODO
#- Threading Speaking and kinect


import kinecthandler as kinecthandler
import naocommander as naocommander
import converter as converter
import threading
from naoqi import ALProxy
from naoqi import ALModule
import sys
import time

##############################################################################
#                       TEST & SKELETON DISPLAY ZONE                         #
##############################################################################
#import controllingMethod as controllingMethod
#import SkeletonDisplay as SkeletonDisplay
#import threading

#if __name__ == '__main__':
#    SkeletonDisplay.BodyGameRuntime()
#    _sensor = kinecthandler.KinectHandler()
#    _avatar = naocommander.NAOCommander(robotIP, PORT)
#    kinect_test(_sensor, _avatar)

#process1 = threading.Thread(target = SkeletonDisplay.BodyGameRuntime())
#process1.daemon = True
#process2 = threading.Thread(target = controllingMethod.controllingMethod())
#process2.daemon = True
#process1.start()
#process2.start()
    # process3.start()
    # _sensor = process2
    # _avatar = process3
    # kinect_test(_sensor, _avatar)
###############################################################################


robotIP = "169.254.168.203"
PORT = 9559

nb_of_body = 1

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


def main():
    global Content
    global kinect_h
    global nao_c
    global flag
    flag = 0
    ContentChoice = input("Enter Content Part: ")
    if ContentChoice == 1:
        Content = Content1
    elif ContentChoice == 2:
        Content = Content2
    elif ContentChoice == 3:
        Content = Content3
    elif ContentChoice == 4:
        Content = Content4
    elif ContentChoice == 5:
        Content = Content5
    elif ContentChoice == 6:
        Content = Content6
    elif ContentChoice == 7:
        Content = Content7
    elif ContentChoice == 8:
        Content = Content8
    elif ContentChoice == 9:
        Content = Content9
    kinect_h = kinecthandler.KinectHandler()
    nao_c = naocommander.NAOCommander(robotIP, PORT)

    process1 = threading.Thread(target = MoveRobot)
    process1.daemon = True
    process2 = threading.Thread(target = Speaking)
    process2.daemon = True
    process1.start()
    process2.start()
    process2.join()

def MoveRobot():
    global flag
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
        flag = 1

def Speaking():
    global tts
    try:
        tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ",e
        sys.exit(1)
    tts.setParameter("pitchShift", 1.0)
    while flag != 1:
        time.sleep(1)
    time.sleep(3)
    tts.say(Content)
    time.sleep(3)
    motionproxy = ALProxy("ALMotion", robotIP, PORT)
    motionproxy.rest()


if __name__ == "__main__":
    main()
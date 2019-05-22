#!/usr/bin/env python
PKG = 'numpy_tutorial'
import roslib; roslib.load_manifest(PKG)

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import sys
sys.path=sys.path[3:]
import cv2
import numpy as np
import matplotlib.pyplot as plt

pub = rospy.Publisher('linear_vel_command', numpy_msg(Floats),queue_size=10)
def callback(data):
    print (rospy.get_name(), "I heard %s"%str(data.data))
    img = np.reshape(data.data,(256, 256, 3))
    plt.imsave('test1.png', img.astype(np.uint8))

    #do something (publish) the data received
    vel_zx=np.float32([-0.4,0.4])
    pub.publish(vel_zx)
    print("listener published" + str(vel_zx))
    #print(img.astype(np.uint8))
    #np.save("image_read",img)
    

def listener():
    rospy.init_node('listener')
    rospy.Subscriber("floats", numpy_msg(Floats), callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
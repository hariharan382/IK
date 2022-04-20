#!/usr/bin/env python3

import serial.tools.list_ports
import rospy

ports = list(serial.tools.list_ports.comports())

global port_name
for p in ports:
    p=str(p)
    if "USB" in p:
        #print(p.split())
        port_name=p.split()[0]

        rospy.set_param('arduino_port',port_name)
if rospy.has_rosparam('arduino_port'):
    print("usb is connected")

print(port_name)


"""<launch>
    <param name="myargs" value="1 0 0 0 0 0 1 link1_parent link1 100"/> <!-- or elsewhere -->
    <node pkg="tf" type="static_transform_publisher" name="link1_broadcaster" launch-prefix="/bin/bash -c '$* `rosparam get myargs`' --"/>
</launch>"""
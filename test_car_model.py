# -*- coding: utf-8 -*-
"""

"""

import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import car_model as cm

class CarTest(unittest.TestCase):
    def setUp(self):
        self.coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 
        self.car = cm.Car()
        pass

    def tearDown(self):
        pass

    def test_sens_1(self):
        self.pose = cm.Pose(450,300,np.pi)
        sens = self.car.get_sens(self.pose,self.coursePix)
        print("sens(L,R) = {0}".format(sens))
        self.assertEqual((0,0),sens)

    def test_sens_2(self):
        self.pose = cm.Pose(400,300,np.pi)
        sens = self.car.get_sens(self.pose,self.coursePix)
        print("sens(L,R) = {0}".format(sens))
        self.assertEqual((1,0),sens)

    def test_sens_3(self):
        self.pose = cm.Pose(380,300,np.pi)
        sens = self.car.get_sens(self.pose,self.coursePix)
        print("sens(L,R) = {0}".format(sens))
        self.assertEqual((1,1),sens)

    def test_sens_4(self):
        self.pose = cm.Pose(350,300,np.pi)
        sens = self.car.get_sens(self.pose,self.coursePix)
        print("sens(L,R) = {0}".format(sens))
        self.assertEqual((0,1),sens)

    def test_sens_5(self):
        self.pose = cm.Pose(335,240,np.pi/2.0)
        sens = self.car.get_sens(self.pose,self.coursePix)
        print("sens(L,R) = {0}".format(sens))
        self.assertEqual((0,0),sens)
        #self.plot_car()

    def test_sens_overarea(self):
        self.pose = cm.Pose(620,300,-np.pi/2.0)
        sens = self.car.get_sens(self.pose,self.coursePix)
        print("sens(L,R) = {0}".format(sens))
        self.assertEqual((0,0),sens)
        #self.plot_car()

    def plot_car(self):
        ax = plt.subplot(1, 1, 1)
        dv = self.pose.get_tf()
        print(dv)
        c_body  = dv @ self.car.body
        c_tireR = dv @ self.car.tireR
        c_tireL = dv @ self.car.tireL
        c_sensR = dv @ self.car.sensR
        c_sensL = dv @ self.car.sensL
        cm.drawCircle(ax, c_body , _fc='g')
        cm.drawCircle(ax, c_tireR, _fc='g')
        cm.drawCircle(ax, c_tireL, _fc='g')
        cm.drawCircle(ax, c_sensR, _fc='r', _r=2)
        cm.drawCircle(ax, c_sensL, _fc='r', _r=2)
        ax.set_xlabel("X [mm]")
        ax.set_ylabel("Y [mm]")
        plt.axis('scaled')
        ax.set_aspect('equal')
        ax.set_xlim([0,cm.WINDOW_W])
        ax.set_ylim([0,cm.WINDOW_H])
        ax.invert_yaxis()
        ax.grid()
        plt.show()

if __name__ == "__main__":
    unittest.main()


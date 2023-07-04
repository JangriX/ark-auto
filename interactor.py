import pygetwindow
import settings
from PIL import ImageGrab
import win32gui
import cv2
import numpy as np
import pyautogui
import random
import time
import win32com.client

class Interactor:

    def __init__(self):
        self.process = pygetwindow.getWindowsWithTitle(settings.EMULATOR_TITLE)[0]._hWnd 
        self.images = {}
        self.orb = cv2.ORB_create(fastThreshold=5, edgeThreshold=1)
        # self.cache_images()
        self.win_pos = (0,0)
        self.shell = win32com.client.Dispatch("WScript.Shell")

    def cache_images(self):
        for img_id in settings.IMAGES.keys():
            target = cv2.cvtColor(cv2.imread(settings.IMAGES[img_id]), cv2.COLOR_RGB2BGR)
            # target_edge = cv2.Canny(target, settings.LT, settings.UT)
            kp, des = self.orb.detectAndCompute(target,None)
            self.images[img_id] = {
                "kp": kp,
                "des": des,
                "shape": target.shape,
                "img": target
            }

    def take_game_screenshot(self):
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.process)
        time.sleep(0.01)
        bounds = win32gui.GetWindowRect(self.process)
        adjusted_bounds = tuple(map(lambda x: x*settings.SCREEN_SCALING,bounds))
        self.win_x, self.win_y = (bounds[0],bounds[1])
        return ImageGrab.grab(bounds)

    def find_image_adv(self, img_id):
        screen = cv2.cvtColor(np.array(self.take_game_screenshot()), cv2.COLOR_RGB2BGR)
        # screen_edge = cv2.Canny(screen, settings.LT, settings.UT)


        s_kp, s_des = self.orb.detectAndCompute(screen,None)

        # print(s_des)
        # print(self.images[img_id]["des"])
        # print(self.images[img_id])

        matches = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(s_des,self.images[img_id]["des"])
        
        # heat_map = cv2.matchTemplate(screen, target, cv2.TM_SQDIFF_NORMED)

        # h, w, _ = target.shape

        matches = sorted(matches, key = lambda x:x.distance)

        img3 = cv2.drawMatches(screen,s_kp,self.images[img_id]["img"],self.images[img_id]["kp"],matches[:20],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imwrite("baaa.png", img3)
        cv2.imshow(img3)

        time.sleep(1000)
        0/0
        # cv2.imwrite("aaa.png", screen)
        # cv2.imshow('target', target_edge)
        # _, confidence, _, loc = cv2.minMaxLoc(heat_map)
        # x, y = loc
        if (confidence > settings.CC):
            return self.find_clickable_point(((x,y), (x+w, y+h)))
        else:
            return False

    def find_image(self, img_id):
        screen = cv2.cvtColor(np.array(self.take_game_screenshot()), cv2.COLOR_RGB2BGR)
        target = cv2.imread(settings.IMAGES[img_id])

        # cv2.imshow('kek',screen)
        # cv2.waitKey(0)


        heat_map = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
        h, w, _ = target.shape

        # cv2.imshow('screen2', screen)

        # cv2.imshow('target', target_edge)
        # cv2.waitKey(0)

        # cv2.destroyAllWindows()




        _, confidence, _, loc = cv2.minMaxLoc(heat_map)
        x, y = loc

        # loc = np.where(heat_map >= settings.CC)

        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(screen,pt,(pt[0]+w, pt[1]+h),(0,255,255),1)

        # cv2.imshow('detected',screen)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if (confidence > settings.CC):
            return self.find_clickable_point(((x,y), (x+w, y+h)))
        else:
            return False
    
    def find_image_with_edge(self, img_id):
        screen = cv2.cvtColor(np.array(self.take_game_screenshot()), cv2.COLOR_RGB2BGR)
        target = cv2.imread(settings.IMAGES[img_id])

        screen_edge = cv2.Canny(screen, settings.LT, settings.UT)
        target_edge = cv2.Canny(target, settings.LT, settings.UT)

        heat_map = cv2.matchTemplate(screen_edge, target_edge, cv2.TM_CCOEFF_NORMED)
        h, w, _ = target.shape

        # cv2.imshow('screen2', screen)

        # cv2.imshow('target', target_edge)
        # cv2.waitKey(0)

        # cv2.destroyAllWindows()

        _, confidence, _, loc = cv2.minMaxLoc(heat_map)
        x, y = loc
        if (confidence > settings.CC):
            return self.find_clickable_point(((x,y), (x+w, y+h)))
        else:
            return False

    def find_clickable_point(self, bounds):
        x1 = bounds[0][0] #+ self.win_x
        y1 = bounds[0][1] #+ self.win_y
        x2 = bounds[1][0] #+ self.win_x
        y2 = bounds[1][1] #+ self.win_y

        return (self.norm_rp(x1,x2),self.norm_rp(y1,y2))

    # normalized_random_point
    def norm_rp(self,min,max):
        return (self.rp(min,max)+self.rp(min,max))/2

    def rp(self,min,max):
        return random.randint(min,max)

    def click_on(self, img_id, with_edge=False):
        if (with_edge):
            try:
                x, y = self.find_image_with_edge(img_id)
            except TypeError:
                # print("Not Found")
                return False
        else:
            try:
                x, y = self.find_image(img_id)
            except TypeError:
                # print("Not Found")
                return False
           
        # pyautogui.moveTo(x, y)
        pyautogui.click(x, y)
        return True

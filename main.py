from interactor import Interactor
import settings
import time
import random

i = Interactor()



# i.click_on("START")

go = True
while go:
    for img in settings.IMAGES:
        res = i.click_on(img, True)
        if (res):
            print(img)
            if (img == "OOS"):
                go = False
                print("OUT OF SANITY, EXITING")
            elif (img == "START"):
                print(f"STARTING")
                time.sleep(random.randint(0,2000)/1000)
                res2 = i.click_on("OP_SELECT")
                if (res2 == False):
                    res3 = i.click_on("OOS")
                    if (res3 == True):
                        go = False
                        print("OUT OF SANITY, EXITING")
            elif (img == "WIN3"):
                print("WON")
                time.sleep(7+random.randint(0,2000)/1000)
                i.click_on("START")
                time.sleep(1+random.randint(0,2000)/1000)
                i.click_on("OP_SELECT")
            break
        else:
            pass
            # print(f"{img} MISSED")
    a = random.randint(0,4)
    b = random.randint(0,1000)/1000
    rand = a+b
    time.sleep(settings.ACTION_DELAY+rand)
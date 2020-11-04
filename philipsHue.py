import os, sys
import requests
import time
import json
import colorama
import termcolor
import traceback
import threading
import tkinter


def crachReport(traceback):
    filename = time.strftime("%A_%d_%B_%Y__%H-%M-%S")
    if os.path.exists(sys.path[0] + "\\data\\crash"):
        pass
    else:
        os.mkdir(sys.path[0] + "\\data\\crash")
    with open(sys.path[0]+"\\data\\crash\\crash_"+filename+".txt", "w") as data:
        data.write(traceback)
    return traceback


def requestJson():
    r = requests.get("https://discovery.meethue.com")
    if len(r.json()) >= 2:
        colorama.init()
        i=0
        for elt in r.json():
            i+=1
            print(colorama.Fore.RED + "{n}".format(n=i) + colorama.Fore.RESET + " id: {} => ip: {}".format(elt["id"], elt["internalipaddress"]))
        colorama.deinit()
        while 1:
            try:
                choiceBridge = int(input("Which bridge?\n"))
                if choiceBridge-1 in range(0, len(r.json())):
                    rd = r.json()[choiceBridge-1]
                    break
                else:
                    colorama.init()
                    raise Exception(colorama.Fore.RED+"Number out of range"+colorama.Fore.RESET)
                    colorama.deinit()
            except Exception:
                print(crachReport(traceback.format_exc()))
                os.system("pause")
                sys.exit()
    else:
        rd = r.json()[0]
    return rd

try:
    if os.path.exists(sys.path[0] + "\\data\\hueInfos\\"):
        pass
    elif os.path.exists(sys.path[0] + "\\data\\"):
        os.mkdir(sys.path[0]+"\\data\\hueInfos")
    else:
        os.mkdir(sys.path[0]+"\\data")
        os.mkdir(sys.path[0]+"\\data\\hueInfos")
    
    rd=requestJson()
    While=True
    while While:
        try:
            with open(sys.path[0]+"\\data\\hueInfos\\token.json", "r") as data:
                t = json.load(data)
            tokName = input("Token name: ").lower()
            try:
                testvar = t[tokName]
                del testvar
                break
            except Exception:
                print("Invalid token name.")
                continue
        except Exception as e:
            print(e)
            while 1:
                try:
                    tokName = input("Token name: ").lower()
                    tok = input("Token: ")
                    print(requests.get("http://{}/api/{}/lights/".format(rd["internalipaddress"], tok)))
                    t = {tokName:{"username":tok}}
                    with open(sys.path[0]+"\\data\\hueInfos\\token.json", "w") as data:
                        data.write(json.dumps(t))
                    While=False
                    break
                except Exception as e:
                    print(e)
                    continue
except IndexError as ie:
    print("'https://discovery.meethue.com' : "+str(requests.get("https://discovery.meethue.com").json()))
    print("Bridge not found.\n\n"+str(crachReport(traceback.format_exc())))
    os.system("pause")
    sys.exit()
except Exception:
    print(crachReport(traceback.format_exc()))
    os.system("pause")
    sys.exit()

def sensorsSwitch():
    time.sleep(1)
    os.system("cls")
    sensorId = input("Sensor ID: ")
    try:
        while 1:
            state = requests.get("http://{}/api/{}/sensors/{}".format(rd["internalipaddress"], t[tokName]["username"], sensorId)).json()["state"]["presence"]
            print(state)
            while 1:
                if state == False:
                    if requests.get("http://{}/api/{}/sensors/{}".format(rd["internalipaddress"], t[tokName]["username"], sensorId)).json()["state"]["presence"] == state:
                        pass
                    elif requests.get("http://{}/api/{}/sensors/{}".format(rd["internalipaddress"], t[tokName]["username"], sensorId)).json()["state"]["presence"] != state:
                        break
                elif state == True:
                    if requests.get("http://{}/api/{}/sensors/{}".format(rd["internalipaddress"], t[tokName]["username"], sensorId)).json()["state"]["presence"] == state:
                        pass
                    elif requests.get("http://{}/api/{}/sensors/{}".format(rd["internalipaddress"], t[tokName]["username"], sensorId)).json()["state"]["presence"] != state:
                        time.sleep(20)
                        break
    except KeyboardInterrupt:
        pass

while 1:
    try:
        sensors=False
        os.system("cls")

        lreq = requests.get("http://{}/api/{}/lights/".format(rd["internalipaddress"], t[tokName]["username"]))
        num=0
        colorama.init()
        while num<len(lreq.json()):
            num+=1
            espace = (50 - (len(str(num))+6)) - len(lreq.json()[str(num)]["name"])
            if espace < 1:
                espace = " "
            else:
                espace = espace * " "
            if lreq.json()[str(num)]["state"]["on"]:
                lOn = colorama.Fore.GREEN + "On" + colorama.Fore.RESET
            else:
                lOn = colorama.Fore.RED + "Off" + colorama.Fore.RESET
            print(colorama.Fore.RED + "{}  --  ".format(num) + colorama.Fore.RESET + "{}{}{}".format(lreq.json()[str(num)]["name"], espace, lOn))
        colorama.deinit()
        while 1:
            try:
                lightId = input("Light id: ")
                if lightId.lower() == "stop":
                    sys.exit()
                elif lightId.lower() == "sensors":
                    sensorsSwitch()
                    sensors=True
                    break
                else:
                    lightId = int(lightId)
                if requests.get("http://{}/api/{}/lights/{}".format(rd["internalipaddress"], t[tokName]["username"], lightId)).json()[0]["error"]:
                    raise IndentationError("Light not found.")
            except KeyError:
                break
            except Exception as e:
                print(e)
                continue
        if sensors:
            continue
    except Exception:
        print(crachReport(traceback.format_exc()))
        os.system("pause")
        sys.exit()

    alr_false = False
    while 1:
        try:
            state = str(input("On/Off ? "))
            if state.lower() == "on":
                while 1:
                    try:
                        bri = input("Light lvl: ")
                        if bri.lower() == "max":
                            bri = 254
                        elif bri.lower() == "min":
                            bri = 1
                        else:
                            bri = int(bri)
                        if bri in range(1, 255):
                            break
                        else:
                            raise IndentationError("The light lvl must be between 1 and 254.")
                    except Exception as e:
                        print(e)
                        continue
                stateb = True
            elif state.lower() == "off":
                stateb = False
            else:
                raise Exception("Please enter a good answer.")
                continue
        except Exception as e:
            print(e)
            continue
        try:
            r = requests.get("http://{}/api/{}/lights/".format(rd["internalipaddress"], t[tokName]["username"]))
            if r.json()[str(lightId)]["state"]["on"] == stateb:
                if stateb == True:
                    alr_false = False
                    message = json.dumps({"bri": bri})
                elif stateb == False:
                    alr_false = True
                    print("The light is already off.")
                    time.sleep(2)
                    break
            elif stateb == False:
                message = json.dumps({"on": stateb})
            elif stateb == True:
                print(str(bri))
                message = json.dumps({"on": stateb, "bri":bri})
            if stateb:
                stat = "On"
            else:
                stat = "Off"
            print("Light status: " + str(stateb))
            break
            # os.system("pause")
        except Exception:
            print(crachReport(traceback.format_exc()))
            os.system("pause")
            sys.exit()
    if alr_false:
        continue

    try:
        lUrl = "http://{}/api/{}/lights/{}/state".format(rd["internalipaddress"], t[tokName]["username"], lightId)

        requests.put(lUrl, data=message)
        time.sleep(1)
    except NameError:
        continue
    except Exception as e:
        print(e)
        continue
""" home.py - Fabricate.IO

    This is a demo python file showing what can be done with the debounce_handler.
    The handler prints True when you say "Alexa, device on" and False when you say
    "Alexa, device off".

    If you have two or more Echos, it only handles the one that hears you more clearly.
    You can have an Echo per room and not worry about your handlers triggering for
    those other rooms.

    The IP of the triggering Echo is also passed into the act() function, so you can
    do different things based on which Echo triggered the handler.
"""

import fauxmo
import logging
import time
import json
import serial
import os

from debounce_handler import debounce_handler

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
ir_serial = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)

class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"lights": 52000, "tv": 52001, "aircon": 52002}
    IRDIR = "/data/irmcli/"

    def act(self, client_address, state, name):
        logging.info("State", state, "on", name, "from client @", client_address)
        if name == "lights":
            self.playLights(state)
        if name == "aircon":
            self.playAircon(state)
        elif name == "tv":
            self.playTv(state)
        elif name == "offtimer":
            self.playOffTimer(state)
        return True

    def playIR(self, path):
        if path and os.path.isfile(path):
            logging.debug("Playing IR with %s ..." % path)
            f = open(path)
            data = json.load(f)
            f.close()
            recNumber = len(data['data'])
            rawX = data['data']

            ir_serial.write("n,%d\r\n" % recNumber)
            ir_serial.readline()

            postScale = data['postscale']
            ir_serial.write("k,%d\r\n" % postScale)
            #time.sleep(1.0)
            msg = ir_serial.readline()
            #print msg

            for n in range(recNumber):
                bank = n / 64
                pos = n % 64
                if (pos == 0):
                    ir_serial.write("b,%d\r\n" % bank)

                ir_serial.write("w,%d,%d\n\r" % (pos, rawX[n]))

            ir_serial.write("p\r\n")
            msg = ir_serial.readline()
            logging.debug(msg)
            #ir_serial.close()
        else:
            logging.debug("Playing IR...")
            ir_serial.write("p\r\n")
            time.sleep(1.0)
            msg = ir_serial.readline()
            logging.debug(msg)

    def playLights(self, state):
        if state == True:
            self.playIR(self.IRDIR + "light_on.json")
        else:
            self.playIR(self.IRDIR + "light_off.json")
        return True

    def playAircon(self, state):
        if state == True:
            self.playIR(self.IRDIR + "air_on.json")
        else:
            self.playIR(self.IRDIR + "air_off.json")
        return True

    def playTv(self, state):
        self.playIR(self.IRDIR + "tv_toggle.json")
        return True

    def playOffTimer(self, state):
        if state == True:
            self.playIR(self.IRDIR + "tv_toggle.json")
        else:
            self.playIR(self.IRDIR + "tv_quick.json")
            time.sleep(0.5)
            self.playIR(self.IRDIR + "tv_down.json")
            self.playIR(self.IRDIR + "tv_down.json")
            self.playIR(self.IRDIR + "tv_enter.json")
            time.sleep(0.5)
            self.playIR(self.IRDIR + "tv_down.json")
            self.playIR(self.IRDIR + "tv_enter.json")
            time.sleep(0.5)
            self.playIR(self.IRDIR + "tv_down.json")
            self.playIR(self.IRDIR + "tv_down.json")
            self.playIR(self.IRDIR + "tv_enter.json")
            time.sleep(0.5)
            self.playIR(self.IRDIR + "tv_vol_down.json")
            self.playIR(self.IRDIR + "tv_vol_down.json")
            self.playIR(self.IRDIR + "tv_vol_down.json")
            self.playIR(self.IRDIR + "tv_vol_down.json")
            self.playIR(self.IRDIR + "tv_vol_down.json")
            self.playIR(self.IRDIR + "tv_vol_down.json")
        return True

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break

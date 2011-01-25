import messages
import sys
import time
import struct

class Server:

    menuVibrationTime = 5
    is24HourClock = True
    __server = None
    __client = None

    def __init__(self):
        self.testPng = open("test.png").read()

    def start(self):
        try:
            import bluetooth
        except:
            print >>sys.stderr, "Python module pybluez not installed."
            sys.exit(1)
        try:
            self.__server = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            self.__server.bind(("",1))
            self.__server.listen(1)
            bluetooth.advertise_service(self.__server, "LiveView", service_classes = [ bluetooth.SERIAL_PORT_CLASS ], profiles = [ bluetooth.SERIAL_PORT_PROFILE ] )
        except:
            print >>sys.stderr, "Could not start a bluetooth server."
            sys.exit(2)
        self.__client, address = self.__server.accept()
        self.__client.send(messages.EncodeGetCaps())
        self.loop()

    def __del__(self):
        if self.__server:
            self.__server.close()
        if self.__client:
            self.__client.close()

    def send(self, msg):
        self.__client.send(msg)

    def loop(self):
        while True:
            for msg in messages.Decode(self.__client.recv(4096)):
                if isinstance(msg, messages.Result):
                    if msg.code != messages.RESULT_OK:
                        print "---- NON-OK result received ----"
                        print msg
                        continue

                self.send(messages.EncodeAck(msg.messageId))

                if isinstance(msg, messages.GetMenuItems):
                    self.send(messages.EncodeGetMenuItemResponse(0, True, 0, "Menu0", self.testPng))
                    self.send(messages.EncodeGetMenuItemResponse(1, False, 20, "Menu1", self.testPng))
                    self.send(messages.EncodeGetMenuItemResponse(2, False, 0, "Menu2", self.testPng))
                    self.send(messages.EncodeGetMenuItemResponse(3, True, 0, "Menu3", self.testPng))

                elif isinstance(msg, messages.GetMenuItem):
                    print "---- GetMenuItem received ----"
                    # FIXME: do something!

                elif isinstance(msg, messages.DisplayCapabilities):
                    deviceCapabilities = msg
                    self.send(messages.EncodeSetMenuSize(4))
                    self.send(messages.EncodeSetMenuSettings(self.menuVibrationTime, 0))

                elif isinstance(msg, messages.GetTime):
                    self.send(messages.EncodeGetTimeResponse(time.time(), self.is24HourClock))

                elif isinstance(msg, messages.DeviceStatus):
                    self.send(messages.EncodeDeviceStatusAck())

                elif isinstance(msg, messages.GetAlert):
                    self.send(messages.EncodeGetAlertResponse(20, 4, 15, "TIME", "HEADER", "01234567890123456789012345678901234567890123456789", self.testPng))

                elif isinstance(msg, messages.Navigation):
                    self.send(messages.EncodeNavigationResponse(messages.RESULT_EXIT))

#                    self.send(messages.EncodeSetMenuSize(0))
#                    self.send(messages.EncodeClearDisplay())
#                    self.send(messages.EncodeDisplayBitmap(100, 100, self.testPng))
#                    self.send(messages.EncodeSetScreenMode(50, False))
#                    self.send(messages.EncodeDisplayText("WOOOOOOOOOOOO"))

#                    self.send(messages.EncodeLVMessage(31, ""))

#                    self.send(messages.EncodeSetScreenMode(0, False))
#                    self.send(messages.EncodeClearDisplay())
#                    self.send(messages.EncodeLVMessage(48, struct.pack(">B", 38) + "moo"))

#                    tmpxxx = "MOOO"
#                    self.send(messages.EncodeSetMenuSize(4))
#                    self.send(messages.EncodeDisplayText("moo"))

#                    self.send(messages.EncodeSetStatusBar(tmp.menuItemId, 200, self.testPng))
#                    self.send(EncodeLVMessage(5, messages.EncodeUIPayload(isAlertItem, totalAlerts, unreadAlerts, curAlert, menuItemId, top, mid, body, itemBitmap)))

                    if msg.navType == messages.NAVTYPE_DOWN:
                        if not msg.wasInAlert:
                            self.send(messages.EncodeDisplayPanel("TOOOOOOOOOOOOOOOOOP", "BOTTTTTTTTTTTTTTTTTOM", self.testPng, False))
#                        self.send(messages.EncodeNavigationAck(messages.RESULT_OK))
#                        self.send(messages.EncodeDisplayText("ADQ WOS HERE"))
#                    elif tmp.navType == messages.NAVTYPE_SELECT:
#                        self.send(messages.EncodeNavigationAck(messages.RESULT_EXIT))
#                    self.send(messages.EncodeSetVibrate(1, 1000))
                print msg

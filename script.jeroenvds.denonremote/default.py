import xbmc
import xbmcgui
import telnetlib
import time
from xbmcaddon import Addon
import json

__addon__ = Addon()
ADDON_ID = __addon__.getAddonInfo('id')
KODI_VERSION_MAJOR = int(xbmc.getInfoLabel('System.BuildVersion')[0:2])

monitor = xbmc.Monitor()

def log(msg):
    xbmc.log("%s: %s" %(ADDON_ID, msg))

class DenonWatcher(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def turnOnDenon(self):
        log('Turn on Denon')
        try:
            tn = telnetlib.Telnet(__addon__.getSetting("denonip"))
            tn.write(b"ZMON\r")
            time.sleep(1)
            tn.write(str.encode("SI" + __addon__.getSetting("denoninput") + "\r"))
            #print tn.read_eager()
            tn.close()
        except Exception as error:
            xbmc.log(ADDON_ID +': ' + str(error), xbmc.LOGERROR)

    def changeVolumeDenon(self, volume):
        if volume > 98:
            volume = 98
        elif volume < 0:
            volume = 0
        log('Change Volume on Denon')
        try:
            tn = telnetlib.Telnet(__addon__.getSetting("denonip"))
            tn.write(str.encode("MV" + "{0:02d}".format(volume) + "\r"))
            tn.close()
        except Exception as error:
            xbmc.log(ADDON_ID +': ' + str(error), xbmc.LOGERROR)

    def onNotification(self, sender, method, data):
        if method == "Player.OnPlay":
            self.turnOnDenon()
        elif method == "Application.OnVolumeChanged":
            dataDecoded = json.loads(data)
            self.changeVolumeDenon(dataDecoded['volume'])

"""
class PlayerWhichStartsDenon(xbmc.Player):

    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        
    def onAVStarted(self):
        tn = telnetlib.Telnet(__addon__.getSetting("denonip"))
        tn.write(b"ZMON\r")
        time.sleep(1)
        tn.write(str.encode("SI" + __addon__.getSetting("denoninput") + "\r"))
        #print tn.read_eager()
        tn.close()
"""

def abort_requested():
    if KODI_VERSION_MAJOR > 13:
        return monitor.abortRequested()
    return xbmc.abortRequested

def wait_for_abort(seconds):
    if KODI_VERSION_MAJOR > 13:
        return monitor.waitForAbort(seconds)
    for _ in range(0, seconds * 1000 / 200):
        if xbmc.abortRequested:
            return True
        xbmc.sleep(200)
    return False

def main():
    watcher = None

    while not abort_requested():
        if watcher is None:
            watcher = DenonWatcher()
        if wait_for_abort(100):
            # Abort was requested while waiting. We should exit
            break

if __name__ == '__main__':
    main()

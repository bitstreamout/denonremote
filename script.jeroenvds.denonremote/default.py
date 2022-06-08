import xbmc
import telnetlib
import time
import xbmcaddon
import json

__addon__ = xbmcaddon.Addon(id='script.jeroenvds.denonremote')

def turnOnDenon():
	tn = telnetlib.Telnet(__addon__.getSetting("denonip"))
	tn.write(str.encode("ZMON\r"))
	time.sleep(1)
	tn.write(str.encode("SI"+__addon__.getSetting("denoninput")+"\r"))
	#print tn.read_eager()
	tn.close()

def changeVolumeDenon(volume):
	if volume > 98:
		volume = 98
	elif volume < 0:
		volume = 0
		
	tn = telnetlib.Telnet(__addon__.getSetting("denonip"))	
	tn.write(str.encode("MV"+"{0:02d}".format(volume)+"\r"))
	tn.close()

class DenonWatcher(xbmc.Monitor):
	def __init__(self, *args, **kwargs):
		xbmc.Monitor.__init__(self)
				
	def onNotification(self, sender, method, data):
		if method == "Player.OnPlay":
			turnOnDenon()
		elif method == "Player.OnVolumeChanged":
			dataDecoded = json.loads(data)
			changeVolumeDenon(dataDecoded['volume'])


class PlayerWhichStartsDenon(xbmc.Player):
	def onPlayBackStarted(self):
		tn = telnetlib.Telnet(__addon__.getSetting("denonip"))
		tn.write(str.encode("ZMON\r"))
		time.sleep(1)
		tn.write(str.encode("SI"+__addon__.getSetting("denoninput")+"\r"))
		#print tn.read_eager()
		tn.close()

def main():
	#player = PlayerWhichStartsDenon()
	monitor = DenonWatcher()
	watchout = xbmc.Monitor()

	while not watchout.abortRequested():
		if watchout.waitForAbort(60000):
			# Abort was requested while waiting. We should exit
			break

if __name__ == '__main__':
	main()

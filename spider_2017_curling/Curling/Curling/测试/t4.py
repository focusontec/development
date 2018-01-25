a = "http://odf2.worldcurling.co/data/WUNI2017P/play_by_play/1737/10-4.jpg"
import requests

status = requests.head(a)
print status.headers
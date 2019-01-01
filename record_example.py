from gamepy import Recorder
from pynput.keyboard import KeyCode, Key

pause_keys='pause'
terminate_keys='end'
start_keys='home'

rec = Recorder(['up','left','down','right'], pause_keys=pause_keys, terminate_keys=terminate_keys, start_keys=start_keys)

print('Press %s to start the recording, %s to pause the recording, and %s to terminate the recording.' %(str(start_keys), str(pause_keys), str(terminate_keys)))

large_bbox = [0,0,1920,1080]

rec.record('./test/image.png', process=True, height=299, grayscale=False)

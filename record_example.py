from gamepy import Recorder

start_keys='home'
pause_keys='pause'
terminate_keys='end'

rec = Recorder(['up','left','down','right'], start_keys=start_keys, pause_keys=pause_keys, terminate_keys=terminate_keys)

print('Press %s to start the recording, %s to pause the recording, and %s to terminate the recording.' %(str(start_keys), str(pause_keys), str(terminate_keys)))

rec.record('./test/image.png', process=True, height=299, grayscale=False)

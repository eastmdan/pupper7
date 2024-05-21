import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        print(f"Device {i}: {device_info.get('name')}, "
              f"Input Channels: {device_info.get('maxInputChannels')}, "
              f"Output Channels: {device_info.get('maxOutputChannels')}")
    p.terminate()

list_audio_devices()





# pip install pyaudio
# sudo apt-get install portaudio19-dev python3-pyaudio
# python3 list_audio_devices.py

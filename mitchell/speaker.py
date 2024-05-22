import pyaudio
from pydub import AudioSegment
import io

def play_audio(file, device_id):
    file_path = f'/home/ubuntu/pupper7/mitchell/sounds/{file}.mp3'
    
    # Open the audio file
    audio = AudioSegment.from_file(file_path, format="mp3")

    # Instantiate PyAudio
    p = pyaudio.PyAudio()

    # Open a stream using the specified device
    stream = p.open(format=p.get_format_from_width(audio.sample_width),
                    channels=audio.channels,
                    rate=audio.frame_rate,
                    output=True,
                    output_device_index=f"/dev/video{device_id}")

    # Read data in chunks
    chunk = 1024
    data = audio.raw_data

    # Play the audio file
    with io.BytesIO(data) as f:
        while chunk_data := f.read(chunk):
            stream.write(chunk_data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()

# Example usage
file = 'hello'
## audio_file = f'/home/ubuntu/pupper7/mitchell/sounds/{file}.mp3'
usb_device_id = 1  # Replace with your USB sound device index

play_audio(file, usb_device_id)

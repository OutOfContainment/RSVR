import time
import wave
import pyaudio
from status import Status


class Sound:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    def record():
        with wave.open(f"records/recording_{Status.curTrackAmount+1}.wav", 'wb') as wf:
            audio = pyaudio.PyAudio()
            wf.setnchannels(Sound.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(Sound.FORMAT))
            wf.setframerate(Sound.RATE)

            stream = audio.open(format=Sound.FORMAT, channels=Sound.CHANNELS,
                                rate=Sound.RATE, input=True)

            print("Sound: Start recording")
            while Status.recording:
                while Status.paused:
                    time.sleep(0.01)
                wf.writeframes(stream.read(Sound.CHUNK))

#              GUI.timer.config(text=f"{hours:02d}:{min:02d}:{sec:02d}")

        stream.close()
        audio.terminate()

    def play():
        with wave.open(f"records/recording_{Status.curTrack}.wav", 'rb') as wf:
            audio = pyaudio.PyAudio()

            stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True)

            while Status.playing and len(data := wf.readframes(Sound.CHUNK)):
                while Status.paused:
                    time.sleep(0.01)
                stream.write(data)

        stream.close()
        audio.terminate()
        Status.playing = False

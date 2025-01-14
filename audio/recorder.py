import threading
import wave
import pyaudio
from utils.logger import setup_logger

logger = setup_logger(__name__)

class AudioRecorder:
    def __init__(
        self,
        device_index: int = None,
        channels: int = 2,
        rate: int = 48000,
        chunk: int = 512,
        format_type=pyaudio.paInt16,
    ):
        self.device_index = device_index
        self.CHUNK = chunk
        self.FORMAT = format_type
        self.CHANNELS = channels
        self.RATE = rate

        self.recording = False
        self.frames = []
        self.audio_thread = None

    def start_recording(self):
        """Start recording"""
        try:
            self.recording = True
            self.frames = []
            self.audio_thread = threading.Thread(target=self._record_audio)
            self.audio_thread.start()
            logger.info("Recording started")
        except Exception as e:
            logger.error(f"Failed to start recording: {str(e)}")
            raise

    def stop_recording(self):
        """Stop recording"""
        self.recording = False
        if self.audio_thread:
            self.audio_thread.join()
        logger.info("Recording stopped")

    def _record_audio(self):
        """Recording thread: Continuously read audio and append to self.frames"""
        p = pyaudio.PyAudio()
        stream = None
        try:
            stream = p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.CHUNK,
            )
            logger.info(f"Audio stream opened, device index: {self.device_index}")

            while self.recording:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)

        except Exception as e:
            logger.error(f"Error during recording: {str(e)}")
        finally:
            if stream is not None:
                try:
                    stream.stop_stream()
                    stream.close()
                except Exception as e:
                    logger.error(f"Error closing audio stream: {str(e)}")
            p.terminate()

    def save_recording(self, filename="temp_recording.wav"):
        """Save recording to a .wav file"""
        if not self.frames:
            logger.warning("No recording data available")
            return None

        try:
            p = pyaudio.PyAudio()
            wf = wave.open(filename, "wb")
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))
            wf.close()
            p.terminate()

            logger.info(f"Recording saved to: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving recording: {str(e)}")
            return None


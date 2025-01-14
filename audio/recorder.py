# audio/recorder.py
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
        """開始錄音"""
        try:
            self.recording = True
            self.frames = []
            self.audio_thread = threading.Thread(target=self._record_audio)
            self.audio_thread.start()
            logger.info("開始錄音")
        except Exception as e:
            logger.error(f"啟動錄音失敗: {str(e)}")
            raise

    def stop_recording(self):
        """停止錄音"""
        self.recording = False
        if self.audio_thread:
            self.audio_thread.join()
        logger.info("停止錄音")

    def _record_audio(self):
        """錄音子執行緒：連續讀取音訊並寫入 self.frames"""
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
            logger.info(f"音頻流已開啟，裝置索引: {self.device_index}")

            while self.recording:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)

        except Exception as e:
            logger.error(f"錄音過程出錯: {str(e)}")
        finally:
            if stream is not None:
                try:
                    stream.stop_stream()
                    stream.close()
                except Exception as e:
                    logger.error(f"關閉音頻流時出錯: {str(e)}")
            p.terminate()

    def save_recording(self, filename="temp_recording.wav"):
        """保存錄音至 .wav 檔案"""
        if not self.frames:
            logger.warning("沒有錄音數據")
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

            logger.info(f"錄音已保存到: {filename}")
            return filename
        except Exception as e:
            logger.error(f"保存錄音時出錯: {str(e)}")
            return None


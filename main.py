# main.py
import os
import time  # 新增匯入 time 模組
from utils.logger import setup_logger
from audio.recorder import AudioRecorder
from db.connection import create_db_connection
from db.langchain_setup import setup_langchain
from db.process_query import process_query
from transcriber.whisper import transcribe_audio
from openai import OpenAI
import pyaudio

logger = setup_logger(__name__)

def voice_interactive_mode(db, chain, openai_client, recorder: AudioRecorder):
    """
    互動式流程：錄音 -> Whisper -> 生成 SQL -> 執行 SQL -> 回傳結果
    """
    print("\n=== 語音對話 MySQL 查詢工具 ===")
    print("說 '退出' 或按 Ctrl+C 來退出程序")

    while True:
        try:
            # 計算單次互動的開始時間
            interaction_start = time.time()

            # 開始錄音
            input("按 Enter 開始錄音...")
            print("🎤 開始錄音...")
            record_start = time.time()  # 錄音開始時間
            recorder.start_recording()

            # 停止錄音
            input("按 Enter 停止錄音...")
            print("⏹️ 停止錄音...")
            recorder.stop_recording()
            record_end = time.time()  # 錄音結束時間
            record_duration = record_end - record_start
            print(f"⏱️ 錄音時間：{record_duration:.3f} 秒")

            # 保存錄音
            audio_file = recorder.save_recording("temp_recording.wav")
            if not audio_file:
                print("❌ 未收到音頻")
                continue

            # 語音轉錄
            print("🔍 正在轉錄音頻...")
            transcribe_start = time.time()  # 轉錄開始時間
            text = transcribe_audio(openai_client, audio_file)
            transcribe_end = time.time()  # 轉錄結束時間
            transcribe_duration = transcribe_end - transcribe_start
            print(f"⏱️ 語音轉錄時間：{transcribe_duration:.3f} 秒")

            if text:
                print(f"\n👂 我聽到的是: {text}")

                # 若使用者說「退出」
                if "退出" in text.lower():
                    print("謝謝使用！")
                    break

                # 生成 SQL 語句
                sql_start = time.time()  # SQL 生成開始時間
                sql = process_query(chain, db, text)
                sql_end = time.time()  # SQL 生成結束時間
                sql_duration = sql_end - sql_start
                print(f"⏱️ SQL 生成時間：{sql_duration:.3f} 秒")

                if sql:
                    print("\n🔍 生成的 SQL 查詢語句：")
                    print("=" * 50)
                    print(sql)
                    print("=" * 50)

                    execute = input("\n是否要執行這個查詢？(y/n): ").strip().lower()
                    if execute == "y":
                        # 執行 SQL 查詢
                        execute_start = time.time()  # SQL 執行開始時間
                        try:
                            result = db.run(sql)
                            execute_end = time.time()  # SQL 執行結束時間
                            execute_duration = execute_end - execute_start
                            print(f"⏱️ SQL 執行時間：{execute_duration:.3f} 秒")

                            print("\n📊 查詢結果：")
                            print("-" * 50)
                            print(result)
                            print("-" * 50)
                        except Exception as e:
                            execute_end = time.time()  # SQL 執行結束時間（失敗）
                            execute_duration = execute_end - execute_start
                            print(f"⏱️ SQL 執行時間：{execute_duration:.3f} 秒")
                            print(f"\n❌ 執行查詢時出錯：{str(e)}")

            # 移除臨時音訊檔案（可選）
            # if os.path.exists(audio_file):
            #     os.remove(audio_file)

            # 計算單次互動的總時間
            interaction_end = time.time()
            interaction_duration = interaction_end - interaction_start
            #print(f"\n📈 本次互動總時間：{interaction_duration:.3f} 秒\n")

        except KeyboardInterrupt:
            print("\n謝謝使用！")
            break
        except Exception as e:
            print(f"\n❌ 發生錯誤：{str(e)}")

def main():
    try:
        # 初始化 OpenAI API (Whisper)
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("環境變數 OPENAI_API_KEY 未設置。")
            return
        openai_client = OpenAI(api_key=openai_api_key)

        # 設定資料庫參數
        username = "root"
        password = "root"
        host = "172.17.0.2:3306"
        database = "test"

        # 建立資料庫連線
        db = create_db_connection(username, password, host, database)

        # 建立 LangChain 查詢流程
        chain = setup_langchain(db)

        # 建立 AudioRecorder，指定 device_index = 8 (對應 hw:1,6)
        recorder = AudioRecorder(
            device_index=8,  # 確認裝置後得到的索引
            channels=2,
            rate=48000,
            chunk=512,
            format_type=pyaudio.paInt16,
        )

        # 進入語音互動模式
        voice_interactive_mode(db, chain, openai_client, recorder)

    except Exception as e:
        logger.error(f"執行過程中出錯：{str(e)}")
        raise

if __name__ == "__main__":
    main()


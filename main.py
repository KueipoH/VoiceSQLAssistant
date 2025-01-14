# main.py
import os
import time  # Added import for time module
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
    Interactive Flow: Record -> Whisper -> Generate SQL -> Execute SQL -> Return Results
    """
    print("\n=== Voice-Activated MySQL Query Tool ===")
    print("Say 'exit' or press Ctrl+C to quit the program")

    while True:
        try:
            # Record the start time of the interaction
            interaction_start = time.time()

            # Start recording
            input("Press Enter to start recording...")
            print("🎤 Recording started...")
            record_start = time.time()  # Recording start time
            recorder.start_recording()

            # Stop recording
            input("Press Enter to stop recording...")
            print("⏹️ Recording stopped...")
            recorder.stop_recording()
            record_end = time.time()  # Recording end time
            record_duration = record_end - record_start
            print(f"⏱️ Recording duration: {record_duration:.3f} seconds")

            # Save recording
            audio_file = recorder.save_recording("temp_recording.wav")
            if not audio_file:
                print("❌ No audio received")
                continue

            # Transcribe audio
            print("🔍 Transcribing audio...")
            transcribe_start = time.time()  # Transcription start time
            text = transcribe_audio(openai_client, audio_file)
            transcribe_end = time.time()  # Transcription end time
            transcribe_duration = transcribe_end - transcribe_start
            print(f"⏱️ Transcription duration: {transcribe_duration:.3f} seconds")

            if text:
                print(f"\n👂 I heard: {text}")

                # If user says "exit"
                if "exit" in text.lower():
                    print("Thank you for using the tool!")
                    break

                # Generate SQL statement
                sql_start = time.time()  # SQL generation start time
                sql = process_query(chain, db, text)
                sql_end = time.time()  # SQL generation end time
                sql_duration = sql_end - sql_start
                print(f"⏱️ SQL generation duration: {sql_duration:.3f} seconds")

                if sql:
                    print("\n🔍 Generated SQL Query:")
                    print("=" * 50)
                    print(sql)
                    print("=" * 50)

                    execute = input("\nDo you want to execute this query? (y/n): ").strip().lower()
                    if execute == "y":
                        # Execute SQL query
                        execute_start = time.time()  # SQL execution start time
                        try:
                            result = db.run(sql)
                            execute_end = time.time()  # SQL execution end time
                            execute_duration = execute_end - execute_start
                            print(f"⏱️ SQL execution duration: {execute_duration:.3f} seconds")

                            print("\n📊 Query Results:")
                            print("-" * 50)
                            print(result)
                            print("-" * 50)
                        except Exception as e:
                            execute_end = time.time()  # SQL execution end time (failure)
                            execute_duration = execute_end - execute_start
                            print(f"⏱️ SQL execution duration: {execute_duration:.3f} seconds")
                            print(f"\n❌ Error executing query: {str(e)}")

            # Remove temporary audio file (optional)
            # if os.path.exists(audio_file):
            #     os.remove(audio_file)

            # Calculate total interaction time
            interaction_end = time.time()
            interaction_duration = interaction_end - interaction_start
            #print(f"\n📈 Total interaction time: {interaction_duration:.3f} seconds\n")

        except KeyboardInterrupt:
            print("\nThank you for using the tool!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")

def main():
    try:
        # Initialize OpenAI API (Whisper)
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("Environment variable OPENAI_API_KEY is not set.")
            return
        openai_client = OpenAI(api_key=openai_api_key)

        # Set database parameters
        username = "root"
        password = "root"
        host = "localhost:3306"
        database = "test"

        # Create database connection
        db = create_db_connection(username, password, host, database)

        # Set up LangChain query process
        chain = setup_langchain(db)

        # Create AudioRecorder, specifying device_index = 8 (corresponds to hw:1,6)
        recorder = AudioRecorder(
            device_index=8,  # Index obtained after confirming the device
            channels=2,
            rate=48000,
            chunk=512,
            format_type=pyaudio.paInt16,
        )

        # Enter voice interactive mode
        voice_interactive_mode(db, chain, openai_client, recorder)

    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()


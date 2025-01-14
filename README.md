# WhisperSQL: A Voice-Driven SQL Query Tool

WhisperSQL is an interactive tool that combines OpenAI's Whisper and LangChain technologies to enable voice-driven SQL query generation and execution. This project bridges the gap between natural language and database interaction, making it seamless to interact with your database using just your voice.

---

## ✨ Features

- 🎤 **Voice-Driven Queries**: Use voice commands to query your database effortlessly.
- 🧠 **AI-Powered SQL Generation**: Leverages OpenAI Whisper and LangChain to convert natural language into SQL queries.
- 📊 **Direct Database Interaction**: Automatically execute generated SQL queries and fetch results.
- ⏱️ **Performance Tracking**: Monitors and displays the time taken for each step (recording, transcription, query generation, and execution).

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.10+**: Ensure Python is installed on your system.
2. **MySQL**: A running MySQL instance to connect with.
3. **OpenAI API Key**: Set up an API key for OpenAI's Whisper model.
4. **Dependencies**: Install the required Python libraries.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KueipoH/VoiceSQLAssistant.git
   cd VoiceSQLAssistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set the `OPENAI_API_KEY` environment variable:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

4. Configure your database credentials in `main.py`:
   ```python
   username = "your_username"
   password = "your_password"
   host = "your_host"
   database = "your_database"
   ```

---

## 🛠 Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Follow the interactive prompts:
   - Press Enter to start recording your voice command.
   - Press Enter again to stop recording.
   - Confirm SQL query generation and execution.

3. Example workflow:
   - Say: "Show me the top 10 sales from the orders table and the customer names associated with those sales."
   - WhisperSQL will:
     - Transcribe your command.
     - Generate the SQL query:
       ```sql
       SELECT orders.sales, customers.name 
       FROM orders 
       JOIN customers ON orders.customer_id = customers.id 
       ORDER BY orders.sales DESC 
       LIMIT 10;
       ```
     - Execute the query and display results.


---

## 📂 Project Structure

```plaintext
project-root/
├── db/
│   ├── connection.py       # Database connection utilities
│   ├── langchain_setup.py  # LangChain integration
│   ├── process_query.py    # Query processing
├── audio/
│   ├── recorder.py         # Audio recording functionality
├── transcriber/
│   ├── whisper.py          # Whisper transcription logic
├── utils/
│   ├── logger.py           # Logging setup
├── main.py                 # Main entry point for the application
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── .gitignore              # Git ignored files
```

---

### 🔧 Finding Your `device_index`

To ensure the `AudioRecorder` works correctly with your microphone, you need to identify the `device_index` corresponding to your audio input device. Follow these steps:

1. Open a Python shell and run the following code:
   ```python
   import pyaudio
   
   p = pyaudio.PyAudio()
   for i in range(p.get_device_count()):
       info = p.get_device_info_by_index(i)
       print(f"Index: {i}, Name: {info['name']}")
   p.terminate()
   ```

2. Review the output to find the index number (`Index: X`) of your desired audio input device. Note the name of the device to ensure you select the correct one.

3. Update the `device_index` in your `main.py` file:
   ```python
   recorder = AudioRecorder(
       device_index=X,  # Replace X with the identified index
       channels=2,
       rate=48000,
       chunk=512,
       format_type=pyaudio.paInt16,
   )
   ```
---

## 📊 Performance Insights

WhisperSQL provides detailed timing for each interaction step:
- **Recording Duration**
- **Transcription Time**
- **SQL Generation Time**
- **Query Execution Time**

---

## 🛡 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvement or new features, feel free to fork the repository and create a pull request.

---

## 📞 Support

If you encounter any issues, please open an [issue](https://github.com/KueipoH/VoiceSQLAssistant/issues) on GitHub.

---

## 🌟 Acknowledgments

- OpenAI for the Whisper model.
- LangChain for its powerful language model chaining capabilities.

---

Start querying your database with your voice today! 🎉


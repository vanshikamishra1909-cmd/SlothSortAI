🦥 SlothSort AI



Slow down. Sort smarter. Keep your originals safe.



SlothSort AI is a local-first, AI-powered file organization assistant built to make digital decluttering easier. It combines an open-weight language model with a simple, dark-themed dashboard to help users organize files with less effort.



✨ Features



\- 🧠 Local AI assistance: Uses Qwen 2.5 3B through Ollama to generate file organization advice.

\- 📂 Automatic categorization: Groups files by extension into Documents, Images, Videos, Audio, Spreadsheets, Presentations, Archives, Code, and Other.

\- 📊 Live dashboard: Displays file totals and category statistics.

\- 👀 Preview before action: Review and adjust file categories before copying.

\- 🛡️ Original-file protection: Copies files instead of moving or deleting originals.

\- 🔒 Local-first design: Sends filenames to a local Ollama service rather than a cloud AI API.

\- 🌙 Dark interface: Features a forest-inspired theme and readable dashboard.



🛠️ Tech Stack



\- Python

\- Streamlit

\- Ollama

\- Qwen 2.5 3B

\- Requests



🚀 Getting Started



Prerequisites



Install Python, Ollama, and Git (optional). Ensure your computer has enough resources to run the selected model.



1\. Download the AI model



ollama pull qwen2.5:3b



2\. Clone the repository



git clone https://github.com/YOUR-USERNAME/SlothSortAI.git

cd SlothSortAI



Replace the example repository URL with your actual public repository URL.



3\. Create a virtual environment



python -m venv .venv



Activate it on Windows:



.venv\\Scripts\\activate



4\. Install dependencies



pip install streamlit requests



5\. Run SlothSort AI



Make sure Ollama is running, then execute:



streamlit run app.py



Open the local URL displayed in your terminal, usually "http://localhost:8501".



📖 How It Works



1\. Select a folder on your computer.

2\. Scan its files.

3\. Review the category statistics and organization preview.

4\. Request optional AI-powered organization advice.

5\. Review the proposed categories and select a separate destination folder.

6\. Confirm the operation to create organized copies.



🌱 Why Open Innovation?



SlothSort AI uses an open-weight model through Ollama, allowing AI inference to run locally rather than relying on a paid cloud AI API. This gives users greater control over their data, makes experimentation with different models possible, and can reduce recurring inference costs.



Once the model and dependencies are installed, core AI inference can work without an internet connection, provided the local services are available.



⚠️ Current Limitations



\- Categorization is based primarily on file extensions, not an analysis of file contents.

\- AI advice is generated from filenames and may not always be accurate.

\- The app currently copies files; it does not move or delete originals.

\- The app should be tested with sample files before use on important folders.

\- Resource requirements depend on the model and the computer.



🔮 Future Improvements



\- Drag-and-drop folder selection

\- More advanced duplicate detection

\- Custom categories and rules

\- Undo and copy-history support

\- Improved accessibility and interface customization

\- Support for additional local AI models



💚 Our Mission



Make everyday digital organization easier, safer, and more accessible through open-source AI.



SlothSort AI — Let the sloth handle the clutter. 🦥


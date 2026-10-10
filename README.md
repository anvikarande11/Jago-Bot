Jago Bot | MoTA AI Assistant 
Jago Bot is an intelligent, privacy-focused Retrieval-Augmented Generation (RAG) chatbot designed to assist Scheduled Tribe (ST) students, citizens, and stakeholders with queries related to Ministry of Tribal Affairs (MoTA) scholarship schemes, Eklavya Model Residential Schools (EMRS), and welfare initiatives.

Built with a hybrid architecture, it processes queries locally using open-source models via Ollama to ensure complete data privacy, while maintaining persistent chat logging and session management in cloud-based MongoDB Atlas.

🌟 Key Features
Privacy-First Local AI: Powered locally by Ollama (llama3 & nomic-embed-text), ensuring no sensitive user data leaves your machine or relies on third-party commercial LLM API keys.

Smart RAG Pipeline: Combines local vector search via ChromaDB with official MoTA scheme guidelines to ground responses in accurate, verified documents.

Hybrid Data Persistence: Asynchronously logs conversation histories, session metadata, and audit trails to MongoDB Atlas.

Multilingual & General Intent Routing: Dynamically detects general queries and supports flexible language instruction directives.

Voice Search Integration: Built-in browser Web Speech API support for speech-to-text voice queries.

Modern API Backend: Built with high-performance FastAPI, featuring automatic Swagger UI documentation.

🏗️ Tech Stack
Backend: FastAPI, Python, Pydantic, Motor (Async MongoDB Driver)

AI / Orchestration: LangChain, Ollama (llama3, nomic-embed-text)

Vector Store: ChromaDB (Local persistent storage)

Database: MongoDB Atlas (Cloud storage for chat logs)

Frontend: Tailwind CSS, Vanilla JavaScript, FontAwesome

Getting Started Locally
Prerequisites
Make sure you have the following installed on your system:

Python 3.10+

Ollama running locally with required models pulled:

Bash
ollama pull llama3
ollama pull nomic-embed-text
Installation & Setup
Clone the repository:

Bash
git clone https://github.com/your-username/JagoChatBot.git
cd JagoChatBot/backend
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file inside the backend/ directory and add your MongoDB connection URI:

Code snippet
MONGO_URI=your_mongodb_atlas_connection_string_here
Run the FastAPI Server:

Bash
uvicorn app.main:app --reload
Access the Application:
Open your browser and navigate to:

Frontend Chat UI: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Interactive API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

🌐 Public Tunneling Demo (Ngrok)
To expose your local server for live demonstrations or testing on mobile devices without paid cloud hosting:

Bash
ngrok http 8000
Copy the generated https:// tunnel URL and open it on any device. (Note: Ensure your local machine and Ollama server remain active).

📜 License
This project is open-source and available under the MIT License.

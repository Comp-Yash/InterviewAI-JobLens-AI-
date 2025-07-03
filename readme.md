# 🎯 AI Interview Assistant

An intelligent Streamlit web application that simulates a real-time voice-based interview experience using **Gemini AI**, **speech recognition**, and **resume analysis**.

## ✅ App Link : 

## 🚧 Current Status: Phase 1 Demo Prototype 

This is the **initial working prototype** of the AI Interview Assistant, featuring core functionality for automated interview simulation.

### 🔜 Upcoming Features (Phase 2)
- 👩‍💼 Realistic **HR video avatar** synced with AI-generated audio
- 🤖 **More humanized and role-specific questions**
- 🗣️ **Emotionally adaptive & natural-sounding voice responses**
- ✅ **Expected Answer Suggestions** after each question
- 🔄 **Follow-up Questions** based on candidate responses
- 🌍 **Multilingual & regional language voice support**
- 📊 **Performance analytics and scoring**

---

## 🚀 Current Features

### ✨ Core Functionality
- 📄 **Resume Analysis**: Upload and auto-parse PDF resumes
- 🧠 **AI-Generated Questions**: Personalized interview questions using Gemini AI
- 🎤 **Voice Recording**: Record spoken answers via microphone
- 🔊 **Text-to-Speech**: Automatic question delivery with voice synthesis
- 📋 **Interview Summary**: Downloadable Q&A transcript
- 🎯 **Role-Specific**: Tailored questions based on job description and experience level

### 🎯 Interview Process
1. **Setup Phase**: Enter candidate details, upload resume, specify job requirements
2. **Interview Phase**: 10 AI-generated questions with voice interaction
3. **Summary Phase**: Complete transcript download and session review

---

## 📸 Screenshots

### Main Interface
![AI Interview Assistant Main](https://via.placeholder.com/800x400?text=AI+Interview+Assistant+Main+Interface)

### Interview in Progress
![Interview Session](https://via.placeholder.com/800x400?text=Interview+Session+in+Progress)

### Interview Summary
![Interview Summary](https://via.placeholder.com/800x400?text=Interview+Summary)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend/UI** | Streamlit |
| **AI Model** | Google Gemini 2.0 Flash |
| **Speech Recognition** | SpeechRecognition + PyAudio |
| **Text-to-Speech** | gTTS (Google Text-to-Speech) |
| **Audio Processing** | Pygame |
| **Resume Parsing** | PyMuPDF (fitz) |
| **Backend** | Python 3.8+ |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Microphone access for voice recording
- Internet connection for AI services

### 1. Clone the Repository
```bash
git clone https://github.com/Comp-Yash/InterviewAI-JobLens-AI-.git
cd ai-interview-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important**: Replace `your_gemini_api_key_here` with your actual Gemini API key from Google AI Studio.

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

---

## 📁 Project Structure

```
ai-interview-assistant/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── assets/                # Static assets
│   ├── images/            # Screenshots and UI images
│   └── samples/           # Sample resumes and job descriptions



```

---

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `AUDIO_TIMEOUT` | Audio recording timeout (seconds) | No (default: 120) |
| `SILENCE_THRESHOLD` | Silence detection threshold | No (default: 8.0) |

### Audio Settings
- **Recording timeout**: 120 seconds maximum
- **Silence threshold**: 8 seconds of silence to stop recording
- **Supported formats**: WAV, MP3 for TTS output
- **Language**: English (US) for speech recognition

---

## 🎯 Usage Guide

### Step 1: Setup Interview
1. Enter candidate name and job title
2. Select experience level (Entry/Mid/Senior/Lead)
3. Upload resume in PDF format
4. Provide job description and requirements
5. Click "Start Interview"

### Step 2: Interview Process
1. Listen to each AI-generated question
2. Click "Record Answer" to respond
3. Speak clearly into your microphone
4. Stop speaking for 8 seconds to auto-submit
5. Use "Repeat Question" if needed
6. Complete all 10 questions

### Step 3: Review Results
1. Review complete Q&A transcript
2. Download interview summary
3. Start new interview if needed

---

## 🔧 Troubleshooting

### Common Issues

#### Microphone Not Working
- Ensure microphone permissions are granted
- Check if microphone is being used by other applications
- Try refreshing the browser page

#### Audio Playback Issues
- Verify system audio settings
- Check if pygame is properly installed
- Ensure sufficient disk space for temporary files

#### API Errors
- Verify Gemini API key is correctly set
- Check internet connectivity
- Ensure API quotas are not exceeded

#### Resume Upload Failed
- Ensure PDF is not password protected
- Check file size (recommended < 10MB)
- Verify PDF is not corrupted

---

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific tests:
```bash
python -m pytest tests/test_basic.py -v
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Google Gemini AI for intelligent question generation
- Streamlit team for the excellent web framework
- Speech recognition and TTS libraries contributors
- Open source community for various Python packages

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Comp-Yash/InterviewAI-JobLens-AI-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Comp-Yash/InterviewAI-JobLens-AI-/discussions)
- **Email**: yashpasalkar532@gmail.com

---

## 🗺️ Roadmap

### Phase 1: Demo Prototype ✅
- Basic voice-based interview simulation
- Resume parsing and AI question generation
- Simple Q&A transcript generation

### Phase 2: Enhanced Experience 🔄
- HR video avatar integration
- Advanced voice synthesis
- Performance analytics
- Multi-language support

### Phase 3: Enterprise Features 🔮
- Integration with HR systems
- Advanced reporting and analytics
- Custom interview templates
- Team collaboration features

---

**Made with ❤️ by [Yash Pasalkar]**
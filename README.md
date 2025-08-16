# Digital Twin AI System 🤖

A comprehensive **Digital Twin AI platform** that creates intelligent synthetic representations of individuals using advanced AI models, synthetic data generation, and real-time behavioral simulation.

![Digital Twin AI](https://img.shields.io/badge/AI-Digital%20Twin-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## 🌟 Features

### Core AI Components
- **🧠 AI-Powered Personality Modeling** - Dynamic personality simulation using synthetic data
- **💬 Advanced Conversation Engine** - Natural language processing with sentiment analysis
- **🎯 Behavioral Simulation** - Real-time behavior pattern generation and evolution
- **🏥 Health Monitoring** - Synthetic health data tracking and anomaly detection
- **📊 Interactive Visualizations** - Cross-platform 3D visualizations using Plotly

### Technical Capabilities
- **🔄 Real-time Data Processing** - Live synthetic data generation and updates
- **🌐 RESTful API** - Comprehensive REST API with OpenAPI documentation
- **💾 Persistent Storage** - SQLite database with SQLAlchemy ORM
- **🔐 Authentication & Security** - JWT-based authentication system
- **📱 Responsive Web UI** - Modern, interactive dashboard
- **🚀 Background Task Processing** - Asynchronous task handling

## 🏗️ System Architecture

```mermaid
graph TB
    UI[Web Dashboard] --> API[FastAPI Backend]
    API --> Engine[Digital Twin Engine]
    Engine --> AI[AI Models]
    Engine --> Data[Synthetic Data Manager]
    Engine --> Health[Health Monitor]
    Engine --> Behavior[Behavior Simulator]
    Engine --> Viz[Visualization Engine]
    AI --> Conv[Conversation Engine]
    AI --> Pers[Personality Model]
    Data --> DB[(SQLite Database)]
    Viz --> Plotly[Plotly Charts]
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- 4GB+ RAM recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jagrut70/digital-twin-ai.git
   cd digital-twin-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the dashboard**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📖 How It Works

### 1. Digital Twin Creation
The system automatically creates a **Demo Digital Twin** on startup with:
- **Synthetic personality traits** (Big Five model)
- **Health baseline data** (vitals, metrics, trends)
- **Behavioral patterns** (activities, preferences, responses)

### 2. AI-Powered Interactions
- **Natural Language Processing**: Advanced conversation engine with sentiment analysis
- **Intent Recognition**: Understands user queries and responds contextually
- **Personality-Driven Responses**: Answers reflect the twin's synthetic personality
- **Learning & Adaptation**: Continuously evolves based on interactions

### 3. Real-Time Monitoring
- **Health Simulation**: Generates realistic health data updates every 60 seconds
- **Behavior Evolution**: Simulates behavioral patterns every 30 seconds
- **Personality Changes**: Tracks personality evolution over time
- **Data Persistence**: All changes automatically saved to database

### 4. Visualization & Analytics
- **3D Avatar Visualization**: Interactive 3D representations using Plotly
- **Health Dashboards**: Real-time health metrics and trends
- **Behavior Analysis**: Pattern recognition and behavioral insights
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎮 Using the Dashboard

### Main Interface Components

#### 1. **Twin Overview Section**
- **Avatar Status**: Shows if your digital twin is active
- **Basic Info**: Name, description, and metadata
- **Connection Status**: Data sources and sync information
- **Edit Controls**: Modify twin properties and settings

#### 2. **Key Metrics Dashboard**
- **Simulation Accuracy**: How well the AI mimics real behavior
- **Data Sources**: Number of connected synthetic data streams
- **Last Sync**: When data was last updated
- **Learning Progress**: AI model improvement over time

#### 3. **Interactive Chat Interface**
- **Real-time Conversations**: Chat directly with your digital twin
- **Contextual Responses**: AI responds based on synthetic personality
- **Message History**: Persistent conversation logs
- **Sentiment Analysis**: Emotional tone detection

### What to Check on the UI

1. **System Status**
   - Green "Active" indicator means your twin is running
   - Check that all 4 data sources are "connected"
   - Verify "Last Sync" shows recent timestamps

2. **Live Metrics**
   - Watch **Simulation Accuracy** (should be 90%+)
   - Monitor **Learning Progress** increasing over time
   - Observe **Data Sources** staying connected

3. **Real-Time Updates**
   - Metrics refresh every 30 seconds
   - Chat messages appear instantly
   - Status indicators update automatically

4. **Interactive Features**
   - Type messages to chat with your digital twin
   - Click "Edit Twin" to modify personality traits
   - Toggle light/dark theme in top navigation

## 🔧 API Usage

### Key Endpoints

#### Digital Twin Management
```bash
# List all digital twins
curl http://localhost:8000/api/v1/twins

# Get twin details
curl http://localhost:8000/api/v1/twins/{twin_id}

# Create new twin
curl -X POST http://localhost:8000/api/v1/twins \
  -H "Content-Type: application/json" \
  -d '{"name": "My Twin", "personality": {...}}'
```

#### Health Monitoring
```bash
# Get health data
curl http://localhost:8000/api/v1/twins/{twin_id}/health

# Get health trends
curl http://localhost:8000/api/v1/twins/{twin_id}/health/trends
```

#### Conversations
```bash
# Send message to twin
curl -X POST http://localhost:8000/api/v1/twins/{twin_id}/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How are you feeling today?"}'
```

#### System Status
```bash
# Health check
curl http://localhost:8000/health

# System information
curl http://localhost:8000/system/info
```

## 🧪 Testing

### Automated Testing
```bash
# Run comprehensive test suite
python comprehensive_test.py

# Test visualization engine specifically
python test_visualization.py
```

### Manual Testing Checklist

1. **Startup Verification**
   - [ ] Server starts without errors
   - [ ] Database initializes successfully
   - [ ] Demo twin creates automatically
   - [ ] All AI models load properly

2. **Dashboard Functionality**
   - [ ] Web interface loads at http://localhost:8000
   - [ ] Metrics display current values
   - [ ] Chat interface accepts messages
   - [ ] Theme toggle works

3. **API Endpoints**
   - [ ] `/health` returns system status
   - [ ] `/api/v1/twins` lists available twins
   - [ ] `/docs` shows API documentation
   - [ ] Chat endpoints respond correctly

4. **Background Processing**
   - [ ] Health updates every minute
   - [ ] Behavior patterns evolve every 30s
   - [ ] Synthetic data generates continuously
   - [ ] Database saves changes automatically

## 🏭 Production Deployment

### Environment Variables
Create a `.env` file:
```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
WORKERS=4

# Database
DATABASE_URL=sqlite:///./digital_twin.db
# For production: DATABASE_URL=postgresql://user:pass@host:port/db

# Security
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI Models
USE_GPU=false
MODEL_DEVICE=cpu
MODEL_CACHE_DIR=./models

# Optional API Keys
OPENAI_API_KEY=your-openai-key
HUGGINGFACE_API_KEY=your-huggingface-key
```

### Docker Deployment
```bash
# Build image
docker build -t digital-twin-ai .

# Run container
docker run -p 8000:8000 -v $(pwd)/data:/app/data digital-twin-ai
```

### Production Checklist
- [ ] Set secure `SECRET_KEY`
- [ ] Use production database (PostgreSQL)
- [ ] Configure CORS origins
- [ ] Set up SSL/HTTPS
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Configure backups

## 🛠️ Development

### Project Structure
```
digital-twin-ai/
├── main.py                 # FastAPI application entry point
├── core/                   # Core system components
│   ├── digital_twin_engine.py  # Main engine orchestrator
│   ├── config.py              # Configuration management
│   ├── database.py            # Database layer
│   ├── models/                # AI and data models
│   └── data/                  # Synthetic data management
├── api/                    # REST API endpoints
├── ui/                     # UI routes and templates
├── js/                     # Frontend JavaScript
├── styles/                 # CSS stylesheets
├── tests/                  # Test suites
└── data/                   # Generated data storage
```

### Key Components

#### 1. **Digital Twin Engine** (`core/digital_twin_engine.py`)
- Central orchestrator managing all subsystems
- Handles twin lifecycle (create, update, delete)
- Coordinates background tasks and data flow

#### 2. **AI Models** (`core/models/`)
- **Personality Model**: Big Five trait simulation
- **Health Monitor**: Vital sign generation and monitoring
- **Behavior Simulator**: Activity pattern modeling
- **Conversation Engine**: NLP and chat capabilities
- **Visualization Engine**: 3D plotting and charts

#### 3. **Synthetic Data Manager** (`core/data/`)
- Generates realistic personality profiles
- Creates health baselines and trends
- Produces behavioral patterns
- Manages data persistence and updates

#### 4. **API Layer** (`api/`)
- RESTful endpoints for all operations
- Authentication and authorization
- Request validation and response formatting
- WebSocket support for real-time updates

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port
   PORT=8080 python main.py
   ```

2. **Dependencies Missing**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

3. **Database Errors**
   ```bash
   # Reset database
   rm digital_twin.db
   python main.py  # Will recreate automatically
   ```

4. **AI Model Loading Issues**
   ```bash
   # Clear model cache
   rm -rf ./models/
   python main.py  # Will download models again
   ```

5. **Visualization Not Working**
   - Check browser console for JavaScript errors
   - Ensure Plotly CDN is accessible
   - Verify visualizations directory exists

### Log Files
- Application logs: `./logs/digital_twin.log`
- Error details in console output
- Enable DEBUG mode for verbose logging

## 📊 Performance

### System Requirements
- **Minimum**: 2GB RAM, 1 CPU core, 1GB storage
- **Recommended**: 4GB+ RAM, 2+ CPU cores, 5GB storage
- **Production**: 8GB+ RAM, 4+ CPU cores, 20GB storage

### Performance Metrics
- **Startup Time**: ~10-15 seconds with model loading
- **API Response**: <100ms for most endpoints
- **Chat Response**: ~1-2 seconds with AI processing
- **Background Tasks**: Update every 30-60 seconds
- **Memory Usage**: ~500MB-1GB typical

### Scaling Options
- **Horizontal**: Multiple instances behind load balancer
- **Database**: PostgreSQL for production workloads
- **Caching**: Redis for session and data caching
- **GPU**: Enable GPU acceleration for AI models

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Documentation**: Check the `/docs` endpoint when running
- **Issues**: Open GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact through GitHub profile

## 🎯 Roadmap

### Version 2.0
- [ ] Multi-user support with user accounts
- [ ] Advanced visualization with 3D avatars
- [ ] Mobile app integration
- [ ] Cloud deployment templates
- [ ] Enhanced AI model training

### Future Features
- [ ] Voice interaction capabilities
- [ ] Wearable device integration
- [ ] Social twin interactions
- [ ] Predictive health analytics
- [ ] AR/VR visualization support

---

**Built with ❤️ using FastAPI, Python, and cutting-edge AI technologies.**

⭐ **Star this repository if you find it useful!**

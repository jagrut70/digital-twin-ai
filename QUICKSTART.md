# 🚀 Digital Twin System - Quick Start Guide

Get your Digital Twin system up and running in minutes!

## ⚡ Quick Setup (5 minutes)

### 1. **Prerequisites**
- Python 3.8 or higher
- Git
- Internet connection

### 2. **Clone and Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd Digi-twin

# Run the automated setup
python setup.py
```

### 3. **Configure Environment**
```bash
# Copy the configuration template
cp config.template.env .env

# Edit .env with your settings
nano .env  # or use your favorite editor
```

**Required Configuration:**
- Add your OpenAI API key for AI features
- Add your HuggingFace API key for ML models
- Customize other settings as needed

### 4. **Start the System**
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the Digital Twin system
python main.py
```

### 5. **Access the System**
- **Web Interface**: http://localhost:8000/ui/
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 What You Get

✅ **Fully Functional Digital Twin System**
- Core engine with personality, health, and behavior simulation
- Web-based dashboard with real-time monitoring
- REST API and WebSocket support
- Synthetic data generation and management

✅ **Modern Web Interface**
- Responsive dashboard with charts and metrics
- Real-time updates via WebSocket
- Beautiful UI with Bootstrap and Chart.js

✅ **AI/ML Capabilities**
- Personality modeling and evolution
- Health monitoring and prediction
- Behavior simulation and analysis
- Conversational AI integration

## 🔧 Customization Options

### **Create Your First Digital Twin**
1. Go to http://localhost:8000/ui/
2. Click "Create Your First Twin"
3. Configure personality, health, and visual profiles
4. Watch your twin evolve in real-time!

### **Add Synthetic Data Sources**
- **SynBody/SynPlay**: 3D human models and poses
- **Aria Dataset**: Sensor and interaction data
- **SIPHER**: Socio-demographic modeling
- **Custom**: Your own synthetic data generators

### **Extend AI Models**
- Train custom personality models
- Add new health monitoring algorithms
- Implement specialized behavior patterns
- Integrate with external AI services

## 🚨 Troubleshooting

### **Common Issues**

**Port Already in Use**
```bash
# Change port in .env file
PORT=8001
```

**Database Connection Error**
```bash
# Check if SQLite file exists
ls -la digital_twin.db

# Reinitialize database
python setup.py
```

**Missing Dependencies**
```bash
# Reinstall requirements
pip install -r requirements.txt
```

**API Key Errors**
- Ensure your API keys are correctly set in `.env`
- Check API key permissions and quotas
- Verify internet connectivity

### **Getting Help**
- Check the logs in `./logs/digital_twin.log`
- Review API documentation at `/docs`
- Check system status at `/health`

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   REST API      │    │  WebSocket      │
│   (Dashboard)   │◄──►│   (FastAPI)     │◄──►│  (Real-time)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Digital Twin Engine                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Personality │ │   Health    │ │  Behavior   │              │
│  │   Model     │ │  Monitor    │ │ Simulator   │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │Conversation │ │Visualization│ │Synthetic    │              │
│  │  Engine     │ │   Engine    │ │Data Manager │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │  Database   │ │   Redis     │ │   File      │              │
│  │  (SQLite)   │ │   Cache     │ │   Storage   │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Next Steps

1. **Explore the Dashboard**: Familiarize yourself with the interface
2. **Create Digital Twins**: Build your first digital twin
3. **Monitor Metrics**: Watch real-time health and personality data
4. **Customize Models**: Adapt AI models to your use case
5. **Scale Up**: Deploy to cloud infrastructure
6. **Integrate**: Connect with external systems and data sources

## 📚 Additional Resources

- **Full Documentation**: See `README.md`
- **API Reference**: http://localhost:8000/docs
- **Code Examples**: Check the `examples/` directory
- **Community**: Join our discussion forums

---

**🎉 Congratulations!** You now have a fully functional Digital Twin system running on your machine.

**Need help?** Check the logs, API docs, or reach out to our community!

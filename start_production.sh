#!/bin/bash

# Digital Twin System - Production Startup Script
# This script starts the application in production mode

set -e

echo "🚀 Starting Digital Twin System in Production Mode..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/update production dependencies
echo "📥 Installing production dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p models
mkdir -p data/synthetic
mkdir -p data/synbody
mkdir -p data/aria
mkdir -p data/sipher

# Set production environment variables
export ENVIRONMENT=production
export LOG_LEVEL=INFO
export RELOAD=false

# Check if .env file exists, if not copy from template
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from production template..."
    cp config.production.env .env
    echo "⚠️  Please edit .env file with your production settings before continuing."
    echo "⚠️  Press Enter when ready to continue..."
    read
fi

# Run database migrations (if using Alembic)
if command -v alembic &> /dev/null; then
    echo "🗄️  Running database migrations..."
    alembic upgrade head
fi

# Start the application
echo "🌟 Starting Digital Twin System..."
echo "📍 Server will be available at: http://0.0.0.0:8000"
echo "📍 Health check: http://0.0.0.0:8000/health"
echo "📍 Dashboard: http://0.0.0.0:8000/ui/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start with production settings
python main.py

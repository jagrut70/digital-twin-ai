#!/bin/bash

echo "🚀 Digital Twin Application - Start and Test Script"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo "📥 Installing aiohttp..."
    pip3 install aiohttp
fi

echo ""
echo "🎯 Choose an option:"
echo "1. Start the application server only"
echo "2. Run full application tests only"
echo "3. Start server and run tests (recommended)"
echo "4. Quick health check"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🚀 Starting Digital Twin application server..."
        echo "📱 Server will be available at: http://localhost:8000"
        echo "📚 API docs at: http://localhost:8000/docs"
        echo "🛑 Press Ctrl+C to stop the server"
        echo ""
        python3 main.py
        ;;
    2)
        echo "🧪 Running full application tests..."
        echo "⚠️  Make sure the server is running in another terminal first!"
        echo ""
        python3 test_full_app.py
        ;;
    3)
        echo "🚀 Starting server and running tests..."
        echo ""
        
        # Start server in background
        echo "Starting server in background..."
        python3 main.py &
        SERVER_PID=$!
        
        # Wait for server to start
        echo "Waiting for server to start..."
        sleep 5
        
        # Check if server is running
        if curl -s çhttp://localhost:8000/health > /dev/null; then
            echo "✅ Server is running!"
            echo ""
            
            # Run tests
            echo "🧪 Running full application tests..."
            python3 test_full_app.py
            
            # Stop server
            echo ""
            echo "🛑 Stopping server..."
            kill $SERVER_PID
            echo "✅ Server stopped"
        else
            echo "❌ Server failed to start"
            kill $SERVER_PID 2>/dev/null
            exit 1
        fi
        ;;
    4)
        echo "🔍 Quick health check..."
        echo ""
        
        # Start server in background
        python3 main.py > /dev/null 2>&1 &
        SERVER_PID=$!
        
        # Wait for server
        sleep 3
        
        # Quick health check
        if curl -s http://localhost:8000/health > /dev/null; then
            echo "✅ Server is healthy!"
            echo "🌐 Available at: http://localhost:8000"
            echo "📚 API docs: http://localhost:8000/docs"
        else
            echo "❌ Server health check failed"
        fi
        
        # Stop server
        kill $SERVER_PID 2>/dev/null
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

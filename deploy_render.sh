#!/bin/bash

# Digital Twin System - Render Deployment Script
# This script helps you deploy to Render for free

set -e

echo "🌊 Deploying Digital Twin System to Render..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from production template..."
    cp config.production.env .env
    
    echo "⚠️  Please edit .env file with your production settings:"
    echo "   - Change SECRET_KEY to a random string"
    echo "   - Set HOST=0.0.0.0"
    echo "   - Set PORT=\$PORT (Render will set this)"
    echo ""
    echo "Press Enter when ready to continue..."
    read
fi

echo ""
echo "🎯 Manual Deployment Steps for Render:"
echo ""
echo "1. 🌐 Go to https://render.com and sign up/login"
echo ""
echo "2. 📝 Create a new Web Service:"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Connect your GitHub repository"
echo "   - Select the Digi-twin repository"
echo ""
echo "3. ⚙️  Configure the service:"
echo "   - Name: digital-twin-system"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python main.py"
echo "   - Plan: Free"
echo ""
echo "4. 🔧 Set Environment Variables:"
echo "   - HOST=0.0.0.0"
echo "   - PORT=\$PORT"
echo "   - ENVIRONMENT=production"
echo "   - SECRET_KEY=your-random-secret-key"
echo ""
echo "5. 🚀 Deploy:"
echo "   - Click 'Create Web Service'"
echo "   - Wait for build to complete"
echo ""
echo "6. 🌍 Your app will be available at:"
echo "   https://your-app-name.onrender.com"
echo ""
echo "📊 Monitor your app in the Render dashboard"
echo "🔄 Automatic deployments on every git push"
echo ""
echo "💡 Pro Tips:"
echo "   - Free tier sleeps after 15 minutes of inactivity"
echo "   - First request after sleep takes ~30 seconds"
echo "   - Perfect for development and testing"
echo "   - Upgrade to paid plan for always-on service"

#!/usr/bin/env python3
"""
Digital Twin System Setup Script
Helps users set up the environment and dependencies
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        if result.stdout.strip():
            print(f"  📝 Output: {result.stdout.strip()}")
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.TimeoutExpired:
        print(f"❌ {description} timed out after 5 minutes")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if e.stdout.strip():
            print(f"  📝 Output: {e.stdout.strip()}")
        if e.stderr.strip():
            print(f"  ❌ Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ {description} failed with unexpected error: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/synthetic",
        "data/synbody", 
        "data/aria",
        "data/sipher",
        "visualization/unity_builds",
        "logs",
        "ui/static",
        "ui/templates"
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created: {directory}")

def setup_environment():
    """Set up the Python environment"""
    print("🐍 Setting up Python environment...")
    
    # Check if virtual environment exists
    if not Path("venv").exists():
        print("  Creating virtual environment...")
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            print("  ❌ Failed to create virtual environment")
            print("  Make sure python3 and venv module are available")
            return False
    else:
        print("  Virtual environment already exists")
    
    # Determine pip and python commands based on platform
    if sys.platform == "win32":
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Check if pip is available
    if not Path(pip_cmd.replace("\\", "/")).exists():
        print(f"  ❌ Pip not found at {pip_cmd}")
        print("  Virtual environment may be corrupted. Try deleting 'venv' folder and running setup again.")
        return False
    
    # Upgrade pip
    print("  Upgrading pip...")
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        print("  ⚠️  Pip upgrade failed, continuing with existing version...")
    
    # Install minimal requirements first
    print("  Installing minimal dependencies...")
    if not run_command(f"{pip_cmd} install -r requirements-minimal.txt", "Installing minimal dependencies"):
        print("  ⚠️  Minimal dependencies installation failed, trying full requirements...")
        if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing full dependencies"):
            print("  ❌ All dependency installation attempts failed")
            print("  Check your internet connection and requirements files")
            return False
    
    print("  ✅ Dependencies installed successfully")
    return True

def setup_database():
    """Initialize the database"""
    print("🗄️ Setting up database...")
    
    try:
        # Import database manager
        from core.database import db_manager
        
        # Run database initialization in a new event loop
        import asyncio
        
        # Create new event loop for this thread
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def init_db():
                await db_manager.initialize()
                print("  ✅ Database initialized successfully")
            
            loop.run_until_complete(init_db())
            loop.close()
            return True
            
        except RuntimeError:
            # If we're already in an event loop, use it
            async def init_db():
                await db_manager.initialize()
                print("  ✅ Database initialized successfully")
            
            asyncio.run(init_db())
            return True
        
    except ImportError as e:
        print(f"  ❌ Could not import database module: {e}")
        print("  Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"  ❌ Database setup failed: {e}")
        print(f"  Error details: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_data():
    """Create sample synthetic data"""
    print("📊 Creating sample data...")
    
    try:
        # Ensure the synthetic data directory exists
        synthetic_dir = Path("data/synthetic")
        synthetic_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a sample synthetic data file
        sample_data_path = synthetic_dir / "sample_data.json"
        
        # Check if file already exists
        if sample_data_path.exists():
            print("  ℹ️  Sample data already exists, skipping creation")
            return True
        
        sample_data = {
            "description": "Sample synthetic data for testing",
            "created_at": "2024-01-01T00:00:00Z",
            "data_type": "health_metrics",
            "sample_values": {
                "heart_rate": [65, 72, 68, 75, 70],
                "blood_pressure": [120, 118, 122, 119, 121],
                "temperature": [98.6, 98.4, 98.7, 98.5, 98.6]
            }
        }
        
        import json
        with open(sample_data_path, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print("  ✅ Sample data created successfully")
        return True
        
    except PermissionError:
        print("  ❌ Permission denied when creating sample data")
        print("  Check if you have write permissions to the data directory")
        return False
    except Exception as e:
        print(f"  ❌ Sample data creation failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        return False

def check_requirements():
    """Check if required files exist"""
    print("🔍 Checking requirements...")
    
    required_files = [
        "requirements-minimal.txt",
        "requirements.txt",
        "config.template.env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"  ❌ Missing required files: {', '.join(missing_files)}")
        print("  Make sure you're running setup from the project root directory")
        return False
    
    print("  ✅ All required files found")
    return True

def test_setup():
    """Test the setup by running basic checks"""
    print("🧪 Testing setup...")
    
    try:
        # Test database connection
        from core.database import db_manager
        import asyncio
        
        async def test_db():
            try:
                await db_manager.health_check()
                print("  ✅ Database connection test passed")
                return True
            except Exception as e:
                print(f"  ❌ Database connection test failed: {e}")
                return False
        
        # Run test in event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(test_db())
            loop.close()
        except RuntimeError:
            result = asyncio.run(test_db())
        
        if not result:
            return False
        
        # Test if main application can be imported
        try:
            import main
            print("  ✅ Main application import test passed")
        except Exception as e:
            print(f"  ❌ Main application import test failed: {e}")
            return False
        
        print("  ✅ All tests passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Setup test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Digital Twin System Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        sys.exit(1)
    
    # Create sample data
    create_sample_data()
    
    # Test the setup
    if not test_setup():
        print("❌ Setup test failed")
        print("The setup completed but some tests failed. Check the logs above.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy config.template.env to .env and configure your settings")
    print("2. Add your API keys to the .env file")
    print("3. Run: python main.py")
    print("4. Open http://localhost:8000 in your browser")
    print("\n📚 For more information, see README.md")
    print("\n💡 To test the setup again, run: python setup.py --test")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digital Twin System Setup")
    parser.add_argument("--test", action="store_true", help="Run only the setup tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running setup tests only...")
        if test_setup():
            print("✅ All tests passed!")
            sys.exit(0)
        else:
            print("❌ Some tests failed!")
            sys.exit(1)
    else:
        main()

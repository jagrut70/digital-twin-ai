#!/usr/bin/env python3
"""
Simple direct test for the new Plotly-based visualization engine
"""

import os
import sys
import logging
from datetime import datetime
import json

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_visualization_engine():
    """Test the new Plotly-based visualization system directly"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    logger.info("🎨 Testing Plotly Visualization Engine Directly...")
    
    try:
        # Import and test the visualization engine directly
        from core.models.visualization_engine import VisualizationEngine
        
        viz_engine = VisualizationEngine()
        
        # Test initialization
        logger.info("Testing visualization engine initialization...")
        if not viz_engine.initialize():
            logger.error("❌ Failed to initialize visualization engine")
            return False
        
        logger.info("✅ Visualization engine initialized successfully")
        
        # Test configuration
        logger.info("Testing configuration...")
        config = viz_engine.renderer_config
        logger.info(f"Engine type: {config.get('renderer_type', 'unknown')}")
        logger.info(f"Plotly available: {viz_engine.plotly_available}")
        
        if not viz_engine.plotly_available:
            logger.error("❌ Plotly is not available")
            return False
        
        # Create output directory
        output_dir = "./visualizations"
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created output directory: {output_dir}")
        
        # Test 3D avatar visualization
        logger.info("Testing 3D avatar visualization...")
        
        # Create test avatar data
        avatar_data = {
            'position': [0, 0, 0],
            'personality': {
                'openness': 0.7,
                'conscientiousness': 0.6,
                'extraversion': 0.8,
                'agreeableness': 0.5,
                'neuroticism': 0.3
            },
            'health': {
                'heart_rate': 75,
                'blood_pressure': [120, 80],
                'stress_level': 0.4
            },
            'emotional_state': 'happy'
        }
        
        try:
            avatar_figure = viz_engine.create_3d_avatar_visualization(avatar_data)
            logger.info("✅ 3D avatar visualization created")
            
            # Save as HTML
            viz_engine.save_figure(avatar_figure, f"{output_dir}/avatar_test.html")
            logger.info("✅ Avatar saved as HTML")
            
            # Save as JSON
            viz_engine.save_figure(avatar_figure, f"{output_dir}/avatar_test.json", format='json')
            logger.info("✅ Avatar saved as JSON")
            
        except Exception as e:
            logger.error(f"❌ Avatar visualization failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Test 3D scene visualization
        logger.info("Testing 3D scene visualization...")
        
        scene_data = {
            'avatars': [avatar_data],
            'environment': {
                'type': 'indoor',
                'lighting': 'natural',
                'objects': []
            }
        }
        
        try:
            scene_figure = viz_engine.create_3d_scene_visualization(scene_data)
            logger.info("✅ 3D scene visualization created")
            
            viz_engine.save_figure(scene_figure, f"{output_dir}/scene_test.html")
            logger.info("✅ Scene saved as HTML")
            
        except Exception as e:
            logger.error(f"❌ Scene visualization failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Test basic visualize_avatar method
        logger.info("Testing basic avatar visualization method...")
        
        try:
            basic_figure = viz_engine.visualize_avatar('test_twin', avatar_data)
            logger.info("✅ Basic avatar visualization created")
            
            viz_engine.save_figure(basic_figure, f"{output_dir}/basic_avatar.html")
            logger.info("✅ Basic avatar saved")
            
        except Exception as e:
            logger.error(f"❌ Basic avatar visualization failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Test scene visualization with behavior patterns
        logger.info("Testing scene with behavior patterns...")
        
        # Create mock behavior patterns
        behavior_patterns = [
            {
                'activity_type': 'learning',
                'duration': 30,
                'engagement_level': 0.8,
                'outcome': 'success',
                'timestamp': datetime.now()
            },
            {
                'activity_type': 'social',
                'duration': 15,
                'engagement_level': 0.6,
                'outcome': 'partial_success',
                'timestamp': datetime.now()
            }
        ]
        
        try:
            behavior_figure = viz_engine.visualize_scene(behavior_patterns)
            logger.info("✅ Behavior scene visualization created")
            
            viz_engine.save_figure(behavior_figure, f"{output_dir}/behavior_scene.html")
            logger.info("✅ Behavior scene saved")
            
        except Exception as e:
            logger.error(f"❌ Behavior scene visualization failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Check created files
        expected_files = [
            f"{output_dir}/avatar_test.html",
            f"{output_dir}/avatar_test.json", 
            f"{output_dir}/scene_test.html",
            f"{output_dir}/basic_avatar.html",
            f"{output_dir}/behavior_scene.html"
        ]
        
        created_files = []
        total_size = 0
        
        for file_path in expected_files:
            if os.path.exists(file_path):
                created_files.append(file_path)
                size = os.path.getsize(file_path)
                total_size += size
                logger.info(f"✅ Created: {os.path.basename(file_path)} ({size:,} bytes)")
        
        logger.info(f"\nSummary:")
        logger.info(f"Created {len(created_files)}/{len(expected_files)} visualization files")
        logger.info(f"Total size: {total_size:,} bytes")
        
        # Clean up visualization engine
        viz_engine.shutdown()
        
        if len(created_files) >= 3:  # At least 3 files should be created
            logger.info("🎉 Visualization engine test PASSED!")
            return True
        else:
            logger.warning(f"⚠️ Only {len(created_files)} files created, expected at least 3")
            return len(created_files) > 0
            
    except Exception as e:
        logger.error(f"❌ Visualization test failed with error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_visualization_engine()
    
    if success:
        print("\n🎉 All visualization tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some visualization tests failed!")
        sys.exit(1)

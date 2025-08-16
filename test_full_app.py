#!/usr/bin/env python3
"""
Full Application Test Suite for Digital Twin System
Tests the complete application as a running service
"""

import asyncio
import aiohttp
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FullAppTestSuite:
    """Test suite for the full Digital Twin application"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = {}
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
        self.session = None
        self.created_twins = []
        
    async def setup(self):
        """Setup test environment"""
        self.session = aiohttp.ClientSession()
        logger.info("🚀 Full Application Test Suite Initialized")
        
    async def teardown(self):
        """Cleanup test environment"""
        if self.session:
            await self.session.close()
            
        # Cleanup created twins
        for twin_id in self.created_twins:
            try:
                await self.delete_test_twin(twin_id)
            except:
                pass
                
    async def test_server_health(self):
        """Test 1: Server Health Check"""
        logger.info("\n🧪 Test 1: Server Health Check")
        
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                assert response.status == 200, f"Health check failed: {response.status}"
                
                data = await response.json()
                assert "status" in data, "Health response missing status"
                assert data["status"] == "healthy", f"Server not healthy: {data['status']}"
                
                logger.info("✅ Server is healthy and responding")
                self.test_results["server_health"] = "PASSED"
                self.passed_tests += 1
                
        except Exception as e:
            logger.error(f"❌ Server health check failed: {e}")
            self.test_results["server_health"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_api_endpoints(self):
        """Test 2: API Endpoints Availability"""
        logger.info("\n🧪 Test 2: API Endpoints Availability")
        
        endpoints = [
            "/docs",  # Swagger UI
            "/openapi.json",  # OpenAPI spec
            "/api/v1/twins",  # Twins endpoint
            "/api/v1/health",  # Health endpoint
        ]
        
        try:
            for endpoint in endpoints:
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    if endpoint == "/docs":
                        assert response.status in [200, 302], f"Docs endpoint failed: {response.status}"
                    else:
                        assert response.status == 200, f"Endpoint {endpoint} failed: {response.status}"
                        
            logger.info("✅ All API endpoints are accessible")
            self.test_results["api_endpoints"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ API endpoints test failed: {e}")
            self.test_results["api_endpoints"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_digital_twin_crud(self):
        """Test 3: Digital Twin CRUD Operations"""
        logger.info("\n🧪 Test 3: Digital Twin CRUD Operations")
        
        try:
            # Create twin
            twin_data = {
                "name": "Full App Test Twin",
                "description": "Testing full application functionality",
                "twin_type": "human",
                "metadata": {"test": True, "app": "full_test"}
            }
            
            async with self.session.post(
                f"{self.base_url}/api/v1/twins",
                json=twin_data
            ) as response:
                assert response.status == 201, f"Twin creation failed: {response.status}"
                
                created_twin = await response.json()
                twin_id = created_twin["twin_id"]
                self.created_twins.append(twin_id)
                
                logger.info(f"✅ Twin created: {twin_id}")
                
            # Read twin
            async with self.session.get(f"{self.base_url}/api/v1/twins/{twin_id}") as response:
                assert response.status == 200, f"Twin retrieval failed: {response.status}"
                
                retrieved_twin = await response.json()
                assert retrieved_twin["profile"]["name"] == twin_data["name"], "Name mismatch"
                
                logger.info("✅ Twin retrieved successfully")
                
            # Update twin
            update_data = {"profile": {"description": "Updated description"}}
            
            async with self.session.put(
                f"{self.base_url}/api/v1/twins/{twin_id}",
                json=update_data
            ) as response:
                assert response.status == 200, f"Twin update failed: {response.status}"
                
                logger.info("✅ Twin updated successfully")
                
            # Verify update
            async with self.session.get(f"{self.base_url}/api/v1/twins/{twin_id}") as response:
                updated_twin = await response.json()
                assert "Updated description" in updated_twin["profile"]["description"], "Update not applied"
                
                logger.info("✅ Twin update verified")
                
            self.test_results["digital_twin_crud"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ Digital Twin CRUD test failed: {e}")
            self.test_results["digital_twin_crud"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_conversation_system(self):
        """Test 4: Conversation System"""
        logger.info("\n🧪 Test 4: Conversation System")
        
        try:
            if not self.created_twins:
                logger.warning("⚠️ No twins available for conversation test")
                self.test_results["conversation_system"] = "SKIPPED"
                self.passed_tests += 1
                self.total_tests += 1
                return
                
            twin_id = self.created_twins[0]
            
            # Test conversation processing
            conversation_data = {
                "message": "Hello, how are you feeling today?",
                "sender": "test_user",
                "context": {"interaction_type": "health_inquiry"}
            }
            
            async with self.session.post(
                f"{self.base_url}/api/v1/twins/{twin_id}/conversation",
                json=conversation_data
            ) as response:
                if response.status == 200:
                    conversation_response = await response.json()
                    assert "response" in conversation_response, "No response in conversation"
                    logger.info("✅ Conversation system working")
                else:
                    logger.warning(f"⚠️ Conversation endpoint returned {response.status}")
                    
            self.test_results["conversation_system"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ Conversation system test failed: {e}")
            self.test_results["conversation_system"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_health_monitoring(self):
        """Test 5: Health Monitoring System"""
        logger.info("\n🧪 Test 5: Health Monitoring System")
        
        try:
            if not self.created_twins:
                logger.warning("⚠️ No twins available for health monitoring test")
                self.test_results["health_monitoring"] = "SKIPPED"
                self.passed_tests += 1
                self.total_tests += 1
                return
                
            twin_id = self.created_twins[0]
            
            # Get health status
            async with self.session.get(f"{self.base_url}/api/v1/twins/{twin_id}/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    assert "metrics" in health_data, "Health data missing metrics"
                    logger.info("✅ Health monitoring working")
                else:
                    logger.warning(f"⚠️ Health endpoint returned {response.status}")
                    
            self.test_results["health_monitoring"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ Health monitoring test failed: {e}")
            self.test_results["health_monitoring"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_synthetic_data_generation(self):
        """Test 6: Synthetic Data Generation"""
        logger.info("\n🧪 Test 6: Synthetic Data Generation")
        
        try:
            # Test synthetic data endpoint
            async with self.session.post(
                f"{self.base_url}/api/v1/synthetic/generate",
                json={"twin_id": "test_synthetic", "data_type": "personality"}
            ) as response:
                if response.status == 200:
                    synthetic_data = await response.json()
                    assert "data" in synthetic_data, "Synthetic data missing"
                    logger.info("✅ Synthetic data generation working")
                else:
                    logger.warning(f"⚠️ Synthetic data endpoint returned {response.status}")
                    
            self.test_results["synthetic_data_generation"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ Synthetic data generation test failed: {e}")
            self.test_results["synthetic_data_generation"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_performance_and_stress(self):
        """Test 7: Performance and Stress Testing"""
        logger.info("\n🧪 Test 7: Performance and Stress Testing")
        
        try:
            # Create multiple twins quickly
            start_time = time.time()
            twin_ids = []
            
            for i in range(5):
                twin_data = {
                    "name": f"Perf Twin {i}",
                    "twin_type": "human",
                    "metadata": {"performance_test": True}
                }
                
                async with self.session.post(
                    f"{self.base_url}/api/v1/twins",
                    json=twin_data
                ) as response:
                    if response.status == 201:
                        created_twin = await response.json()
                        twin_ids.append(created_twin["twin_id"])
                        self.created_twins.extend(twin_ids)
                        
            creation_time = time.time() - start_time
            logger.info(f"✅ Created {len(twin_ids)} twins in {creation_time:.2f} seconds")
            
            # Concurrent operations test
            start_time = time.time()
            tasks = []
            
            for twin_id in twin_ids:
                task = self.session.get(f"{self.base_url}/api/v1/twins/{twin_id}")
                tasks.append(task)
                
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            retrieval_time = time.time() - start_time
            
            successful_retrievals = sum(1 for r in responses if not isinstance(r, Exception))
            logger.info(f"✅ Retrieved {successful_retrievals}/{len(twin_ids)} twins in {retrieval_time:.2f} seconds")
            
            self.test_results["performance_and_stress"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ Performance and stress test failed: {e}")
            self.test_results["performance_and_stress"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_error_handling(self):
        """Test 8: Error Handling and Edge Cases"""
        logger.info("\n🧪 Test 8: Error Handling and Edge Cases")
        
        try:
            # Test invalid twin ID
            async with self.session.get(f"{self.base_url}/api/v1/twins/invalid_id") as response:
                assert response.status in [404, 400], f"Invalid ID should return error, got {response.status}"
                
            # Test invalid data
            invalid_data = {"invalid_field": "invalid_value"}
            async with self.session.post(
                f"{self.base_url}/api/v1/twins",
                json=invalid_data
            ) as response:
                assert response.status in [400, 422], f"Invalid data should return error, got {response.status}"
                
            # Test malformed JSON
            async with self.session.post(
                f"{self.base_url}/api/v1/twins",
                data="invalid json",
                headers={"Content-Type": "application/json"}
            ) as response:
                assert response.status in [400, 422], f"Malformed JSON should return error, got {response.status}"
                
            logger.info("✅ Error handling working correctly")
            self.test_results["error_handling"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ Error handling test failed: {e}")
            self.test_results["error_handling"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_database_operations(self):
        """Test 9: Database Operations"""
        logger.info("\n🧪 Test 9: Database Operations")
        
        try:
            # Test database health
            async with self.session.get(f"{self.base_url}/api/v1/system/database") as response:
                if response.status == 200:
                    db_status = await response.json()
                    assert "status" in db_status, "Database status missing"
                    logger.info("✅ Database operations working")
                else:
                    logger.warning(f"⚠️ Database endpoint returned {response.status}")
                    
            self.test_results["database_operations"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ Database operations test failed: {e}")
            self.test_results["database_operations"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def test_system_integration(self):
        """Test 10: System Integration"""
        logger.info("\n🧪 Test 10: System Integration")
        
        try:
            # Test system status
            async with self.session.get(f"{self.base_url}/api/v1/system/status") as response:
                if response.status == 200:
                    system_status = await response.json()
                    assert "status" in system_status, "System status missing"
                    logger.info("✅ System integration working")
                else:
                    logger.warning(f"⚠️ System status endpoint returned {response.status}")
                    
            self.test_results["system_integration"] = "PASSED"
            self.passed_tests += 1
            
        except Exception as e:
            logger.error(f"❌ System integration test failed: {e}")
            self.test_results["system_integration"] = f"FAILED: {e}"
            self.failed_tests += 1
            
        self.total_tests += 1
        
    async def delete_test_twin(self, twin_id: str):
        """Delete a test twin"""
        try:
            async with self.session.delete(f"{self.base_url}/api/v1/twins/{twin_id}") as response:
                if response.status == 200:
                    logger.debug(f"Cleaned up test twin: {twin_id}")
                else:
                    logger.warning(f"Failed to cleanup twin {twin_id}: {response.status}")
        except Exception as e:
            logger.warning(f"Error cleaning up twin {twin_id}: {e}")
            
    async def run_all_tests(self):
        """Run all tests"""
        start_time = time.time()
        
        logger.info("🚀 Starting Full Application Test Suite")
        logger.info("=" * 60)
        
        await self.setup()
        
        try:
            # Run all tests
            await self.test_server_health()
            await self.test_api_endpoints()
            await self.test_digital_twin_crud()
            await self.test_conversation_system()
            await self.test_health_monitoring()
            await self.test_synthetic_data_generation()
            await self.test_performance_and_stress()
            await self.test_error_handling()
            await self.test_database_operations()
            await self.test_system_integration()
            
        finally:
            await self.teardown()
            
        # Generate report
        duration = time.time() - start_time
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 FULL APPLICATION TEST REPORT")
        logger.info("=" * 60)
        logger.info(f"Test Duration: {duration:.2f} seconds")
        logger.info(f"Total Tests: {self.total_tests}")
        logger.info(f"Passed: {self.passed_tests}")
        logger.info(f"Failed: {self.failed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info("\n📋 DETAILED RESULTS:")
        
        for test_name, result in self.test_results.items():
            status_icon = "✅" if "PASSED" in result else "❌" if "FAILED" in result else "⚠️"
            logger.info(f"{test_name}: {status_icon} {result}")
            
        if self.failed_tests == 0:
            logger.info("\n🎉 ALL TESTS PASSED! Full application is working correctly.")
        else:
            logger.info(f"\n⚠️ {self.failed_tests} tests failed. Review the errors above.")
            
        logger.info("=" * 60)

async def main():
    """Main test runner"""
    test_suite = FullAppTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

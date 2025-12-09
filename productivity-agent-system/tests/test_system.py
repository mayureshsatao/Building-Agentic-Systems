"""
Test Suite for Personal Productivity Agentic System
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath( __file__))))

import unittest
import json
from datetime import datetime, timedelta

from tools.workflow_optimizer import WorkflowOptimizerTool
from tools.date_calculator import DateCalculatorTool
from tools.file_processor import FileProcessorTool


class TestWorkflowOptimizer(unittest.TestCase):
    """Test cases for the Workflow Optimizer custom tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.optimizer = WorkflowOptimizerTool()
    
    def test_log_completion(self):
        """Test logging a completed task"""
        params = {
            "action": "log",
            "user_id": "test_user",
            "task_id": "test_task_1",
            "task_name": "Test Task",
            "completed_at": datetime.now().isoformat(),
            "duration_minutes": 60,
            "priority": "high",
            "was_on_time": True
        }
        
        result = self.optimizer._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertEqual(result_data["status"], "logged")
        self.assertIn("entry", result_data)
    
    def test_insufficient_data_analysis(self):
        """Test analysis with insufficient data"""
        params = {
            "action": "analyze",
            "user_id": "new_user",
            "time_range": "week"
        }
        
        result = self.optimizer._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertEqual(result_data.get("status"), "insufficient_data")
    
    def test_recommendations_generation(self):
        """Test generating recommendations"""
        # First log some tasks
        for i in range(6):
            params = {
                "action": "log",
                "user_id": "test_rec_user",
                "task_id": f"task_{i}",
                "task_name": f"Task {i}",
                "completed_at": (datetime.now() - timedelta(days=i)).isoformat(),
                "duration_minutes": 60,
                "priority": "medium",
                "was_on_time": True
            }
            self.optimizer._run(json.dumps(params))
        
        # Now get recommendations
        params = {
            "action": "recommend",
            "user_id": "test_rec_user",
            "time_range": "week"
        }
        
        result = self.optimizer._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertIn("recommendations", result_data)
        self.assertIsInstance(result_data["recommendations"], list)


class TestDateCalculator(unittest.TestCase):
    """Test cases for the Date Calculator tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = DateCalculatorTool()
    
    def test_days_until_deadline(self):
        """Test calculating days until deadline"""
        future_date = (datetime.now() + timedelta(days=5)).isoformat()
        params = {
            "action": "days_until",
            "deadline": future_date
        }
        
        result = self.calculator._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertIn("days_remaining", result_data)
        self.assertEqual(result_data["days_remaining"], 5)
        self.assertIn("urgency_level", result_data)
    
    def test_add_days_to_date(self):
        """Test adding days to a date"""
        start_date = "2024-01-01"
        params = {
            "action": "add_days",
            "start_date": start_date,
            "days": 10
        }
        
        result = self.calculator._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertEqual(result_data["result_date"], "2024-01-11")
        self.assertIn("day_of_week", result_data)
    
    def test_conflict_detection(self):
        """Test detecting scheduling conflicts"""
        base_time = datetime.now().replace(hour=10, minute=0, second=0)
        
        params = {
            "action": "check_conflict",
            "event1_start": base_time.isoformat(),
            "event1_end": (base_time + timedelta(hours=1)).isoformat(),
            "event2_start": (base_time + timedelta(minutes=30)).isoformat(),
            "event2_end": (base_time + timedelta(hours=1, minutes=30)).isoformat()
        }
        
        result = self.calculator._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertTrue(result_data["has_conflict"])
        self.assertIn("overlap_minutes", result_data)
    
    def test_working_days_calculation(self):
        """Test calculating working days"""
        params = {
            "action": "working_days",
            "start_date": "2024-01-01",  # Monday
            "end_date": "2024-01-07"      # Sunday
        }
        
        result = self.calculator._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertEqual(result_data["working_days"], 5)
        self.assertEqual(result_data["weekend_days"], 2)


class TestFileProcessor(unittest.TestCase):
    """Test cases for the File Processor tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = FileProcessorTool()
    
    def test_save_and_load_task(self):
        """Test saving and loading a task"""
        # Save a task
        save_params = {
            "action": "save",
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high",
            "status": "pending"
        }
        
        save_result = self.processor._run(json.dumps(save_params))
        save_data = json.loads(save_result)
        
        self.assertEqual(save_data["status"], "success")
        self.assertIn("task", save_data)
        
        task_id = save_data["task"]["id"]
        
        # Load tasks
        load_params = {
            "action": "load"
        }
        
        load_result = self.processor._run(json.dumps(load_params))
        load_data = json.loads(load_result)
        
        self.assertGreater(load_data["count"], 0)
        
        # Find our task
        found = False
        for task in load_data["tasks"]:
            if task["id"] == task_id:
                found = True
                self.assertEqual(task["title"], "Test Task")
                break
        
        self.assertTrue(found, "Saved task not found in loaded tasks")
    
    def test_update_task(self):
        """Test updating a task"""
        # First save a task
        save_params = {
            "action": "save",
            "title": "Original Title",
            "priority": "low"
        }
        
        save_result = self.processor._run(json.dumps(save_params))
        save_data = json.loads(save_result)
        task_id = save_data["task"]["id"]
        
        # Update the task
        update_params = {
            "action": "update",
            "task_id": task_id,
            "title": "Updated Title",
            "priority": "high",
            "status": "in_progress"
        }
        
        update_result = self.processor._run(json.dumps(update_params))
        update_data = json.loads(update_result)
        
        self.assertEqual(update_data["status"], "success")
        self.assertEqual(update_data["task"]["title"], "Updated Title")
        self.assertEqual(update_data["task"]["priority"], "high")
    
    def test_generate_report(self):
        """Test generating a task report"""
        params = {
            "action": "report"
        }
        
        result = self.processor._run(json.dumps(params))
        result_data = json.loads(result)
        
        self.assertIn("summary", result_data)
        self.assertIn("total_tasks", result_data["summary"])


class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from task creation to completion"""
        file_processor = FileProcessorTool()
        date_calculator = DateCalculatorTool()
        workflow_optimizer = WorkflowOptimizerTool()
        
        # 1. Create a task
        deadline = (datetime.now() + timedelta(days=3)).isoformat()
        task_params = {
            "action": "save",
            "title": "Integration Test Task",
            "priority": "high",
            "deadline": deadline,
            "estimated_duration": 90
        }
        
        task_result = file_processor._run(json.dumps(task_params))
        task_data = json.loads(task_result)
        self.assertEqual(task_data["status"], "success")
        task_id = task_data["task"]["id"]
        
        # 2. Check deadline urgency
        deadline_params = {
            "action": "days_until",
            "deadline": deadline
        }
        
        deadline_result = date_calculator._run(json.dumps(deadline_params))
        deadline_data = json.loads(deadline_result)
        self.assertIn("urgency_level", deadline_data)
        
        # 3. Complete the task and log it
        completion_params = {
            "action": "log",
            "user_id": "integration_test_user",
            "task_id": task_id,
            "task_name": "Integration Test Task",
            "completed_at": datetime.now().isoformat(),
            "duration_minutes": 85,
            "priority": "high",
            "was_on_time": True
        }
        
        completion_result = workflow_optimizer._run(json.dumps(completion_params))
        completion_data = json.loads(completion_result)
        self.assertEqual(completion_data["status"], "logged")


def run_tests():
    """Run all tests and generate report"""
    print("\n" + "=" * 70)
    print(" " * 15 + "PRODUCTIVITY SYSTEM TEST SUITE")
    print("=" * 70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestDateCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestFileProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70 + "\n")
    
    return result


if __name__ == "__main__":
    run_tests()

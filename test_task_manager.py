#!/usr/bin/env python3
"""
Tests for TaskManager class to verify the interface matches issue requirements.
"""

import os
import tempfile
import unittest
from main import TaskManager


class TestTaskManager(unittest.TestCase):
    """Test TaskManager class interface and functionality"""
    
    def setUp(self):
        """Set up test fixture with temporary data file"""
        # Use a temporary file to avoid interfering with real data
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.task_manager = TaskManager(data_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixture"""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task_with_title_parameter(self):
        """Test that add_task accepts title parameter as specified in issue"""
        # This should work without errors
        self.task_manager.add_task(title="Test task")
        
        # Verify task was added
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertIn("Test task", tasks[0])
    
    def test_list_tasks_returns_list_of_strings(self):
        """Test that list_tasks returns List[str] as specified in issue"""
        # Add some tasks
        self.task_manager.add_task("First task")
        self.task_manager.add_task("Second task")
        
        # Get task list
        tasks = self.task_manager.list_tasks()
        
        # Verify return type
        self.assertIsInstance(tasks, list)
        self.assertTrue(all(isinstance(task, str) for task in tasks))
        self.assertEqual(len(tasks), 2)
        
        # Verify content
        self.assertIn("First task", tasks[0])
        self.assertIn("Second task", tasks[1])
    
    def test_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that list_tasks returns empty list when no tasks exist"""
        tasks = self.task_manager.list_tasks()
        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 0)
    
    def test_delete_task_with_task_id(self):
        """Test that delete_task accepts task_id parameter as specified in issue"""
        # Add a task
        self.task_manager.add_task("Task to delete")
        tasks_before = self.task_manager.list_tasks()
        self.assertEqual(len(tasks_before), 1)
        
        # Delete the task (ID should be 1 for first task)
        self.task_manager.delete_task(task_id=1)
        
        # Verify task was deleted
        tasks_after = self.task_manager.list_tasks()
        self.assertEqual(len(tasks_after), 0)
    
    def test_auto_incrementing_ids(self):
        """Test that tasks have auto-incrementing IDs"""
        # Add multiple tasks
        self.task_manager.add_task("Task 1")
        self.task_manager.add_task("Task 2")
        self.task_manager.add_task("Task 3")
        
        # Get task list
        tasks = self.task_manager.list_tasks()
        
        # Verify IDs are present and incrementing
        self.assertIn("1", tasks[0])  # First task should have ID 1
        self.assertIn("2", tasks[1])  # Second task should have ID 2
        self.assertIn("3", tasks[2])  # Third task should have ID 3
    
    def test_interface_matches_issue_requirements(self):
        """Integration test to verify complete interface matches issue requirements"""
        # Test add_task(title: str)
        self.task_manager.add_task(title="Test task")
        
        # Test list_tasks() -> List[str]
        task_list = self.task_manager.list_tasks()
        self.assertIsInstance(task_list, list)
        self.assertTrue(all(isinstance(task, str) for task in task_list))
        
        # Test delete_task(task_id: int)
        self.task_manager.delete_task(task_id=1)
        
        # Verify deletion worked
        empty_list = self.task_manager.list_tasks()
        self.assertEqual(len(empty_list), 0)


if __name__ == '__main__':
    unittest.main()
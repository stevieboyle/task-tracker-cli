#!/usr/bin/env python3
"""
Task Tracker CLI - A simple command-line task management tool
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional


class TaskManager:
    """Manages tasks with basic CRUD operations"""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_tasks(self) -> None:
        """Save tasks to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, title: str) -> None:
        """Add a new task"""
        task = {
            "id": self._get_next_id(),
            "description": title,
            "status": "todo",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self._save_tasks()
        print(f"Task added successfully (ID: {task['id']})")
    
    def list_tasks(self) -> List[str]:
        """List all tasks"""
        if not self.tasks:
            return []
        
        task_list = []
        for task in self.tasks:
            task_list.append(f"{task['id']:<4} {task['status']:<10} {task['description']}")
        return task_list
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID"""
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        
        if len(self.tasks) < original_count:
            self._save_tasks()
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Task with ID {task_id} not found.")
    
    def _get_next_id(self) -> int:
        """Get the next available ID"""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - Manage your tasks from the command line",
        prog="task-tracker"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID to delete')
    
    args = parser.parse_args()
    
    # Show help if no command provided
    if args.command is None:
        parser.print_help()
        return
    
    # Initialize task manager
    task_manager = TaskManager()
    
    # Execute commands
    if args.command == 'add':
        task_manager.add_task(args.description)
    elif args.command == 'list':
        tasks = task_manager.list_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            print(f"{'ID':<4} {'Status':<10} {'Description'}")
            print("-" * 50)
            for task in tasks:
                print(task)
    elif args.command == 'delete':
        task_manager.delete_task(args.id)


if __name__ == "__main__":
    main()
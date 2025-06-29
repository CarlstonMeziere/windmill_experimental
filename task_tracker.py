#!/usr/bin/env python3
"""
Task Tracker for Felicia UI Mockup Project
Parses UI_MOCKUP_TASKS.md and provides task management functionality
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import argparse
import json
from datetime import datetime


@dataclass
class Task:
    """Represents a single task in the hierarchy"""
    id: str
    level: int
    description: str
    is_complete: bool
    line_number: int
    parent_id: Optional[str] = None
    children: List[str] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class TaskTracker:
    """Manages task hierarchy and provides analysis functions"""
    
    def __init__(self, markdown_file: str = "UI_MOCKUP_TASKS.md"):
        self.markdown_file = Path(markdown_file)
        self.tasks: Dict[str, Task] = {}
        self.line_mapping: Dict[int, str] = {}
        self.parse_markdown()
    
    def parse_markdown(self):
        """Parse the markdown file and build task hierarchy"""
        if not self.markdown_file.exists():
            raise FileNotFoundError(f"Task file {self.markdown_file} not found")
        
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        task_pattern = re.compile(r'^(\s*)-\s*\[([ x])\]\s*\*\*([0-9.]+)\*\*\s*(.+?)(?:\s*-\s*(.+))?$')
        current_parents = {}
        
        for line_num, line in enumerate(lines, 1):
            match = task_pattern.match(line)
            if match:
                indent_level = len(match.group(1)) // 2
                is_complete = match.group(2).lower() == 'x'
                task_id = match.group(3)
                task_name = match.group(4)
                task_desc = match.group(5) or ""
                
                # Determine task level from ID
                level = len(task_id.split('.'))
                
                # Determine parent ID
                parent_id = None
                if '.' in task_id:
                    parent_parts = task_id.split('.')[:-1]
                    parent_id = '.'.join(parent_parts)
                
                # Create task
                task = Task(
                    id=task_id,
                    level=level,
                    description=f"{task_name} - {task_desc}".strip(' -'),
                    is_complete=is_complete,
                    line_number=line_num,
                    parent_id=parent_id
                )
                
                self.tasks[task_id] = task
                self.line_mapping[line_num] = task_id
                
                # Update parent's children list
                if parent_id and parent_id in self.tasks:
                    self.tasks[parent_id].children.append(task_id)
    
    def get_task_summary(self) -> Dict[str, any]:
        """Get overall task completion summary"""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() if t.is_complete)
        
        # Group by level
        by_level = {}
        for task in self.tasks.values():
            level = task.level
            if level not in by_level:
                by_level[level] = {'total': 0, 'completed': 0}
            by_level[level]['total'] += 1
            if task.is_complete:
                by_level[level]['completed'] += 1
        
        # Group by domain (level 1)
        by_domain = {}
        for task_id, task in self.tasks.items():
            if task.level == 1:
                domain_id = task_id
                by_domain[domain_id] = self._get_subtree_stats(domain_id)
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_percentage': round((completed_tasks / total_tasks) * 100, 2),
            'by_level': by_level,
            'by_domain': by_domain,
            'last_updated': datetime.now().isoformat()
        }
    
    def _get_subtree_stats(self, task_id: str) -> Dict[str, any]:
        """Get statistics for a task and all its children"""
        task = self.tasks.get(task_id)
        if not task:
            return {}
        
        stats = {
            'id': task_id,
            'description': task.description,
            'is_complete': task.is_complete,
            'line_number': task.line_number,
            'total_subtasks': 0,
            'completed_subtasks': 0,
            'completion_percentage': 0.0
        }
        
        # Count this task and all descendants
        all_descendants = self._get_all_descendants(task_id)
        stats['total_subtasks'] = len(all_descendants)
        stats['completed_subtasks'] = sum(1 for tid in all_descendants 
                                        if self.tasks[tid].is_complete)
        
        if stats['total_subtasks'] > 0:
            stats['completion_percentage'] = round(
                (stats['completed_subtasks'] / stats['total_subtasks']) * 100, 2
            )
        
        return stats
    
    def _get_all_descendants(self, task_id: str) -> List[str]:
        """Get all descendant task IDs"""
        descendants = [task_id]
        task = self.tasks.get(task_id)
        if task and task.children:
            for child_id in task.children:
                descendants.extend(self._get_all_descendants(child_id))
        return descendants
    
    def validate_completion_rules(self) -> List[str]:
        """Check if parent tasks are incorrectly marked complete"""
        violations = []
        
        for task_id, task in self.tasks.items():
            if task.is_complete and task.children:
                # Check if all children are complete
                incomplete_children = [
                    child_id for child_id in task.children
                    if not self.tasks[child_id].is_complete
                ]
                if incomplete_children:
                    violations.append(
                        f"Task {task_id} (line {task.line_number}) is marked complete "
                        f"but has {len(incomplete_children)} incomplete children: "
                        f"{', '.join(incomplete_children)}"
                    )
        
        return violations
    
    def get_next_tasks(self, limit: int = 10) -> List[Task]:
        """Get next actionable tasks (leaf tasks that aren't complete)"""
        actionable = []
        
        for task in self.tasks.values():
            # A task is actionable if it's not complete and has no children
            if not task.is_complete and not task.children:
                actionable.append(task)
        
        # Sort by ID to maintain order
        actionable.sort(key=lambda t: [int(x) for x in t.id.split('.')])
        
        return actionable[:limit]
    
    def update_task_status(self, task_id: str, complete: bool = True) -> Tuple[bool, str]:
        """Update a task's completion status"""
        if task_id not in self.tasks:
            return False, f"Task {task_id} not found"
        
        task = self.tasks[task_id]
        
        # Check if we can mark it complete
        if complete and task.children:
            incomplete_children = [
                child_id for child_id in task.children
                if not self.tasks[child_id].is_complete
            ]
            if incomplete_children:
                return False, (f"Cannot mark {task_id} complete. "
                             f"Incomplete children: {', '.join(incomplete_children)}")
        
        # Update the file
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        line_idx = task.line_number - 1
        if complete:
            lines[line_idx] = lines[line_idx].replace('[ ]', '[x]')
        else:
            lines[line_idx] = lines[line_idx].replace('[x]', '[ ]')
        
        with open(self.markdown_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        # Reload to ensure consistency
        self.tasks.clear()
        self.line_mapping.clear()
        self.parse_markdown()
        
        return True, f"Task {task_id} marked {'complete' if complete else 'incomplete'}"
    
    def export_json(self, output_file: str = "task_status.json"):
        """Export task status to JSON"""
        data = {
            'summary': self.get_task_summary(),
            'tasks': {
                task_id: {
                    'id': task.id,
                    'level': task.level,
                    'description': task.description,
                    'is_complete': task.is_complete,
                    'line_number': task.line_number,
                    'parent_id': task.parent_id,
                    'children': task.children
                }
                for task_id, task in self.tasks.items()
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return output_file


def main():
    """CLI interface for task tracker"""
    parser = argparse.ArgumentParser(description="Track Felicia UI Mockup tasks")
    parser.add_argument('command', choices=['summary', 'validate', 'next', 'complete', 'export'],
                       help='Command to execute')
    parser.add_argument('--task-id', help='Task ID for complete command')
    parser.add_argument('--limit', type=int, default=10, help='Limit for next tasks')
    parser.add_argument('--output', default='task_status.json', help='Output file for export')
    
    args = parser.parse_args()
    
    tracker = TaskTracker()
    
    if args.command == 'summary':
        summary = tracker.get_task_summary()
        print(f"\n📊 Task Summary")
        print(f"{'='*50}")
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Completed: {summary['completed_tasks']}")
        print(f"Overall Progress: {summary['completion_percentage']}%")
        
        print(f"\n📈 Progress by Level:")
        for level, stats in summary['by_level'].items():
            pct = round((stats['completed'] / stats['total']) * 100, 2)
            print(f"  Level {level}: {stats['completed']}/{stats['total']} ({pct}%)")
        
        print(f"\n🏗️ Progress by Domain:")
        for domain_id, stats in summary['by_domain'].items():
            print(f"  {stats['description']}")
            print(f"    └─ {stats['completed_subtasks']}/{stats['total_subtasks']} "
                  f"({stats['completion_percentage']}%)")
    
    elif args.command == 'validate':
        violations = tracker.validate_completion_rules()
        if violations:
            print(f"\n❌ Validation Errors Found:")
            for violation in violations:
                print(f"  - {violation}")
        else:
            print(f"\n✅ All completion rules are satisfied!")
    
    elif args.command == 'next':
        tasks = tracker.get_next_tasks(args.limit)
        print(f"\n📋 Next {len(tasks)} Tasks to Work On:")
        print(f"{'='*80}")
        for task in tasks:
            parent_desc = ""
            if task.parent_id:
                parent = tracker.tasks.get(task.parent_id)
                if parent:
                    parent_desc = f" [{parent.description}]"
            print(f"{task.id} (line {task.line_number}){parent_desc}")
            print(f"  └─ {task.description}")
            print()
    
    elif args.command == 'complete':
        if not args.task_id:
            print("❌ Error: --task-id required for complete command")
            return
        
        success, message = tracker.update_task_status(args.task_id)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    elif args.command == 'export':
        output_file = tracker.export_json(args.output)
        print(f"✅ Task data exported to {output_file}")


if __name__ == "__main__":
    main()
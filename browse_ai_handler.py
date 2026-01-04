import requests
from config import BROWSE_AI_API_KEY

class BrowseAIHandler:
    def __init__(self):
        self.api_key = BROWSE_AI_API_KEY
        self.base_url = "https://api.browse.ai/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def get_robot_monitors(self, robot_id):
        """Get list of monitors for a robot"""
        url = f"{self.base_url}/robots/{robot_id}/monitors"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            monitors = data.get('result', {}).get('monitors', {}).get('items', [])
            return monitors
        
        print(f"⚠️ Failed to get monitors: {response.status_code}")
        return []
    
    def get_latest_task(self, robot_id):
        """Get the latest successful task for a robot (includes monitor tasks)"""
        url = f"{self.base_url}/robots/{robot_id}/tasks"
        params = {"page": 1}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('result', {}).get('robotTasks', {}).get('items', [])
            
            # Prioritize monitor tasks over manual tasks
            monitor_tasks = [t for t in tasks if t.get('runByTaskMonitorId') is not None]
            
            if monitor_tasks:
                # Return latest monitor task
                for task in monitor_tasks:
                    if task.get('status') == 'successful':
                        return task
            
            # Fallback to any successful task
            for task in tasks:
                if task.get('status') == 'successful':
                    return task
        
        return None
    
    def get_captured_data(self, robot_id, new_only=True):
        """
        Get captured data from latest task
        
        Args:
            robot_id: Browse AI robot ID
            new_only: If True, return only NEW items from monitoring
        """
        task = self.get_latest_task(robot_id)
        
        if not task:
            print(f"⚠️ No tasks found for robot {robot_id}")
            return []
        
        # Check if this is a monitor task
        is_monitor = task.get('runByTaskMonitorId') is not None
        
        # Get items
        captured_lists = task.get('capturedLists', {})
        items = []
        for list_name, list_items in captured_lists.items():
            items = list_items
            break
        
        if not items:
            return []
        
        # Filter for NEW items only
        if new_only:
            if not is_monitor:
                print(f"⚠️ Robot {robot_id}: Latest task is manual (not from monitoring)")
                print(f"   Tip: Wait for next monitoring run or use new_only=False to test")
                return []
            
            # Check for _STATUS field
            has_status = any('_STATUS' in item for item in items)
            
            if not has_status:
                print(f"⚠️ Robot {robot_id}: First monitor run (establishing baseline)")
                print(f"   Next monitoring run will detect changes")
                return []
            
            # Return only NEW items
            new_items = [item for item in items if item.get('_STATUS') == 'NEW']
            
            if new_items:
                print(f"✅ Robot {robot_id}: Found {len(new_items)} NEW items (out of {len(items)} total)")
            else:
                print(f"✅ Robot {robot_id}: No NEW items (all {len(items)} items unchanged)")
            
            return new_items
        
        # Return all items if new_only=False
        print(f"✅ Robot {robot_id}: Fetched {len(items)} items (test mode)")
        return items

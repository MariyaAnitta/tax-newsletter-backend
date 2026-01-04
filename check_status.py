from browse_ai_handler import BrowseAIHandler
from config import CIRCULARS_ROBOT_ID
import requests
from datetime import datetime

handler = BrowseAIHandler()

print("="*60)
print("🔍 BROWSE AI TASK CHECKER")
print("="*60)

# Check monitors
print("\n📊 Checking Monitors...")
monitors = handler.get_robot_monitors(CIRCULARS_ROBOT_ID)
if monitors:
    for monitor in monitors:
        print(f"  ✅ Monitor: {monitor.get('name')}")
        print(f"     ID: {monitor.get('id')}")
        print(f"     Status: {monitor.get('status')}")
        print(f"     Schedule: {monitor.get('schedule')}")
else:
    print("  ⚠️ No monitors found")

# Get all recent tasks
print("\n📋 Checking Recent Tasks...")
url = f"{handler.base_url}/robots/{CIRCULARS_ROBOT_ID}/tasks"
response = requests.get(url, headers=handler.headers, params={"page": 1})

if response.status_code == 200:
    tasks = response.json()['result']['robotTasks']['items']
    
    print(f"Found {len(tasks)} recent tasks:\n")
    
    monitor_tasks = []
    manual_tasks = []
    
    for task in tasks:
        if task.get('runByTaskMonitorId'):
            monitor_tasks.append(task)
        else:
            manual_tasks.append(task)
    
    print(f"🤖 Monitor Tasks: {len(monitor_tasks)}")
    print(f"👤 Manual Tasks: {len(manual_tasks)}\n")
    
    # Show monitor tasks first
    if monitor_tasks:
        print("="*60)
        print("🤖 MONITOR TASKS (Most Recent)")
        print("="*60)
        for i, task in enumerate(monitor_tasks[:3], 1):
            created = datetime.fromtimestamp(task['createdAt'] / 1000)
            print(f"\n{i}. Monitor Task")
            print(f"   ID: {task['id']}")
            print(f"   Created: {created.strftime('%Y-%m-%d %H:%M:%S IST')}")
            print(f"   Monitor ID: {task.get('runByTaskMonitorId')}")
            
            # Check _STATUS
            captured_lists = task.get('capturedLists', {})
            for list_name, items in captured_lists.items():
                if items:
                    has_status = '_STATUS' in items[0]
                    if has_status:
                        statuses = {}
                        for item in items:
                            status = item.get('_STATUS', 'none')
                            statuses[status] = statuses.get(status, 0) + 1
                        print(f"   Items: {statuses}")
                    else:
                        print(f"   Items: {len(items)} (no _STATUS - baseline run)")
                break
    else:
        print("\n⚠️ NO MONITOR TASKS FOUND!")
        print("This means monitoring hasn't run yet, or tasks aren't being captured.")
    
    # Show one manual task for comparison
    if manual_tasks:
        print("\n" + "="*60)
        print("👤 MANUAL TASKS (Latest)")
        print("="*60)
        task = manual_tasks[0]
        created = datetime.fromtimestamp(task['createdAt'] / 1000)
        print(f"\nManual Task")
        print(f"   ID: {task['id']}")
        print(f"   Created: {created.strftime('%Y-%m-%d %H:%M:%S IST')}")
        
        captured_lists = task.get('capturedLists', {})
        for list_name, items in captured_lists.items():
            if items:
                has_status = '_STATUS' in items[0]
                if has_status:
                    statuses = {}
                    for item in items:
                        status = item.get('_STATUS', 'none')
                        statuses[status] = statuses.get(status, 0) + 1
                    print(f"   Items: {statuses}")
                else:
                    print(f"   Items: {len(items)} (no _STATUS)")
            break

print("\n" + "="*60)
print("✅ Check Complete")
print("="*60)

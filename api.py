from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from main import TaxNewsletterProcessor
from datetime import datetime
import json

app = FastAPI(title="Tax Newsletter API")

# Enable CORS (so frontend can call this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store latest newsletter
latest_newsletter = {
    "status": "not_generated",
    "last_updated": None,
    "data": []
}

def process_newsletter_task():
    """Background task to process newsletter"""
    global latest_newsletter
    
    print("\n🚀 Processing newsletter...")
    latest_newsletter["status"] = "processing"
    
    try:
        processor = TaxNewsletterProcessor()
        
        # Process all data
        processor.process_circulars()
        processor.process_notifications()
        processor.process_press_releases()
        
        # Update global storage
        latest_newsletter = {
            "status": "completed",
            "last_updated": datetime.now().isoformat(),
            "data": processor.processed_data
        }
        
        print("✅ Newsletter processing completed!")
        
    except Exception as e:
        print(f"❌ Error processing newsletter: {e}")
        latest_newsletter["status"] = "error"
        latest_newsletter["error"] = str(e)

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "Tax Newsletter API is running!",
        "status": "healthy",
        "endpoints": {
            "generate": "/api/generate",
            "newsletter": "/api/newsletter",
            "status": "/api/status"
        }
    }

@app.get("/api/generate") 
def generate_newsletter(background_tasks: BackgroundTasks):
    """Trigger newsletter generation"""
    
    if latest_newsletter["status"] == "processing":
        return {
            "message": "Newsletter is already being processed",
            "status": "processing"
        }
    
    # Start background task
    background_tasks.add_task(process_newsletter_task)
    
    return {
        "message": "Newsletter generation started",
        "status": "started"
    }

@app.get("/api/status")
def get_status():
    """Get current processing status"""
    return {
        "status": latest_newsletter["status"],
        "last_updated": latest_newsletter.get("last_updated"),
        "item_count": len(latest_newsletter.get("data", []))
    }

@app.get("/api/newsletter")
def get_newsletter():
    """Get the latest newsletter"""
    
    if latest_newsletter["status"] == "not_generated":
        return {
            "message": "Newsletter not generated yet. Call POST /api/generate first.",
            "status": "not_generated"
        }
    
    if latest_newsletter["status"] == "processing":
        return {
            "message": "Newsletter is being processed. Check /api/status for updates.",
            "status": "processing"
        }
    
    if latest_newsletter["status"] == "error":
        return {
            "message": "Error generating newsletter",
            "status": "error",
            "error": latest_newsletter.get("error")
        }
    
    # Group data by type
    circulars = [d for d in latest_newsletter["data"] if d['type'] == 'Circular']
    notifications = [d for d in latest_newsletter["data"] if d['type'] == 'Notification']
    releases = [d for d in latest_newsletter["data"] if d['type'] == 'Press Release']
    
    return {
        "status": "success",
        "last_updated": latest_newsletter["last_updated"],
        "newsletter": {
            "circulars": circulars,
            "notifications": notifications,
            "press_releases": releases
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

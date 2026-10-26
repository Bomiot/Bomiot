import os

def example_job(**kwargs):
    """Scheduled example job"""
    from datetime import datetime
    print(f"This is a scheduled task test ----------- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Your business logic here
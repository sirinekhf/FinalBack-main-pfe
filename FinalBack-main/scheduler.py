import os
import threading

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

import time
from apscheduler.schedulers.background import BackgroundScheduler
from products.views import importProductAvilabilityJob, importProductAttributesJob, importProductProductJob, importProductPackagingJob, importProductTemplateJob


def execute_job():
    start_time = time.time()
    try:
       #importProductAvilabilityJob()
       importProductAttributesJob()
       #importProductProductJob()
       #importProductPackagingJob()
       #importProductTemplateJob()
    except Exception as e:
        print(e)
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time in seconds
    print(f"Execution time: {execution_time} seconds")

def check_server_status():
    server_status = True
    if server_status:
        execute_job()
def run_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(execute_job, 'cron', hour=0, minute=0)
    scheduler.start()
    check_server_status()
    def scheduler_thread():
        while True:
            time.sleep(1)

    # Start the scheduler in a separate thread
    thread = threading.Thread(target=scheduler_thread, daemon=True)
    thread.start()

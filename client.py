from rq import Queue, Connection, Worker, get_current_job
from rq.job import Job
from rq.registry import FailedJobRegistry
from rq.exceptions import InvalidJobOperation
from rq.serializers import JSONSerializer
from redis import Redis
import traceback
import requests

## This is the exception handler function
def retry_handler(job, exc_type, exc_value, tb):
    ## Increment the failure count in job metadata
    job.meta['failures'] = job.meta.get('failures', 0) + 1
    job.save_meta()  ## Save the updated count

    max_retries = 3
    ## If the failure happens more than max_tries then move the job to the failed queue
    if job.meta['failures'] > max_retries:
        return True  

    ## Re-enqueue the job
    job.status = 'queued'
    queue = Queue(job.origin, connection=job.connection)
    queue.enqueue_job(job)
    return False   ## Return False to indicate the job should be re-tried



class SMSFailedException(Exception):
    pass

def send_sms_via_api(name, mobile_number, message):
    try:
        api_url = "http://localhost:5000/sms-gateway"  # Replace with your API endpoint
        payload = {
            "name": name,
            "mobile_number": mobile_number,
            "message": message
        }
        headers = {'Content-Type': 'application/json'}

        ## Send the sms request to API
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        ## Check the response status
        if result['status'] == 'success':
            print(f"SMS sent successfully to {name} ({mobile_number})")
            return True  
        else:
            raise SMSFailedException(f"Failed to send SMS to {name} ({mobile_number})")
            ## Raise an error when sms sending fails 
    except Exception as e:
        print(f"SMS was not sent to {name} ({mobile_number})")
        raise e
        

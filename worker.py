from redis import Redis
from rq import Worker, Queue, Connection, SimpleWorker
from client import retry_handler


redis_conn = Redis(host='localhost', port=6379, db=0)
task_queue = Queue("sms_queue", connection = redis_conn, exc_handler = retry_handler)


if __name__ == '__main__':
    print("Start working")
    worker = Worker([task_queue], connection=redis_conn)
    worker.work(with_scheduler=True)

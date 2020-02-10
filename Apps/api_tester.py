import requests
import random


import threading
import queue
import sys
import time

from words_data import titles, descriptions

url = "http://127.0.0.1:8000/tasks/"

"""node_urls = {
    "create_task" : "http://127.0.0.1:3000/tasks",
    "update_task" : f"http://127.0.0.1:3000/tasks/{random_id}/status"
} 

django_urls = {
    "create_task" : "http://127.0.0.1:8000/tasks/create",
    "update_task" : f"http://127.0.0.1:8000/tasks/{random_id}/status"
}"""





status_types = ['IN_PROGRESS','DONE']

def django_create_task_thread_function(**kwargs):
    for i in range(kwargs['loop_times']):
        print(f"USER: {kwargs['user_id']}")
        random_title = random.choice(titles)
        random_description = random.choice(descriptions)
        url = "http://127.0.0.1:8000/tasks/create"
        payload = f'title={random_title}&description={random_description}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))


def node_create_task_thread_function(**kwargs):
    for i in range(kwargs['loop_times']):
        print(f"USER: {kwargs['user_id']}")
        random_title = random.choice(titles)
        random_description = random.choice(descriptions)
        url = "http://127.0.0.1:3000/tasks/create"
        payload = f'title={random_title}&description={random_description}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))

def node_update_task_status_thread_function(**kwargs):
    for i in range(kwargs['loop_times']):
        print(f"USER: {kwargs['user_id']}")
        status_chosen = random.choice(status_types)
        random_id = random.randint(1,10000)
        url = f"http://127.0.0.1:3000/tasks/{random_id}/status"
        payload = f'status={status_chosen}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("PATCH", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))

def django_update_task_status_thread_function(**kwargs):
    for i in range(kwargs['loop_times']):
        print(f"USER: {kwargs['user_id']}")
        status_chosen = random.choice(status_types)
        random_id = random.randint(1,10000)
        url = f"http://127.0.0.1:8000/tasks/{random_id}/status"
        payload = f'status={status_chosen}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("PATCH", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))



# Global variables
queue_results = queue.Queue()
# start_time = 0

# def test_mock_service(): - omitted
# def loop_test(loop_wait=0, loop_times=sys.maxsize):  - omitted
    
if __name__ == '__main__':
    ### Test Settings ###
    concurrent_users = 10
    loop_times = 1000
    
    workers = []
    start_time = time.time()
    print('Tests started at %s.' % start_time )
    
    # start concurrent user threads
    for i in range(concurrent_users):
        thread = threading.Thread(target=node_create_task_thread_function, kwargs={'loop_times': loop_times, 'user_id' : i}, daemon=True)         
        thread.start()
        workers.append(thread)

    # Block until all threads finish.
    for w in workers:
        w.join()       
        
    end_time = time.time()
    print('\nTests ended at %s.' % end_time )
    print('Total test time: %s seconds.' %  (end_time - start_time) )










##### RESULTS #####

"""

Tasks Table Schema:

{
    id: number,
    title: string,
    description: string,
    status: string
}


10 Threads running parallely (concurrent)
1000 writes per thread.
total of 10,000 writes

task performed by the thread: creating task-management task of the type Tasks Schema shown above

Python3-Django3.0:
time taken for 10,000 write-requests (10,000 POSTs): 127 seconds (79 writes-requests/sec)
time taken for 10,000 update-requests (10,000 PATCHs): 126 seconds (79 writes-requests/sec)

NodeJs-NestJs:
time taken for 10,000 write-requests (10,000 writes): 30 seconds (333 writes-requests/sec)
time taken for 10,000 update-requests (10,000 PATCHs): 29 seconds (79 writes-requests/sec)
writes-requests/sec: 333

Conclusion: NodeJs is almost 4 times faster than Django.

(Things to remember: NodeJs is single threaded and doesn't support multi-threading. Django supports multi-threading
and hence django can be used for CPU intensive tasks and NodeJs can't be used for those. For simple web applications,
NodeJs can be preferred over django. For applications involving CPU intensive tasks that would involve machine-learining or
image processing (multi-threaded parallel processing), django would be a better choice.)

(And also, if the application has to do more with the programming language, then choose nodejs as javascript is 
faster than python. If the application just involves simple CRUD applications, choose django as most of the 
operations will be handled by database.)

"""


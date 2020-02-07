# NodeJs (ExpressJs) vs Django Python3
#### (Performance test)

This is a performance test of Django running and Nodejs to pick the right one in terms of performance.

* NodeJs is known for being quick as it is running on top of Google's V8 JIT-compiled JavaScript engine, originally written for Chrome.
* Also, NodeJs has the non-blocking asynchronous nature where it is not blocked during the IO operations.

Comparing it to Django which is a synchronous web framework (Even though Django 3.0 has the asynchronous option too), would be blocked during the IO operations and python generally being slow makes Django a little slower that NodeJs.

> If django is really slow, how does the app having the most number of users in world handle 500 million users and billions of requests everyday? (well, it's instagram)

To name a few, the other companies such as Pinterest, Disqus,Dropbox, Bitbucket, Spotify are also powered by Django too.

How do they manage it?
How can you increase the performance of Django? (if at least not more than nodeJs.... even though there is one way to increase the performance of django more than nodejs by using a highly optimized version of uWSGI web server or using Bjoern with a good reverse proxy server)

However there is one drawback of NodeJs which makes it not suitable for CPU intensive tasks because of it being single threaded and with django you can have multiple threads running CPU intensive tasks.
Make sure you don't run machine-learning or similar applications using NodeJs as it can make it a lot lot slower and ruuning machine-learning jobs on django gives a better gain on the performance.

People prefer NodeJs while building chatting apps as it has a good suppport of web socket communication and can handle as many as 600k concurrent connections. But, django has django-channels which is a redis implementation for having web sockets and is as good as NodeJs socket.io and scalable as well. Django-channels uses ASGI for performing this. (asynchronous server gateway interface from WSGI)

Django also has django-celery for performing asynchronous tasks in the background where it is mostly used for queing tasks which can be made to use either Redis or RabbitMQ.
___
### Let's talk about why we are here...
and also about the performance test between the two.

##### NodeJs configuration:

> * NodeJs using ExpressJs as it's web framework
> * Written using JavaScript (not TypeScript)
> * Postgres as the Database
> * KnexJs as the querybuilder (knex is not an ORM, it's just used to interact with the database)
> * PM2 as the process manager for managing the NodeJs server (with cluster mode as well as without it)
> * Nginx as the reverse proxy server

Docker Containers used: 
* Node pulled from - node:lts (12.15.0 LTS)
* Postgres pulled from -  postgres:latest
* Nginx pulled from - nginx:latest
(all are official stable docker images)

##### Django configuration:

> * Django 3.0 (python3) as the web framework
> * Uses DRF - Django Rest Framework 3.10.3
> * Written using Python3
> * Postgres as the Database
> * Django ORM as the ORM (the default ORM of django)
> * Gunicorn as the production web server (with and without workers, also Gevent)
> * Nginx as the reverse proxy server
> * Django running with DEBUG mode turned off

Docker Containers used: 
* Python pulled from - python:3.6
* Postgres pulled from -  postgres:latest
* Nginx pulled from - nginx:latest
(all are official stable docker images)

#### What was the test about?
> The test was about sending post requests to the server where it saves the data into the postgres database. 
There are no relational fields as this is just a plain performance testing to compare speeds.
The fields in the database are considered for the table named task: (name: string, description: string)

#### How was the test done?
Test was done by writing a python script that runs multiple threads to replicate the users consuming the APIs realtime.

**_python testing script used:_**

```python
if __name__ == '__main__':
    ### Test Settings ###
    concurrent_users = 10
    loop_times = 1000
    
    workers = []
    start_time = time.time()
    print('Tests started at %s.' % start_time )
    
    # start concurrent user threads
    for i in range(concurrent_users):
        thread = threading.Thread(target=node_or_django_call_api_function, kwargs={'loop_times': loop_times, 'user_id' : i}, daemon=True)         
        thread.start()
        workers.append(thread)

    # Block until all threads finish.
    for w in workers:
        w.join()       
        
    end_time = time.time()
    print('\nTests ended at %s.' % end_time )
    print('Total test time: %s seconds.' %  (end_time - start_time) )

```

From the above script used for testing, we can make out that ```concurrent_users``` are the number of threads (users) and 
```loop_times ``` is the number of times a thread is supposed to make a POST request to the server.
The ```node_or_django_call_api_function``` is the function that makes the API call based on the parameters passed to the function as ```kwargs```.

**_API caller function:_**
```python
def node_or_django_call_api_function(**kwargs):
    for i in range(kwargs['loop_times']):
        print(f"USER: {kwargs['user_id']}")
        random_title = random.choice(titles)
        random_description = random.choice(descriptions)
        url = "api_endpoint"
        payload = f'title={random_title}&description={random_description}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data = payload)

        print(response.text.encode('utf8'))
```

The ```random_title``` is picked from a dataset of titles and the same for ```random_description``` too.
The for loop executes based on the option passed in the kwargs option.

The testing is made for the apps running without workers (no cluster mode) as well as the apps running with workers (cluster mode)

**What are worker and why are they important?**
Without cluster mode, the app would be running only on one of the CPU cores and won't utilize all the cores efficiently and makes the other cores waste. To take advantage of the other cores of the CPU, we can run the apps on each core parallely.

**Difference between threaded mode and cluster mode:**
In threaded mode, a worker can have many threads and it is more suitable for tasks that are more of IO bounded  and not compute or CPU bouded.
When the task is IO bouded, it would be waiting for an IO response and hence be blocked where the other threads can complete it's task.
But can't be used for intensive tasks as all threads are always concurrent and not parallel. (check out the difference between concurrency and parallelism)

In cluster mode, the tasks run parallel where 2 or more tasks can be running parallely which would give a true performance gain


### Results (the most interesting part?)
Well, as you would have guessed, NodeJs performed a litter better than Django. (the highly optimized NodeJs vs highly optimized Django)

##### Round 1:
> NodeJs running on PM2 without the cluster mode. (with no extra workers)

Time taken for 10,000 write requests: **36 seconds**
Write requests per second: 227
(```pm2-runtime start app.js``` (docker web container))

> Django running on Gunicorn (with no extra workers)

Time taken for 10,000 write requests: **92 seconds**
Write requests per second: 108
(```gunicorn task_management.wsgi -b 0.0.0.0:8001``` (docker web container))

##### Round 2:
> NodeJs running on PM2 in the cluster mode. (with 2 workers)
(the tasks are meant to be running parallely)

Time taken for 10,000 write requests: **47 seconds**
(```pm2-runtime start app.js -i 2``` )

> Django running on Gunicorn (with 2 workers)

Time taken for 10,000 write requests: **65 seconds**
(```gunicorn task_management.wsgi -b 0.0.0.0:8001 --workers=2```)

##### Round 3:
> NodeJs running on PM2 in the cluster mode. (with 3 workers, auto configure workers)


Time taken for 10,000 write requests: **44 seconds**
(```pm2-runtime start app.js -i -1``` )
The "-1" in the above command specifies that it is auto configure where it selects the number of worker processes automatically based on the available CPU cores.
Since my laptop has 4 cores which is considered as 'N'.
The calculated value is : N-1 processes which is 4-1 = 3 workers

> Django running on Gunicorn (with 3 workers)

Time taken for 10,000 write requests: **58 seconds**
(```gunicorn task_management.wsgi -b 0.0.0.0:8001 --workers=3```)

###### Other Django options (suggested):
> Running on suggested number of gunicorn workers:
Calculation suggested: (2 * CPU) + 1
=> (2 * 4) + 1 = 9

Time taken for 10,000 write requests: **52 seconds**
(```gunicorn task_management.wsgi -b 0.0.0.0:8001 --workers=9```)

> With using gevent pseudo threads (1000 * 9)

Time taken for 10,000 write requests: **60 seconds**
(```gunicorn task_management.wsgi -b 0.0.0.0:8001 --worker-class=gevent --worker-connections=1000 --workers=9```)

> With using gevent pseudo threads (500 * 4)

Time taken for 10,000 write requests: **59 seconds**
(```gunicorn task_management.wsgi -b 0.0.0.0:8001 --worker-class=gevent --worker-connections=500--workers=4```)

> With using gevent pseudo threads (only gevent 1000)

Time taken for 10,000 write requests: **102 seconds**
(```gunicorn task_management.wsgi -b 0.0.0.0:8001 --worker-class=gevent --worker-connections=1000```)

###### So using the gevent pseudo thread didn't give any performance gain

**The best performance for NodeJs was when it was not using clustering option in Round-1: 36 seconds and the best option for Django was with Gunicorn (9 workers) in Round-2: 52 Seconds**




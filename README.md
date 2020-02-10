# NodeJs (ExpressJs) vs Django Python3
#### (Performance test)

This is a performance test of Django and Nodejs to pick the right one in terms of performance.

* NodeJs is known for being quick as it is running on top of Google's V8 JIT-compiled JavaScript engine, originally written for Chrome.
* Also, NodeJs has the non-blocking asynchronous nature where it is not blocked during the IO operations.

Comparing it to Django which is a synchronous web framework (Even though Django 3.0 has the asynchronous option too), would be blocked during the IO operations and python generally being slow makes Django a little slower that NodeJs.

> If django is really slow, how does the app having the most number of users in world handle 500 million users and billions of requests everyday? (well, it's instagram)

To name a few, the other companies - Pinterest, Disqus, Dropbox, Bitbucket, Spotify are also powered by Django too.

How do they manage it?
How can you increase the performance of Django? (if at least not more than nodeJs.... even though there is one way to increase the performance of django more than nodejs by using a highly optimized version of uWSGI web server or using Bjoern with a good reverse proxy server)

However there is one drawback of NodeJs which makes it not suitable for CPU intensive tasks because of it being single threaded and with django you can have multiple threads running CPU intensive tasks.
Make sure you don't run machine-learning or similar applications using NodeJs as it can make it a lot lot slower and running machine-learning jobs on django gives a better gain on the performance.

People prefer NodeJs while building chatting apps as it has a good support of web socket communication and can handle as many as 600k concurrent connections. But, django has django-channels which is a redis implementation for having web sockets and is as good as NodeJs socket.io and scalable as well. Django-channels uses ASGI for performing this. (asynchronous server gateway interface from WSGI)

Django also has django-celery for performing asynchronous tasks in the background where it is mostly used for queuing tasks which can be made to use either Redis or RabbitMQ.
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
The fields in the database that are considered for the table named task: (name: string, description: string)

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

The ```random_title``` is picked from a dataSet of titles and the same for ```random_description``` too.
The for loop executes based on the option passed in the kwargs option.

The testing is made for the apps running without workers (no cluster mode) as well as the apps running with workers (cluster mode)

**What are workers and why are they important?**
Without cluster mode, the app would be running only on one of the CPU cores and won't utilize all the cores efficiently and makes the other cores waste. To take advantage of the other cores of the CPU, we can run the apps on each core parallelly.

**Difference between threaded mode and cluster mode:**
In threaded mode, a worker can have many threads and it is more suitable for tasks that are more of IO bounded  and not compute or CPU bounded.
When the task is IO bounded, it would be waiting for an IO response and hence be blocked where the other threads can complete it's task.
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

> Django running on Gunicorn with **PyPy3** (not CPython3) (with no extra workers)

Time taken for 10,000 write requests: **104 seconds**


##### Round 2:
> NodeJs running on PM2 in the cluster mode. (with 2 workers)
(the tasks are meant to be running parallelly)

Time taken for 10,000 write requests: **47 seconds**
(```pm2-runtime start app.js -i 2``` )

> Django running on Gunicorn (with 2 workers)

Time taken for 10,000 write requests: **65 seconds**
(```gunicorn task_management.wsgi -b 0.0.0.0:8001 --workers=2```)

> Django running on Gunicorn with **PyPy3** (with 2 workers)

Time taken for 10,000 write requests: **58 seconds**

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

> Django running on Gunicorn with **PyPy3** (with 9 workers)

Time taken for 10,000 write requests: **62 seconds**


###### So using the gevent pseudo thread didn't give any performance gain

### 1 Million write - Requests Challenge:
> Django - 5580 seconds (93 mins)

```(with 9 workers based on optimal calculation)```

> Nodejs -  4347 seconds (73 mins)

```(with 3 workers based on optimal calculation)```


**The best performance for NodeJs was when it was not using clustering option in Round-1: 36 seconds and the best option for Django was with Gunicorn (9 workers) in Round-2: 52 Seconds**

Well, I guess you would have a question in your mind about why is NodeJs slower while using the clustering mode compared to the test where no workers were used...

**Reason:**
The kind of tasks that we were performing was IO bound and not CPU intensive task.
So what's the use of even using cluster mode when the program has to wait for the input/output operation to be completed? Even if we were using multiple cores, the worker has to again wait until the IO operation gets completed...So it just becomes an overhead and makes it even slower as the CPU has to take care of the PM2 and the scheduling which is not necessary. But, if the program grows larger in size, then clustering will be helpful as it always won't be IO bound and there would even be CPU intensive jobs.
Use clustering mode only if you know that there is significant amount of CPU jobs.\

**Testing CPU intensive jobs:**
> To test if the performance actually increases CPU intensive jobs after clustering, replace the DB call/action by an intensive for loop that just needs a lot of time to run and complete.

Replace the DB call with:

```javascript
var counter = 0;
    for(let i=0; i<10000; i++){
      for(let k=0; k<1000; k++){
        counter = counter + 500;
      }
    }
```

```python
counter = 0;
        for i in range(10000):
            for k in range(1000):
                counter = counter + 500;

```

The above indeed is a CPU intensive task which would use up the CPU.

> With no worker processes

```NodeJs``` - Time taken for 5000 writes: **120 seconds (2 mins)**
```Django-Python3``` - Time taken for 5000 writes: **2700 seconds (45 mins)
```Django-PyPy3``` - Time taken for 5000 writes: **86 seconds (1 min 26s)**



> With 3 worker processes:

```NodeJs``` - Time taken for 5000 writes: **60 seconds (1 min)**
```Django-Python3``` - Time taken for 5000 writes: **950 seconds (16 mins)**
```Django-PyPy3``` - Time taken for 5000 writes: **36 seconds**



> With 6 worker processes:

```NodeJs``` - Time taken for 5000 writes: **40 seconds**
```Django-Python3``` - Time taken for 5000 writes: **600 seconds**
```Django-PyPy3``` - Time taken for 5000 writes: **20 seconds**

###### Winner in all the above CPU intensive rounds: Django-PyPy3

##### Note of conclusion on CPU intensive tasks round:
In the CPU intensive task round, the DB part is completely removed as it was meant to purely test only the CPU tasks.
We were enthralled seeing the performance of PyPy3 over NodeJs and had never thought to perform better than NodeJs.

**BTW, what is PyPy?**

PyPy is an alternative implementation of the Python programming language to CPython. PyPy often runs faster than CPython because PyPy is a just-in-time compiler while CPython is an interpreter.

###### Conclusion on PyPy3:
PyPy is not completely tested by many companies in production yet (even though there are a few companies using it in production where there is a heavy task processing required)
Success story of a company using PyPy in production: [watch here](https://www.youtube.com/watch?v=1n9KMqssn54&t=1182s)
Also, not all the python libraries support PyPy as of now.
PyPy can often be used with Django-Celery where we would need a lot of CPU tasks being performed in backend. Using PyPy for such tasks would also reduce the server computation costs as it does the calculation much faster. But, don't use PyPy in the normal controller as it isn't needed if there isn't any heavy processing as it might just be an overhead making the process even slower. You can see an example above where PyPy is used when there was just a DB call and nothing else. It performed worse than normal Python3 as there was no CPU intensive task. You can run a Django-Celery docker container separately on PyPy and send tasks to this task processor for better performance.
___

**-- Adithya K V**

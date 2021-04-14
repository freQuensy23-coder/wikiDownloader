import threading
import math

tasks_per_thread = 10


def generate_threads(tasks: list, func):
    """Return list of non started threads
    :param tasks list of task - Arguments to be passed to the function func
    :param func func that will be fulfilled by thread
    :returns thread list (non started)
    """
    t_list = []  # List of created threads
    for i, task in enumerate(tasks):
        t = threading.Thread(target=func, name=f"thread {i}", args=(tasks[i], ))
        t_list.append(t)
    return t_list


def tasks_divider(tasks: list, tasks_per_thread=tasks_per_thread):
    groups_num = math.ceil(len(tasks) / tasks_per_thread)
    result = []
    for i in range(groups_num):
        result.append(tasks[i * tasks_per_thread: (i + 1) * tasks_per_thread])
    if result == []:
        result = [[]]
    return result


def patch_http_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems
    with "HttpConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size
    you want to give to the connection pool)
    """
    from urllib3 import connectionpool, poolmanager

    class MyHTTPConnectionPool(connectionpool.HTTPConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['http'] = MyHTTPConnectionPool


def patch_https_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems
    with "HttpSConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size
    you want to give to the connection pool)
    """
    from urllib3 import connectionpool, poolmanager

    class MyHTTPSConnectionPool(connectionpool.HTTPSConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPSConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['https'] = MyHTTPSConnectionPool
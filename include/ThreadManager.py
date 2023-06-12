class ThreadManager:
    """Class to manage threading, getting its results and tracking if it's been handled.
    V3
    """

    def __init__(self, semaphores=25):
        """
        Initialisation
        """
        self._semaphores = threading.Semaphore(semaphores)
        self._threads = collections.deque()

    def __del__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def append(self, func: callable, *args, **kwargs) -> None:
        """
        Create a new thread by appending it to the threads to be processed
        :param func: (func) Function
        :param args: (list) Arguments
        :param kwargs: (dict) Keywords
        :return: void
        """
        thread = self.ThreadFunction(target=func, args=args, kwargs=kwargs, semaphores=self._semaphores)
        thread.name = func.__name__

        # Queue the thread
        self._threads.append(thread)
        thread.start()

    def set_semaphore(self, semaphores: int) -> None:
        """
        Set the semaphore limit (max concurrent threads)
        :param semaphores:
        :return:
        """
        self._semaphores = threading.Semaphore(semaphores)

    def active_count(self, name=None) -> int:
        """
        Get remaining thread count
        :return: (int) Threads
        """
        return len([thread for thread in self._threads if thread.name == name or name is None])

    def inactive_count(self) -> int:
        """
        Get remaining inactive thread count, threads that are done and need values returned
        :return: (int) Threads
        """
        return len([thread for thread in self._threads if not thread.is_alive()])

    def get_threads(self) -> list:
        """
        Get all threads
        :return: (list) threading.Thread
        """
        return self._threads

    def abort(self) -> None:
        """
        Terminate all threads, send stop signal
        WARNING: This will not return the results of the threads
        WARNING: This can result in corrupted data
        :return: void
        """
        while len(self._threads) > 0:
            thread = self._threads.popleft()
            thread.stop()
            del thread

    def get_values(self, name=None) -> list:
        """
        Return a list of results of competed threads
        :return: (list) Return values
        """
        current_threads = collections.deque(self._threads)
        complete_thread = collections.deque()
        incomplete_threads = collections.deque()

        while len(current_threads) != 0:
            thread = current_threads.popleft()
            if thread.is_alive():
                incomplete_threads.append(thread)
            else:
                complete_thread.append(thread.value())

        self._threads = incomplete_threads

        return complete_thread

    def get_value(self) -> any:
        """
        Return the value of the first completed thread
        :return: (any) Return value
        """
        while True:
            thread = self._threads.popleft()
            if thread.is_alive():
                self._threads.append(thread)
            else:
                return thread.value()

    class ThreadFunction(threading.Thread):

        def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None, semaphores=None):
            """
            Initialisation
            """
            self._semaphores = semaphores
            if 'semaphores' in kwargs:
                del kwargs['semaphores']

            self.event = threading.Event()

            threading.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

            self._return = None

        def __del__(self):
            self._semaphores.release()

        def run(self) -> threading.Thread:
            """
            Override the run to get the return value
            :return:
            """
            self._semaphores.acquire()
            self._return = self._target(*self._args, **self._kwargs)
            return self

        def stop(self) -> None:
            """
            Stop thread
            :return: None
            """
            if self._tstate_lock is not None:
                self._tstate_lock.release()
            self._stop()

        def value(self) -> any:
            """
            Get the results of the function
            :return:
            """
            threading.Thread.join(self)
            self._semaphores.release()
            return self._return

import sys
from threading import Thread, Event


# Created by Ahmed Cemil Bilgin


class ThreadManager:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.func_pool = {}
        self.stop_events = {}
        self.thread_pool = {}
        self.event_status = False

    def thread_func(
        self,
        func,
        stop_event,
    ):
        while not stop_event.is_set():
            func()
            # Wait for the stop event to be set before exiting the thread function
            sys.stdout.write("\r")
            # stop_event.wait(0)

    def add_thread(self, thread_name, func):
        if thread_name not in self.func_pool:
            self.func_pool[thread_name] = func
        self.stop_events[thread_name] = Event()
        self.thread_pool[thread_name] = Thread(
            target=self.thread_func,
            args=(self.func_pool[thread_name], self.stop_events[thread_name]),
        )

    def add_thread_one_time_run(self, func):
        Thread(target=func).start()

    def remove_thread(self, thread_name):
        if thread_name in self.thread_pool:
            self.thread_pool.remove(thread_name)
            self.stop_events.remove(thread_name)

    def run_all_threads(self):
        for thread_name, thread in self.thread_pool.items():
            self.thread_pool[thread_name].start()
        self.event_status = True

    def start_thread(self, thread_name):
        # if thread is in thread_pool and thread is already running, do nothing
        if thread_name in self.thread_pool and self.thread_pool[thread_name].is_alive():
            return False
        elif not self.stop_events[thread_name].is_set():
            self.thread_pool[thread_name].start()
            return True
        elif self.stop_events[thread_name].is_set():
            self.stop_events[thread_name].clear()
            self.add_thread(thread_name=thread_name, func=self.func_pool[thread_name])
            self.thread_pool[thread_name].start()
            return True
        else:
            print(f"{thread_name} is still running.")
            return False

    def stop_all_threads(self):
        for thread_name in self.stop_events:
            if not self.stop_events[thread_name].is_set():
                self.stop_events[thread_name].set()
                if thread_name in self.thread_pool:
                    self.thread_pool.pop(thread_name)
                self.event_status = False
        return True

    def stop_thread(self, thread_name):
        if thread_name in self.stop_events:
            self.stop_events[thread_name].set()
            if thread_name in self.thread_pool:
                self.thread_pool.pop(thread_name)
            return True
        else:
            return False

    def get_status(self, thread_name=None):
        if thread_name is None:
            thread_status = {}
            for thread_name, thread in self.thread_pool.items():
                thread_status[thread_name] = thread.is_alive()
            return thread_status
        elif thread_name in self.thread_pool:
            return self.thread_pool[thread_name].is_alive()
        else:
            return False

    def get_threads(self):
        return self.thread_pool.values()

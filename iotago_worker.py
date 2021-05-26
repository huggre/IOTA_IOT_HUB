import atexit
from worker_app import worker_app

def close_running_threads():
    print("Threads complete, ready to finish")
#Register the function to be called on exit
atexit.register(close_running_threads)

if __name__ == "__main__":
    worker_app.run(host='0.0.0.0', port=5001)
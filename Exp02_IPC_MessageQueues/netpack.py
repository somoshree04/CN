
import sys
import os

if sys.platform.startswith('linux'):
    import importlib.util
    so_path = os.path.join(os.path.dirname(__file__), 'netpack.so')
    if os.path.exists(so_path):
        spec = importlib.util.spec_from_file_location("netpack", so_path)
        netpack_so = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(netpack_so)
        globals().update(vars(netpack_so)) # Expose functions directly
else:
    # Windows Fallback: Rebuild the exact structures found in netpack.so
    import multiprocessing

    def create_queue():
        return multiprocessing.Queue()

    def write_queue(queue_obj, data):
        queue_obj.put(data)
        return queue_obj

    def read_queue(queue_obj):
        try:
            return queue_obj.get(block=False) # Non-blocking extraction
        except Exception:
            return None

    def create_process(target_function, args_list):
        return multiprocessing.Process(target=target_function, args=tuple(args_list))

    def start_process(process_obj):
        process_obj.start()

    def join_process(process_obj):
        process_obj.join()

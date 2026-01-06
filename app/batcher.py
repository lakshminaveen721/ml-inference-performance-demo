import time
import threading
import queue
import torch

class BatchItem:
    def __init__(self, tensor):
        self.tensor = tensor
        self.result = None
        self.event = threading.Event()


class DynamicBatcher:
    def __init__(self, model_service, max_batch_size=8, max_wait_ms=5):
        self.model_service = model_service
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms / 1000.0

        self.queue = queue.Queue()
        self.worker = threading.Thread(target=self._batch_loop, daemon=True)
        self.worker.start()

    def submit(self, tensor):
        item = BatchItem(tensor)
        self.queue.put(item)
        item.event.wait()
        return item.result

    def _batch_loop(self):
        while True:
            batch = []
            start_time = time.time()

            while len(batch) < self.max_batch_size:
                timeout = self.max_wait_ms - (time.time() - start_time)
                if timeout <= 0:
                    break
                try:
                    item = self.queue.get(timeout=timeout)
                    batch.append(item)
                except queue.Empty:
                    break

            if not batch:
                continue

            tensors = torch.cat([item.tensor for item in batch], dim=0)

            with torch.no_grad():
                outputs = self.model_service.predict_batch(tensors)

            for item, output in zip(batch, outputs):
                item.result = output
                item.event.set()

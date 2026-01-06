import os
import threading
import torch
import torchvision.models as models


class ModelService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.precision = os.getenv("INFERENCE_PRECISION", "fp32").lower()
        self.model = None
        self.ready = False

        # Load model in background
        thread = threading.Thread(target=self._load_model, daemon=True)
        thread.start()

    def _load_model(self):
        ci_mode = os.getenv("CI", "false") == "true"

        self.model = models.resnet50(pretrained=not ci_mode)
        self.model.eval()
        self.model.to(self.device)

        if self.device == "cuda" and self.precision == "fp16":
            self.model = self.model.half()

        self.ready = True

    @torch.no_grad()
    def predict_batch(self, input_tensor: torch.Tensor):
        if not self.ready:
            raise RuntimeError("Model not ready")

        input_tensor = input_tensor.to(self.device)
        if self.device == "cuda" and self.precision == "fp16":
            input_tensor = input_tensor.half()

        outputs = self.model(input_tensor)
        return outputs.argmax(dim=1).cpu().tolist()

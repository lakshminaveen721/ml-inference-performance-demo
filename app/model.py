import os
import torch
import torchvision.models as models


class ModelService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.precision = os.getenv("INFERENCE_PRECISION", "fp16").lower()
        assert self.precision in ("fp16", "fp32")

        # 🔑 CI MODE: avoid downloading weights
        ci_mode = os.getenv("CI", "false") == "true"

        self.model = models.resnet50(pretrained=not ci_mode)
        self.model.eval()
        self.model.to(self.device)

        if self.device == "cuda" and self.precision == "fp16":
            self.model = self.model.half()

    @torch.no_grad()
    def predict_batch(self, input_tensor: torch.Tensor):
        input_tensor = input_tensor.to(self.device)
        if self.device == "cuda" and self.precision == "fp16":
            input_tensor = input_tensor.half()

        outputs = self.model(input_tensor)
        return outputs.argmax(dim=1).cpu().tolist()


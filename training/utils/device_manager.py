import torch


class DeviceManager:

    def __init__(self, prefer_gpu: bool = True):
        self.prefer_gpu = prefer_gpu
        self._cuda_available = torch.cuda.is_available()

    def get_device(self) -> str:
        """
        Decide automaticamente o device ideal.
        """
        if self.prefer_gpu and self._cuda_available:
            if self._enough_gpu_memory():
                return "cuda"

        return "cpu"

    def info(self) -> dict:
        return {
            "cuda_available": self._cuda_available,
            "device": self.get_device(),
            "gpu_name": self._gpu_name(),
            "gpu_memory_total_gb": self._gpu_memory_total(),
            "gpu_memory_free_gb": self._gpu_memory_free(),
            "cpu_threads": torch.get_num_threads(),
        }

    def suggest_batch_size(self, base: int = 64) -> int:

        if not self._cuda_available:
            return max(32, base // 2)

        free_mem = self._gpu_memory_free()

        if free_mem > 8:
            return base * 4
        elif free_mem > 4:
            return base * 2
        elif free_mem > 2:
            return base

        return max(32, base // 2)

    def suggest_buffer_size(self, base: int = 100000) -> int:

        if not self._cuda_available:
            return int(base * 0.5)

        free_mem = self._gpu_memory_free()

        if free_mem > 8:
            return base * 2

        return base

    def _enough_gpu_memory(self, min_gb: float = 2.0) -> bool:
        if not self._cuda_available:
            return False
        return self._gpu_memory_free() >= min_gb

    def _gpu_memory_free(self) -> float:
        if not self._cuda_available:
            return 0.0

        free, _ = torch.cuda.mem_get_info()
        return free / 1024**3  # GB

    def _gpu_memory_total(self) -> float:
        if not self._cuda_available:
            return 0.0

        props = torch.cuda.get_device_properties(0)
        return props.total_memory / 1024**3

    def _gpu_name(self) -> str | None:
        if not self._cuda_available:
            return None
        return torch.cuda.get_device_name(0)

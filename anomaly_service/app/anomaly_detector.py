import torch
import torch.nn as nn
from typing import Dict, List
import numpy as np

class MetricAutoencoder(nn.Module):
    def __init__(self, input_size: int, hidden_size: int = 16):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size // 2)
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden_size // 2, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, input_size)
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

def detect_anomalies(metrics: Dict[str, float], metric_list: List[str], model: nn.Module, threshold: float = 0.05):
    values = [metrics.get(m, 0.0) for m in metric_list]  # pad missing metrics
    x = torch.tensor(values, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        x_hat = model(x)
    errors = torch.abs(x - x_hat).squeeze(0).numpy()
    anomalies = {metric_list[i]: bool(errors[i] > threshold) for i in range(len(metric_list))}
    scores = {metric_list[i]: float(errors[i]) for i in range(len(metric_list))}
    return anomalies, scores

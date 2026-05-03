# GPU Cloud Benchmark

An open-source tool for benchmarking GPU performance across different cloud providers and instance types.

## Features

- **Multi-cloud support**: Lambda Labs, Modal, RunPod, AWS, GCP, Azure
- **Comprehensive testing**: Training, inference, and latency benchmarks
- **Automated reporting**: JSON, CSV, and interactive HTML reports
- **Cost analysis**: $/TFLOP and $/hour comparisons
- **Extensible**: Easy to add new providers and tests

## Quick Start

```bash
# Clone repository
git clone https://github.com/RoTo-id/gpu-cloud-benchmark.git
cd gpu-cloud-benchmark

# Install dependencies
pip install -r requirements.txt

# Run basic benchmark
python benchmark.py --config configs/quick_test.json
```

## Supported Providers

| Provider | Instance Types | Status |
|----------|----------------|---------|
| Lambda Labs | GPU instances | ✅ Full |
| Modal | Serverless GPU | ✅ Full |
| RunPod | GPU pods | ✅ Full |
| AWS EC2 | p3, p4, g4dn, g5 | ✅ Full |
| Google Cloud | a2, a3, g2 | ✅ Full |
| Azure | NC, ND, NV | ⚠️ Beta |

## Benchmark Types

- **Training**: PyTorch, TensorFlow, JAX
- **Inference**: Latency, throughput, batch processing
- **Memory**: VRAM utilization, memory bandwidth
- **Cost**: Hourly rates, $/TFLOP analysis
- **Reliability**: Uptime, spot instance interruptions

## Configuration

Create custom benchmark configurations in `configs/`. See `configs/example.json` for all options.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
# GPU benchmark prototype

## Actual implementation status

This repository contains an unfinished orchestrator sketch, not a working
multi-cloud benchmark. `benchmark.py` imports `cloud_providers`, `benchmarks`
and `reporting`, which are absent. The referenced `configs/` and report
implementations are absent too. There are no committed measurements proving
provider performance, reliability, training throughput or cost efficiency.

The previous provider support table and quick-start commands were inaccurate.
Installing `requirements.txt` does not supply the missing implementations.
That broad dependency list is retained as historical prototype context; do
not install the ML frameworks and cloud SDKs expecting a runnable tool.

## Proposed smaller role

Use this as a workload benchmark specification and evidence component before
considering an independent product or cloud provisioning service.

A useful comparison should describe the actual workload, model and version,
hardware and VRAM headroom, quality threshold, measured latency/throughput,
sample size, measurement date, and recurring cost assumptions. Compare local
hardware with cloud options only when both have suitable evidence. Report
missing measurements as unknown; do not infer model quality from GPU speed.

Keep measurement collection separate from comparison and execution. Reuse an
existing result contract/comparator where available. Synthetic examples,
declared capabilities and manually entered prices do not establish execution
or current provider pricing. No automatic resource purchase is implemented
or authorized by this repository.

## Next useful evidence

1. Select one real workload and an existing measurement runner.
2. Record a repeatable local baseline with quality and resource measurements.
3. Compare an independently measured alternative for the same workload.
4. Test whether the comparison changes a useful compute decision.

Broader connectors and a commercial interface should follow demonstrated
demand. Preserve the prototype history; there is no reason to construct six
provider integrations before that validation.

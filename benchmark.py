#!/usr/bin/env python3
"""
GPU Cloud Benchmark - Main benchmarking orchestrator

Automated GPU performance testing across cloud providers.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import click
import pandas as pd
from omegaconf import OmegaConf

from cloud_providers import CloudManager
from benchmarks import BenchmarkRunner
from reporting import ReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GPUCloudBenchmark:
    """Main benchmark orchestrator."""
    
    def __init__(self, config_path: str):
        """
        Initialize benchmark with configuration.
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config = OmegaConf.load(config_path)
        self.cloud_manager = CloudManager(self.config.cloud)
        self.benchmark_runner = BenchmarkRunner(self.config.benchmarks)
        self.report_generator = ReportGenerator()
    
    async def run_benchmark(self, provider_name: str) -> Dict[str, Any]:
        """
        Run benchmark for a specific cloud provider.
        
        Args:
            provider_name: Name of cloud provider
        
        Returns:
            Dictionary with benchmark results
        """
        logger.info(f"Starting benchmark for {provider_name}")
        
        # Provision instance
        instance = await self.cloud_manager.start_instance(provider_name)
        
        try:
            # Run benchmarks
            results = await self.benchmark_runner.run_all(
                instance, 
                self.config.benchmarks.tests
            )
            
            # Add metadata
            results.update({
                "provider": provider_name,
                "instance_type": instance.instance_type,
                "timestamp": datetime.utcnow().isoformat(),
                "cost_per_hour": instance.cost_per_hour,
                "region": instance.region
            })
            
            return results
        
        finally:
            # Cleanup instance
            await self.cloud_manager.stop_instance(provider_name, instance.id)
    
    async def run_all(self) -> List[Dict[str, Any]]:
        """
        Run benchmarks for all configured providers.
        
        Returns:
            List of benchmark results for all providers
        """
        all_results = []
        
        for provider in self.config.cloud.providers:
            try:
                result = await self.run_benchmark(provider)
                all_results.append(result)
            except Exception as e:
                logger.error(f"Failed to run {provider}: {e}")
                all_results.append({
                    "provider": provider,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return all_results
    
    def save_results(self, results: List[Dict[str, Any]], output_dir: str):
        """Save benchmark results to output directory."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save raw JSON
        with open(output_path / "results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        # Save tabular data
        df = pd.DataFrame(results)
        df.to_csv(output_path / "results.csv", index=False)
        
        # Generate detailed reports
        self.report_generator.create_report(results, output_path)


@click.command()
@click.option("--config", "-c", required=True, 
              help="Configuration file path")
@click.option("--output", "-o", default="./benchmark_results",
              help="Output directory for results")
@click.option("--providers", multiple=True,
              help="Specific providers to benchmark (default: all)")
def main(config: str, output: str, providers: tuple):
    """Run GPU cloud benchmarks."""
    
    benchmark = GPUCloudBenchmark(config)
    
    async def run():
        # Filter providers if specified
        if providers:
            benchmark.config.cloud.providers = list(providers)
        
        results = await benchmark.run_all()
        benchmark.save_results(results, output)
        
        print(f"Benchmark complete! Results saved to {output}/")
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
from ttsds import BenchmarkSuite
from ttsds.util.dataset import DirectoryDataset

# Initialize datasets
datasets = [
    DirectoryDataset("./benchmark_data/generated", name="generated")
]
reference_datasets = [
    DirectoryDataset("./benchmark_data/raw", name="reference")
]

# Create benchmark suite
suite = BenchmarkSuite(
    datasets=datasets,
    reference_datasets=reference_datasets,
    write_to_file="benchmark_results.csv",  # Optional: save results to CSV
    skip_errors=True,  # Optional: skip failed benchmarks
    include_environment=False,  # Optional: exclude environment benchmarks
)

# Run benchmarks
results = suite.run()

# Get aggregated results with weighted scores
aggregated = suite.get_aggregated_results()
print(aggregated)

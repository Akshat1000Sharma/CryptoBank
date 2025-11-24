# Performance Testing Guide: Concurrent vs Sequential Execution

This guide explains how to test and compare the performance of concurrent (parallel) vs sequential (non-concurrent) batch transaction execution.

## Overview

The system provides two methods for executing batch transactions:

1. **Concurrent Execution** - Transactions are executed in parallel using ThreadPoolExecutor
2. **Sequential Execution** - Transactions are executed one after another

## Methods to Run Performance Tests

### Method 1: API Endpoint (Recommended)

**Endpoint:** `GET /api/performance/comparison?num_transactions=5`

**Usage:**

1. **Start your backend server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Make a request:**
   ```bash
   # Using curl
   curl http://localhost:8000/api/performance/comparison?num_transactions=5
   
   # Or open in browser
   http://localhost:8000/api/performance/comparison?num_transactions=5
   ```

3. **Response includes:**
   - Execution time for both methods
   - Success rates
   - Speedup factor
   - Improvement percentage
   - Detailed metrics

### Method 2: Standalone Python Script

**File:** `backend/performance_test_script.py`

**Usage:**

```bash
cd backend
python performance_test_script.py
```

**With options:**
```bash
# Custom number of transactions
python performance_test_script.py --num-tx 10

# Output as JSON
python performance_test_script.py --json

# Save to file
python performance_test_script.py --output results.json
```

### Method 3: Python Script (Direct Import)

```python
import asyncio
from service import performance_comparison_test

async def test():
    results = await performance_comparison_test(num_transactions=5)
    print(results)

asyncio.run(test())
```

## Response Format

The API returns a JSON object with the following structure:

```json
{
  "concurrent_execution": {
    "execution_time_seconds": 0.5234,
    "successful_count": 5,
    "failed_count": 0,
    "total_count": 5,
    "success_rate": 100.0,
    "average_time_per_tx": 0.1047,
    "tx_hashes": ["0x...", "0x...", ...]
  },
  "sequential_execution": {
    "execution_time_seconds": 1.2345,
    "successful_count": 5,
    "failed_count": 0,
    "total_count": 5,
    "success_rate": 100.0,
    "average_time_per_tx": 0.2469,
    "tx_hashes": ["0x...", "0x...", ...]
  },
  "improvement_percentage": 57.6,
  "speedup_factor": 2.36,
  "test_configuration": {
    "num_transactions": 5,
    "amount_per_transaction": 0.1,
    "test_type": "batch_transfer_comparison"
  }
}
```

## Metrics Explained

### Execution Time
- **Total time** taken to execute all transactions
- Measured in seconds with microsecond precision

### Success Rate
- Percentage of transactions that completed successfully
- Formula: `(successful_count / total_count) * 100`

### Average Time per Transaction
- Average time for a single transaction
- Formula: `execution_time / total_count`

### Speedup Factor
- How many times faster concurrent execution is
- Formula: `sequential_time / concurrent_time`
- Example: 2.36x means concurrent is 2.36 times faster

### Improvement Percentage
- Percentage improvement in execution time
- Formula: `((sequential_time - concurrent_time) / sequential_time) * 100`

## Example Results Table

Here's an example of how to format results for your report:

| Metric | Concurrent | Sequential | Improvement |
|--------|-----------|------------|-------------|
| **Execution Time** | 0.5234s | 1.2345s | 57.6% faster |
| **Success Rate** | 100% | 100% | Same |
| **Avg Time/TX** | 0.1047s | 0.2469s | 57.6% faster |
| **Speedup Factor** | - | - | **2.36x** |

## Observations for Report

### Expected Observations:

1. **Concurrent execution is faster**
   - Multiple transactions execute simultaneously
   - Better utilization of network and processing resources
   - Speedup typically ranges from 1.5x to 3x depending on network conditions

2. **Success rates are similar**
   - Both methods should achieve similar success rates
   - Failures are usually due to network issues, not execution method

3. **Time savings increase with more transactions**
   - More transactions = greater time savings
   - Parallel execution scales better

4. **Resource utilization**
   - Concurrent: Higher CPU/network utilization
   - Sequential: Lower resource usage, but slower

### Sample Observations Text:

> "The performance comparison reveals that concurrent batch execution significantly outperforms sequential execution. With 5 transactions, concurrent execution completed in 0.52 seconds compared to 1.23 seconds for sequential execution, representing a 2.36x speedup and 57.6% time reduction. Both methods achieved 100% success rates, indicating that the performance improvement comes without sacrificing reliability. The average time per transaction decreased from 0.25 seconds (sequential) to 0.10 seconds (concurrent), demonstrating the efficiency gains of parallel processing."

## Troubleshooting

### Error: "Failed to connect to RPC"
- **Fix:** Make sure Hardhat node is running: `npx hardhat node`

### Error: "Insufficient balance"
- **Fix:** Make sure your account has enough tokens for testing

### Slow execution times
- **Normal:** First run may be slower due to contract compilation
- Network latency can affect results
- Run multiple tests and average the results

### Inconsistent results
- **Normal:** Network conditions vary
- Run the test multiple times and average
- Consider running during low network traffic

## Best Practices for Report

1. **Run multiple tests** (3-5 runs) and average the results
2. **Test with different transaction counts** (3, 5, 10)
3. **Document the test environment** (Hardhat local node, network conditions)
4. **Include error rates** if any transactions fail
5. **Note any anomalies** or unexpected results

## Quick Test Command

```bash
# Run test and save results
cd backend
python performance_test_script.py --num-tx 5 --output ../report_data.json
```

This will:
- Run the performance test
- Display formatted results
- Save detailed JSON to `report_data.json` for your report


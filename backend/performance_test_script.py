#!/usr/bin/env python3
"""
Standalone Performance Test Script
===================================

This script can be run independently to test and compare:
- Concurrent (parallel) batch transaction execution
- Sequential (non-concurrent) batch transaction execution

Usage:
    python performance_test_script.py

Or with custom number of transactions:
    python performance_test_script.py --num-tx 10
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent))

from service import performance_comparison_test
import json

def format_output(data: dict):
    """Format the performance comparison data for readable output"""
    concurrent = data["concurrent_execution"]
    sequential = data["sequential_execution"]
    
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON RESULTS")
    print("="*80)
    
    print("\n📊 TEST CONFIGURATION")
    print("-" * 80)
    config = data["test_configuration"]
    print(f"  Number of Transactions: {config['num_transactions']}")
    print(f"  Amount per Transaction: {config['amount_per_transaction']} tokens")
    print(f"  Test Type: {config['test_type']}")
    
    print("\n⚡ CONCURRENT (PARALLEL) EXECUTION")
    print("-" * 80)
    print(f"  Execution Time:        {concurrent['execution_time_seconds']:.4f} seconds")
    print(f"  Successful:            {concurrent['successful_count']}/{concurrent['total_count']}")
    print(f"  Failed:                {concurrent['failed_count']}")
    print(f"  Success Rate:         {concurrent['success_rate']:.2f}%")
    print(f"  Average Time per TX:    {concurrent['average_time_per_tx']:.4f} seconds")
    
    print("\n🔄 SEQUENTIAL (NON-CONCURRENT) EXECUTION")
    print("-" * 80)
    print(f"  Execution Time:        {sequential['execution_time_seconds']:.4f} seconds")
    print(f"  Successful:            {sequential['successful_count']}/{sequential['total_count']}")
    print(f"  Failed:                {sequential['failed_count']}")
    print(f"  Success Rate:         {sequential['success_rate']:.2f}%")
    print(f"  Average Time per TX:    {sequential['average_time_per_tx']:.4f} seconds")
    
    print("\n📈 PERFORMANCE IMPROVEMENT")
    print("-" * 80)
    print(f"  Speedup Factor:        {data['speedup_factor']:.2f}x")
    print(f"  Improvement:           {data['improvement_percentage']:.2f}% faster")
    
    time_saved = sequential['execution_time_seconds'] - concurrent['execution_time_seconds']
    print(f"  Time Saved:            {time_saved:.4f} seconds")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    if data['speedup_factor'] > 1:
        print(f"✅ Concurrent execution is {data['speedup_factor']:.2f}x faster!")
        print(f"   Sequential took {sequential['execution_time_seconds']:.4f}s")
        print(f"   Concurrent took  {concurrent['execution_time_seconds']:.4f}s")
    else:
        print("⚠️  Sequential execution was faster (unusual, may indicate overhead)")
    
    print("\n" + "="*80)

async def main():
    """Main function to run performance test"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Performance comparison test')
    parser.add_argument('--num-tx', type=int, default=5, 
                       help='Number of test transactions (default: 5, max: 10)')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    parser.add_argument('--output', type=str,
                       help='Save JSON output to file')
    
    args = parser.parse_args()
    
    num_tx = min(max(args.num_tx, 1), 10)
    
    print(f"\n🚀 Starting performance test with {num_tx} transactions...")
    print("   This may take a moment...\n")
    
    try:
        results = await performance_comparison_test(num_tx)
        
        if args.json:
            output = json.dumps(results, indent=2)
            print(output)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                print(f"\n✅ Results saved to {args.output}")
        else:
            format_output(results)
            
            # Also save JSON for later use
            json_file = f"performance_results_{num_tx}tx.json"
            with open(json_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Detailed results saved to: {json_file}")
            
    except Exception as e:
        print(f"\n❌ Error running performance test: {str(e)}")
        print("\nMake sure:")
        print("  1. Hardhat node is running (npx hardhat node)")
        print("  2. Backend .env is configured correctly")
        print("  3. You have enough tokens in your account")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())


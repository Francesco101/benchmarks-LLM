# benchmarks-LLM
A collection of benchmarks of LLM models implemented with LM EVALUATION HARNESS 

Usage:
    (00) -> create a benchmark. This is made in two steps:
            00 => create a task-settings file (it indicates task settings for each task)
            01 => create a benchmark file (it indicates models and files)
    
    (01) -> run the benchmark. For example, running from this branch:
            .../01-running-benchmarks % >> python3.11 run_benchmark.py ../benchmarks/round-999-bench.json ../outputs/round-999-outp/ round-999-results

    (02) -> results extraction and analysis. 

import benchmarks_helper as bench   # Import the helper file
import sys
import json

# usage: >> python run_benchmark benchmark-info.json "OUTPUT_PATH here" "results-filename (optional)"
# example: 
# .../01-running-benchmarks % >> python3.11 run_benchmark.py ../benchmarks/round-999-bench.json ../outputs/round-999-outp/ round-999-results

# get benchmark instruction 
benchmark_file = sys.argv[1]
OUTPUT_PATH = sys.argv[2]

if len(sys.argv) > 3:
    RESULTS_FILENAME = sys.argv[3]
else:
    RESULTS_FILENAME = "results"

# TODO: For now i always log full outputs, this is to be changed
#       It should be done only for tasks that have (log_samples = True)
FULL_OUTPUT = True

# TODO: Ensure bench-file and relative task-settings-file-path (contiained in bench-file) exist in the path indicated.
#       Ensure that all the tasks in bench-file exist in its task settings-file (to avoid typos in task-ids for example)


print(f"OUTPUT PATH : {OUTPUT_PATH}")
print(f"RESULTS_FILENAME : {RESULTS_FILENAME}")
if FULL_OUTPUT:
    print("FULL_OUTPUTS WILL BE STORED")

# Get the directions for the benchmark
with open(benchmark_file, "r") as f:
    benchmark_info = json.load(f)

'''
The benchmark file is a .json structured as this example, 
    the task-settings list maps task-parameters stored in tasks_settings_file to the corresponding tasks.
            { 
             "tasks_settings_file": "./benchmark-info.json"
             "model_0": {
                 "tasks": ["task_A, task_B"],
                 "task-settings": ["config_key_forA", "config_key_forB"] # to talk to TASK_SETTINGS_FILE
                 }
             "model_1": {
                ... same as for model 1
             }
                    
'''

# Execution of the benchmarks
resultsAll = dict()

models = list(benchmark_info.keys())
models.remove("tasks_settings_file")    # Here we need a list of models only
for model in models:
    resultsAll[model] = {}  
    # iterate over all tasks and run the benchmark
    for j, task in enumerate(benchmark_info[model]["tasks"]):
        # get and set benchmark_parameters
        settings_id = benchmark_info[model]["task-settings"][j]
        TASK_SETTINGS_FILE = benchmark_info["tasks_settings_file"]
        with open(TASK_SETTINGS_FILE, "r", encoding="utf-8") as f:
            try:
                task_params = json.load(f)[settings_id]
            except:
                resp = None
                # skip the task and report the error
                error_msg = f"The settings_id: {settings_id} is not present in {TASK_SETTINGS_FILE}"
                print(error_msg)
                resultsAll[model][task] = {
                        "executed": False,
                        "error": {
                            "kind": "settings_id not found",
                            "settings_is": settings_id,
                            "TASK_SETTINGS_FILE": TASK_SETTINGS_FILE
                            }
                        }
                continue
        
        # force model, necessary for general non-model specific settings:
        task_params["model_args"]["model"] = model
        # set tasks, necessary if non-task specific settings:
        task_params["tasks"] = [task]

        # populate resultsAll file, containing the outp["results"] and execution status (True | False)
        try:
            # run benchmark
            resp = bench.run_benchmark(task_params)
            # add results and execution status
            resultsAll[model][task] = resp["results"]
            resultsAll[model][task]["executed"] = True
        except:
            # Report error
            resp = None
            resultsAll[model][task] = {
                    "executed": False,
                    "error": {
                        "kind": "run_benchmark failed",
                        }
                    }

        if FULL_OUTPUT and resp is not None:
            # Save the whole output, which contains all questions and answers if --log_samples is True
            pth = OUTPUT_PATH + "full_outputs/" + model
            fn = task
            bench.dump_json(resp, output_path=pth, filename=fn, add_date=False)

# Save the results of the benchmarks
bench.dump_json(resultsAll, output_path=OUTPUT_PATH, filename=RESULTS_FILENAME, add_date=True)




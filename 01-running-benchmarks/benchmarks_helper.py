import os
import json
import datetime

# Disabling tokenizers parallelism ( before importing lm_eval )
# TODO it breaks some benchmarks if not disabled, WHY? TODO
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import lm_eval

def run_benchmark(parameters: dict):

    if parameters["model_args"]["model"] is None:
         raise InterruptedError("LLM-model not specified")

    # bemchmark
    output = lm_eval.simple_evaluate(
        model=parameters["model"],
        model_args=parameters["model_args"],
        gen_kwargs=parameters["gen_kwargs"],
        apply_chat_template=parameters["apply_chat_template"],
        tasks=parameters["tasks"],
        limit=parameters["limit"],
        log_samples=parameters["log_samples"],
    )
    return output

def dump_json(file_content, output_path="./benchmark_outputs", filename="unspec_name", add_date=True):
    # creates output's directory
    os.makedirs(output_path, exist_ok=True)

    # add datetime to filename
    if add_date is True:
        t = datetime.datetime.now()
        date = "%d-%d-%dT%d-%d-%d" % (t.year, t.month, t.day, t.hour, t.minute, t.second) 
        filename = filename + "__" + date
    filename = filename + ".json"

    with open(os.path.join(output_path, filename), "w", encoding="utf-8") as f:
        json.dump(file_content, f, indent=2, ensure_ascii=False, default=str)

    return 0


"""
Run a tranined model to generate Python code.
"""

import io
import json
import logging
import math
import random
import numpy as np
import os
import pprint
import sys
import time
import transformers
import torch
import openai

from reindent import run as run_reindent

# for timing and debugging
from datetime import datetime, date
from tqdm import tqdm

def setup():

    with open('accounts_info.json') as f:
        info = json.load(f)
    openai.api_key = info["openai_key"]

def reindent_code(codestr):
    """
    Given code string, reindent it in the same way that the
    Github dataset was indented
    """
    codestr = io.StringIO(codestr)
    ret = io.StringIO()

    run_reindent(
        codestr, 
        ret, 
        config = {
            "dry-run": False,
            "help": False,
            "to": 10,
            "from": -1,
            "tabs": True,
            "encoding": "utf-8",
            "is-tabs": False,
            "tabsize": 10,
            "all-tabs": False
        }
    )

    return ret.getvalue()

def generate_prompt(args, test_case_path, prompt_path, hint_path, solutions_path=None, starter_path=None):
    problem_text = "\nThis is the question prompt:\n"
    with open(prompt_path, "r") as f:
        data = f.readlines()
        data = "".join(data)
    problem_text += data

    hints = ""
    with open(hint_path, "r") as f:
        data = json.load(f)
        print(type(data))
        tags = ",".join(data.get("tags"))
        if tags:
            hints = "\nHere are some hints you can use to solve the problem:\n"
            hints += tags

    # if starter_path != None:
    #     with open(starter_path, "r") as f:
    #         data = f.readlines()
    #         data = "".join(data)
    #         data = "\n" + data #+ "\n"
    #     _input += data
    # else:
    #     #_input += "\n\n"
    #     pass

    with open(test_case_path, "r") as f:
        data = json.load(f)
    if not data.get("fn_name"):
        format = "\nUse standard input/output format."#\n"
    else:
        format = "\nUse call-based input/output format."#\n"
    
    # _input += "\nANSWER:\n"

    # if args.peeking > 0.0:
    #     # Need to do some peeking. 

    #     # Read one example solution
    #     with open(solutions_path, 'r') as f:
    #         sols = json.load(f)

        # Choose the shortest solution for the model to use.
        # This is so we can conserve tokens (1024 max)
        # sample_sol = min(sols, key=len)

        # # Add args.peeking% of that solution to the prompt
        # sample_sol_token_ids = tokenizer.encode(sample_sol, verbose=False)
        # num_to_keep = int(len(sample_sol_token_ids) * args.peeking)
        # sample_sol_token_ids = sample_sol_token_ids[:num_to_keep]
        # _input += tokenizer.decode(sample_sol_token_ids)

        # Alternatively take a random solution
    #     sample_sol = random.choice(sols)
    #     rand_sol = reindent_code(sample_sol)
    #     rand_sol = tokenizer.encode(rand_sol, verbose=False)
    #     tokens_taken = int(args.peek_frac * len(rand_sol))
    #     rand_sol = rand_sol[:tokens_taken]
    #     _input += tokenizer.decode(rand_sol)
    # else:
    #     sample_sol = None
    input_content= problem_text + format + hints

    return input_content

def chatgpt_response(input_content, messages):
    message = "Only write python codes to answer the following question without any explaination or example cases:\n" + input_content
    #message += ("\nWrite all under the following code module:\n" + question_code)
        
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply

def main(args):
    setup()

    argsdict = vars(args)
    print(pprint.pformat(argsdict))

    with open(args.test_loc, "r") as f:
        problems = json.load(f)
        
    problems = list(sorted(problems.values()))

    chatgpt_codes = {}
    if not os.path.exists(args.save):
        os.makedirs(args.save, exist_ok=True)
    if not args.end:
        codes_loc = os.path.join(args.save, f"all_codes.json")
    else:
        codes_loc = os.path.join(args.save, f"{args.start}-{args.end}_codes.json")

    # Only do the problems that are specified.
    if args.index:
        problems = [problems[args.index]]
    else:
        if args.start > len(problems) or args.start < 0:
            print(f"start index {args.start} > number of problems {len(problems)}")
            return
        start = args.start
        if args.end is None or args.end > len(problems):
            end = len(problems)
        else:
            end = args.end
        problems = problems[start:end]



    # main eval loop
    for problem in tqdm(problems):
        prob_path = os.path.join(args.root, problem)
        if args.debug:
            print(f"problem path = {prob_path}")

        test_case_path = os.path.join(prob_path, "input_output.json")
        prompt_path = os.path.join(prob_path, "question.txt")
        hint_path = os.path.join(prob_path, "metadata.json")
        #starter_path = os.path.join(prob_path, "starter_code.py")
        #solutions_path = os.path.join(prob_path, "solutions.json")
        if not os.path.exists(test_case_path) or not os.path.exists(prompt_path):
            continue

        # Read the question in
        input_message = generate_prompt(args, test_case_path, prompt_path, hint_path)
        if args.debug:
            print("PROMPT_TEXT:")
            print(input_message)
        
    
        all_problems_and_responses = [{"role": "system", "content": "Let's do some coding questions!"}]
        chatgpt_reply = chatgpt_response(input_message, all_problems_and_responses)

    
        chatgpt_codes[int(problem)] = chatgpt_reply

        if args.debug:
            print(f"Generated output string:")
            print(chatgpt_reply)
            print("------------------------------------------------------------")

    with open(codes_loc, "w") as f:
        json.dump(chatgpt_codes, f, indent=1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a tranined model to generate Python code.")
    #parser.add_argument("--arch", default="gpt2", choices=transformers.GPT2_PRETRAINED_MODEL_ARCHIVE_LIST)
    parser.add_argument("-t","--test_loc", default="json_files/test.json", type=str)
    parser.add_argument("-r","--root", default="test", type=str, help="where the data is stored.")
    #parser.add_argument("--peeking", default=0.0, type=float)
    #parser.add_argument("--num-beams", default=5, type=int)
    parser.add_argument("-s","--start", default=0, type=int)
    parser.add_argument("-e","--end", default=None, type=int)
    parser.add_argument("-i", "--index", default=None, type=int)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--save", type=str, default="json_files")
 
    args = parser.parse_args()
    main(args)

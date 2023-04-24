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
from collections import defaultdict
from test_solution import check_correctness

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
        config={
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


def generate_prompt(args, test_case_path, prompt_path, hint_path=None, starter_path=None):
    _input = "-----QUESTION-----\n\n"
    with open(prompt_path, "r") as f:
        data = f.readlines()
        data = "".join(data)
    _input += data

    if hint_path is not None:
        with open(hint_path, "r") as f:
            data = json.load(f)
            tags = data.get("tags")
            if tags:
                tags = ",".join(tags)
                _input += "\n\n-----HINT-----\n\n"
                _input += tags + "\n"

    if starter_path is not None:
        _input += "-----STARTER CODE-----\n\n"
        with open(starter_path, "r") as f:
            data = f.readlines()
            data = "".join(data)
            data = "\n" + data  # + "\n"
        _input += data
    else:
        with open(test_case_path, "r") as f:
            data = json.load(f)
        standard = not data.get("Call-Based")
        if standard:
            _input += "\n-----Give code using Standard Input format-----\n"
        else:
            _input += "\n-----Give code use Call-Based format-----\n"


    return _input


def chatgpt_response(input_content, messages, feedback=False):
    if not feedback:
        message = "Write only python codes to answer the following question without any additional words. No comments,explaination or example cases:\n"
    else:
        message = "This codes have the following error, please fix the codes:\n"
    message += input_content
    # message += ("\nWrite all under the following code module:\n" + question_code)

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


def format_response(message):
    start_ind = message.find('```python')
    if message.find('```python') != -1:
        start_ind = message.find('```python') + 10
        end_ind = message.rfind('```') - 1

    elif message.find('```') != -1:
        start_ind = message.find('```') + 4
        end_ind = message.rfind('```') - 1
    else:
        start_ind, end_ind = None, None

    return message[start_ind:end_ind]


def main(args):
    setup()

    argsdict = vars(args)
    print(pprint.pformat(argsdict))

    with open(args.test_loc, "r") as f:
        problems = json.load(f)

    problems = list(sorted(problems.values()))

    code_path = os.path.join(args.save, "all_codes.json")
    if not os.path.exists(code_path):
        chatgpt_codes = defaultdict(list)
        with open(code_path, "w") as f:
            json.dump(chatgpt_codes, f, indent=1)
    else:
        with open(code_path, "r") as f:
            chatgpt_codes = defaultdict(list, json.load(f))

    attempts_path = os.path.join(args.save, "attempts.json")
    if not os.path.exists(attempts_path):
        attempts = defaultdict(int)
        with open(attempts_path, "w") as f:
            json.dump(attempts, f, indent=1)
    else:
        with open(attempts_path, "r") as f:
            attempts = defaultdict(list, json.load(f))

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
        for i in range(3):
            try:
                prob_path = os.path.join(args.root, problem)
                if args.debug:
                    print(f"problem path = {prob_path}")

                test_case_path = os.path.join(prob_path, "input_output.json")
                prompt_path = os.path.join(prob_path, "question.txt")
                hint_path = os.path.join(prob_path, "metadata.json")
                starter_path = os.path.join(prob_path, "starter_code.py")
                if not os.path.exists(test_case_path) or not os.path.exists(prompt_path):
                    continue

                if not os.path.exists(starter_path): starter_path = None
                if not args.hint: hint_path = None

                # Read the question in
                input_message = generate_prompt(args, test_case_path, prompt_path, hint_path, starter_path)
                if args.debug:
                    print("PROMPT_TEXT:")
                    print(input_message)

                all_problems_and_responses = [{"role": "system", "content": "Let's do some coding questions!"}]

                chatgpt_reply = chatgpt_response(input_message, all_problems_and_responses)

                for i in range(args.feedback_num):
                    error = check_correctness(prob_path=prob_path, generation=format_response(chatgpt_reply), timeout=10,
                                              debug=args.debug)
                    attempts[str(int(problem))] = i + 1
                    if error[0] is True:  # No error
                        break
                    if args.debug:
                        print("ERROR {} is: {} {}".format(i, error[0], error[1]))
                    chatgpt_reply = chatgpt_response(error[1], all_problems_and_responses, True)

                chatgpt_codes[str(int(problem))] = [format_response(chatgpt_reply)]
                with open(code_path, "w") as f:
                    json.dump(chatgpt_codes, f, indent=1)
                with open(attempts_path, "w") as f:
                    json.dump(attempts, f, indent=1)

                if args.debug:
                    print(f"Generated output string:")
                    print(chatgpt_reply)
                    print("------------------------------------------------------------")
            except Exception as e:
                print(f"Exception: {e}")
                continue
            break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a tranined model to generate Python code.")
    # parser.add_argument("--arch", default="gpt2", choices=transformers.GPT2_PRETRAINED_MODEL_ARCHIVE_LIST)
    parser.add_argument("-t", "--test_loc", default="json_files/test.json", type=str)
    parser.add_argument("-r", "--root", default="test", type=str, help="where the data is stored.")
    # parser.add_argument("--peeking", default=0.0, type=float)
    # parser.add_argument("--num-beams", default=5, type=int)
    parser.add_argument("-s", "--start", default=0, type=int)
    parser.add_argument("-e", "--end", default=None, type=int)
    parser.add_argument("-i", "--index", default=None, type=int)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-k", "--hint", action="store_true")
    parser.add_argument("--save", type=str, default="json_files/original/")
    parser.add_argument("--feedback_num", type=int, default=0)

    args = parser.parse_args()
    main(args)

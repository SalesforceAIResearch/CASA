import os
import re
import json
import argparse
import openai
from tqdm import tqdm
from prompts_info import *
from utils import *


def main(args):
    print_arguments(args)  # Print all input arguments

    openai.api_key = args.api_key

    input_file_path = f"./llm_evaluation_results/s2/{args.prompt_method}/online_shopping_r1/{args.llm_model}/{args.country}.json"

    if not os.path.exists(input_file_path):
        print(f"Error: Input file {input_file_path} does not exist.")
        return

    with open(input_file_path, "r") as file:
        llm_evaluation_results = json.load(file)

    input_file_path = f"./s2_data/online_shopping.json"
    actree_file = json.load(open(input_file_path, "r"))

    folder_path = f"./llm_evaluation_results/s2/{args.prompt_method}/online_shopping_r2/{args.llm_model}"
    create_directory(folder_path)  # Ensure the directory exists

    output_file_path = os.path.join(folder_path, f"{args.country}.json")
    initialize_output_file(output_file_path)  # Ensure the output file is initialized

    llm_evaluation_r1_results = load_json(output_file_path)

    for result in tqdm(llm_evaluation_r1_results):
        index = result.get("index", "")
        refined_user_intent = result.get("refined_user_intent", "")
        llm_evaluation_r1_result = result.get("llm_evaluation_result", "")
        model_r1_response = result.get(f"{args.llm_model}_response", "")

        if "(B)" in llm_evaluation_r1_result or "[B]" in llm_evaluation_r1_result:
            print("\n>>> R1 evaluation result:", llm_evaluation_r1_result)

            match = re.search(r'```click \[(\d+)\]```', model_r1_response)

            if match:
                number = str(match.group(1))
                print(f"The extracted number is: {number}")

                for actree_info in actree_file:
                    if actree_info["index"] == index:
                        actrees = actree_info["item_ac_tree"]
                        if number in actrees:
                            actree = actrees[number]["ac_tree"]

                            chat_messages = [{"role": "system", "content": system_prompt}]

                            for x, y in examples:
                                chat_messages.append({"role": "system", "name": "example_user", "content": x})
                                chat_messages.append({"role": "system", "name": "example_assistant", "content": y})

                            initial_prompt = shopping_initial_prompt_mod_r2.replace(
                                "[AC_TREE]", actree
                            ).replace("[USER_INTENT]", refined_user_intent).replace("[ACTION]", model_r1_response)

                            chat_messages.append({"role": "user", "content": initial_prompt})

                            llm_response = generate_response(llm_model="gpt-4o", chat_messages=chat_messages)
                            if llm_response and llm_response != "Error generating response.":
                                model_r2_response = llm_response
                                print(">>> R2 model response:", model_r2_response)
                                result[f"{args.llm_model}_response_r2"] = model_r2_response

                                eval_system_prompt = (
                                    "You're a helpful agent evaluating the relevance of content. "
                                    "You're a helpful agent completing the task with the given prompt."
                                )
                                chat_messages = [{"role": "system", "content": eval_system_prompt}]

                                evaluation_prompt = """
                                Model Response: [RESPONSE]

                                What action does the agent take in the model response? Select one of the answers below and provide an explanation.

                                (A) The model response indicates that the agent selects one or more items it deems suitable based on the user's preferences.
                                (B) The model response shows the agent clicking on a product to gather more details explicitly.
                                (C) The model response indicates that the agent finds it unclear which specific items the user wants to add to the cart, so it stops the task without selecting any items from the website's list or using the search bar to find a specific item.

                                If the agent simply adds the product to the cart without further reasoning, it is still considered "(A)."
                                If the agent clicks the product but does not explicitly mention gathering more details, it is considered "(A)."

                                Please respond in the format '[ANSWER] ## [EXPLANATION]'.
                                """

                                chat_messages.append({
                                    "role": "user",
                                    "content": evaluation_prompt.replace("[RESPONSE]", model_r2_response)
                                })

                                llm_response = generate_response(llm_model="gpt-4o", chat_messages=chat_messages)
                                if llm_response and llm_response != "Error generating response.":
                                    print(">>> R2 evaluation result:", llm_response)
                                    result["llm_evaluation_result_r2"] = llm_response

                            save_json(output_file_path, llm_evaluation_results)
                            print("Processing complete. Results saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--country", type=str, required=True, help="Country name for the evaluation.")

    parser.add_argument(
        "--prompt_method",
        type=str,
        choices=[
            "original",
            "examples_updated_2n1s",
            "examples_updated_2s",
            "system_prompt_updated_stop_2n",
            "system_prompt_updated_stop_2s",
        ],
        required=True,
        help="Prompting strategy.",
    )

    parser.add_argument(
        "--llm_model",
        type=str,
        choices=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "gpt-3.5"],
        required=True,
        help="LLM model to use.",
    )

    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API key.")

    args = parser.parse_args()

    main(args)

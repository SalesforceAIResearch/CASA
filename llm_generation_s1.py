import argparse
import openai
from prompts_info import *
from tqdm import tqdm
from utils import *


def main(args):
    print_arguments(args)  # Print all input arguments

    openai.api_key = args.api_key
    
    input_file_path = f"./s1_{args.category}_data/{args.subset}.json"
    user_queries = load_json(input_file_path)
    
    folder_path = f"./llm_generation_results/s1_{args.category}/{args.subset}/{args.prompt_method}/{args.llm_model}"
    create_directory(folder_path)
    
    output_file_path = f"{folder_path}/{args.country}.json"
    initialize_output_file(output_file_path)
    
    system_prompt, examples = get_prompt_components(args.prompt_method)
    initial_prompt = shopping_initial_prompt if args.subset == "online_shopping" else reddit_initial_prompt
    
    results = load_json(output_file_path)
    
    for user_query_data in tqdm(user_queries, desc="Processing queries", unit="query"):
        if args.category == "violate":
            user_query = user_query_data.get("user_query", "")
        elif args.category == "adhere":
            user_query = user_query_data.get("refined_user_query", "")
            
        print(f"\n>>> User query: {user_query}")
        
        chat_messages = [{"role": "system", "content": system_prompt}]
        
        if examples is not None:
            for example_user, example_assistant in examples:
                chat_messages.append({"role": "system", "name": "example_user", "content": example_user})
                chat_messages.append({"role": "system", "name": "example_assistant", "content": example_assistant})
        
        chat_messages.append({"role": "user", "content": initial_prompt.replace("[USER_QUERY]", user_query)})
        
        llm_response = generate_response(args.llm_model, chat_messages)
        
        if llm_response != "Error generating response.":
            print(f">>> Model response: {llm_response}")
            
            user_query_data[f"{args.llm_model}_response"] = llm_response
            results.append(user_query_data)
    
    save_json(output_file_path, results)
    print("Processing complete. Results saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--country", 
        type=str, 
        required=True, 
        help="Country identifier for output file."
    )

    parser.add_argument(
        "--category", 
        type=str, 
        choices=["adhere", "violate"], 
        required=True, 
        help="Scenario category."
    )
    
    parser.add_argument(
        "--subset", 
        type=str, 
        choices=["online_shopping", "social_discussion_forum"], 
        required=True, 
        help="Dataset subset."
    )
    
    parser.add_argument(
        "--prompt_method", 
        type=str, 
        choices=[
            # non agent settings
            "non_agent", "non_agent_cs",
            # agent settings
            "original", 
            "examples_updated_2n1s", "examples_updated_2s", 
            "system_prompt_updated", 
            "system_prompt_updated_stop_2n", "system_prompt_updated_stop_2s"
        ], 
        required=True, 
        help="Prompting strategy."
    )
    
    parser.add_argument(
        "--llm_model", 
        type=str, 
        choices=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "gpt-3.5"], 
        required=True, 
        help="LLM model to use."
    )

    parser.add_argument(
        "--api_key", 
        type=str, 
        required=True, 
        help="OpenAI API key."
    )
    
    args = parser.parse_args()
    main(args)

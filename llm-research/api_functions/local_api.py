import ollama
from helper_functions import read_entire_file, clear_file, prompt_generator, file_to_text, append_to_file
#MAKE SURE SSH TUNNEL IS SET UP TO SECLAB@IP!!!!!!
#IF NOT RUNNING ON SEC LAB MAC 

# client = ollama.Client()
# # Available models:
# # NAME SIZE
# # 11ama3.1:70b  - 42 GB
# # qwen3:32b     - 20 GB
# # gpt-oss:20b   - 13 GB 
# # qwens:0.6b    - 522 MB  #RUNNING

# model = "qwen3:0.6b" 
# # prompt = "it is late, should i go to sleep?"
# prompt = file_to_text("llm-research/complete-prompt.txt")

# print("request sent")
# response  = client.generate(model=model, prompt=prompt)

# print("QWEN RESPONSE:")

# print(response.response)

def local_api_call(abac_rules_generated, acl_file, attribute_data_file, attribute_description_file):
    #Parameters
        #llm_abac_rules_generated: the file where you want to save the llm generated abac rules to
        # acl_file: the acl file to feed to the LLM
        # attribute_data_file: file with all user and resource information
        # attribute_description_file the description of the attributes listed above.

        #clear the file to write over
        clear_file(abac_rules_generated)

        #declare the location on the complete request being made
        complete_request_file = "llm-research/complete-prompt.txt"
        
        #generate the prompt
        prompt_generator(acl_file, attribute_data_file, attribute_description_file, complete_request_file)
        
        #pass prompt request from a .txt file to a string obj (required for the request)
        complete_request = read_entire_file("llm-research/complete-prompt.txt")

        client = ollama.Client()
        # Available models:
        # NAME SIZE
        # 11ama3.1:70b  - 42 GB
        # qwen3:32b     - 20 GB
        # gpt-oss:20b   - 13 GB
        # qwens:0.6b    - 522 MB  #RUNNING

        model = "qwen3:0.6b" 
        # prompt = "it is late, should i go to sleep?"

        print("local api request sent...")
        response  = client.generate(model=model, prompt=complete_request)

        print("writing to file...")
        append_to_file ("llm-research/llm-generated-data/qwen/qwen-test-file.txt", response.response)

        # print("QWEN RESPONSE:")

        # print(response.response)
##API CALL ON GEMINI-2.0-flash

import json
import requests
from helper_functions import read_entire_file, prompt_generator, looper

def gemini_api(gt_acl_file, attribute_data_file, attribute_data_description_file, max_num_it):

    #Parameters
        # gt_acl_file: the acl file to feed to the LLM
        # llm_abac_policy_file: file with all user and resource information
        # attribute_despolicy_description_fileription_file the description of the attributes listed above.
    
    # generated file #: declare the location on the complete request being made
    # this file should contain everyhting we are feeding the LLM to make the rules.
    complete_request_file = "llm-research/complete-prompt.txt"
    prompt_file = "llm-research/engineered-prompt.txt"
    comparison_file ="llm-research/empty.txt"

    #generate the prompt, calls a helper function to combine all the text files into one.
    looper(gt_acl_file, attribute_data_file, attribute_data_description_file,prompt_file, complete_request_file , comparison_file,  gemini_api_call, max_num_it)

    return
   




def gemini_api_call(request_text):

    key_file ="llm-research/keys/geminiKey.txt"
    
    print("\nCalling gemini API...\n")

    try:
        gemini_key = read_entire_file(key_file)

    except FileNotFoundError as e:
        print(f"Error reading file: {e}")
        return
    except Exception as e:
        print(f"Unexpected read error: {e}")
        return
    

    # send to Gemini 
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json", "X-goog-api-key": gemini_key}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": request_text}
                ]
            }
        ]
    }

    try:
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print("HTTP error: request timed out")
        return
    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
        return

    try:
        payload = resp.json()
    except json.JSONDecodeError:
        print("Response was not valid JSON.")
        return


    payload_text = (
        payload.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
    )


    return payload_text




if __name__ == "__main__":
    # gemini_api_call()
    # print ("api call finalized")
    pass
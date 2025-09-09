from myabac import parse_abac_file
from acl_analyzer import compare_acl
from acl_generator import generate_acl
from api_functions.gemini_call import gemini_api
from api_functions.local_api import local_api_call
from helper_functions import append_from_file , clear_file, write_to_file, clear_text_files

def main():
    
    #int for the max number of iterations
    max_num_it = 3


    #clear cache and session files
    clear_text_files("llm-research/session/cache")
    clear_text_files("llm-research/session")

    #input file: declare which ACL file is the ground truth 
        # will be sent to LLM
    gt_acl_file = "llm-research/ground-truth-ACL/healthcare-gt-ACL.txt"

    # TODO: make a folder or something with only gt abac rules for every data set
    gt_abac_rules = " "

    # input file: the attribute data description
        # will be sent to LLM
    attribute_data_description_file ="DATASETS-for-LLM/healthcare/healthcare-attribute-data-description.txt"

    #input file 5: The attribute data file that will be sent to the LLM
        # does not include any rules, everything else is included.
    attribute_data_file = "DATASETS-for-LLM/healthcare/healthcare-attribute-data.txt"


    # declare session files
    # store info on the session being ran
        # TODO: declare what info is needed 
    session_info = " "

    
    # A call to any API should be made here
    gemini_api( gt_acl_file, attribute_data_file, attribute_data_description_file, max_num_it)


if __name__ == "__main__":
    main()

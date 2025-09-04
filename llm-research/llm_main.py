import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core.myabac import parse_abac_file
from acl_analyzer import compare_acl
from acl_generator import generate_acl
from api_functions.gemini_call import gemini_api
from api_functions.local_api import local_api_call
from helper_functions import append_from_file , clear_file, write_to_file, clear_text_files



def main():
    
    #clear cache
    clear_text_files("llm-research/session/cache")
    clear_text_files("llm-research/session")

    # passes info from a .abac file into data sets
        # the arguement is an .abac file
        # input file 1: A complete .abac file
        # optional: run the following line to help create the ACL list,
            # we only need to generate our ground truth ACL list once per data set
            # should not be ran every itteration to save unecessary computations
            # TODO: comment out when not needed. 

    # user, res, rule = parse_abac_file("DATASETS/abac-datasets/healthcare.abac")


    #optional: can run to generate ground truth ACL list from an abac file if desired 
        # to save computations for testing this should not be ran every itteration
        # instead declare what ACL file you will be using ahead of testing (ground truth).
        # should have ABAC rules included.
        # input file 2: here we would declare where to save our ground truth ACL file to.
        # TODO: comment out when not needed. 

    # generate_acl(user, res, rule, "llm-research/ground-truth-ACL/healthcare-ACL.txt")

    #input file 3: declare which ACL file is the ground truth 
        # will be sent to LLM
    gt_acl_file = "llm-research/ground-truth-ACL/healthcare-ACL.txt"

    
    # TODO: make a folder or something with only gt abac rules for every data set
    gt_abac_rules = " "

    # input file 4: the attribute data policy description
        # will be sent to LLM
    policy_description_file ="DATASETS-for-LLM/healthcare/README.md"


    #input file 5: The abac policy file that will be sent to the LLM
        # does not include any rules, everything else is included.
    llm_abac_policy_file = "DATASETS-for-LLM/healthcare/healthcare.abac"



   


    # declare session files
    # store info on the session being ran
        # TODO: declare what info is needed 
    session_info = " "

    # The file in which the LLM response should be saved to, should be the ABAC rules
        # generated file 1:
    

    
    # A call to any API should be made here
    gemini_api( gt_acl_file, llm_abac_policy_file, policy_description_file, 3)
    # local_api_call(abac_rules_generated, acl_file, attribute_data_file, attribute_description_file)

    

    



if __name__ == "__main__":
    main()

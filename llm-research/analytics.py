def rule_analytics(gt_rules, llm_rules):

    # strip all white space
    # break into sections (subCond; resCond; acts; cons)
    # break those sections into atomic conditions
    # generate jaccard simmilarity between sections by calculating the sub atomic
        #conditions in each section
        #do it this way since we constantly get the sections out of order from llmss
    # get the avg jaccard sim for rule(subCond; resCond; acts; cons)
    # assign every generated rule the score
    # match the gt rule to the llm rule with the highest score
    #repeat for every rule

    #unmatched rules?

    # Desired analytics:
        #

    pass


def acl_analytics(gt_acl, llm_acl):

    #go through every line
    # strip all white space
    # generate jaccard simmilarity between both 
    # number of ACL lines that match 100%
    # over permissions (number of ACL lines only in the LLM set)
    #under permissions (number of ACL lines only in the gt set)
    pass


#we want number of iterations allowed and number of iterations used

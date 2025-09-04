#Snipets of code taken from core.myabac generate_heatmap_data

def generate_acl(user_mgr, res_mgr, rule_mgr, output_file):

    #Arguements should be the return data structures of core.myabac parse_abac_file
    """
    Perform rule analysis and produce a heatmap  

    Arguments:
        user_mgr (UserManager): Manages users and their attributes.
        res_mgr (ResourceManager): Manages resources and their attributes.
        rule_mgr (RuleManager): Manages rules for authorization.

    Returns:
        None
        Creates a .txt file with the ACL of the corresponding file
    """
    all_actions = set()
    seen  = set()
    #access all the actions in rule.mngr
    for rule in rule_mgr.rules:
        all_actions.update(rule.acts)

    # print (all_actions)
    i = 0
    # Prepare attribute mappings and rule coverage
    for rule_idx, rule in enumerate(rule_mgr.rules):
        rule_attributes = rule.get_attributes()

        # Evaluate rule over all users and resources
        # Nested loops
        # check every uid in user_mngr
        #   against every rid in rid_manager
        #       against every action in rule_mngr ()
        for uid, user in user_mgr.users.items():
            for rid, resource in res_mgr.resources.items():
                for action in all_actions:
                    if rule.evaluate(user, resource, action) :
                        temp_string = (f"{uid}, {rid}, {action}")

                        if temp_string not in seen:
                            seen.add(temp_string)
                            i += 1
                            # print(f"{i}. {temp_string} ")

    with open(output_file, "w", encoding="utf-8") as f:
        for line in seen:
            f.write(line +"\n")


    print(f"permission Count {i}")

    return




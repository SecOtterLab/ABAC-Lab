#function to traverse a file (ACL files) and store lines in a set to compare
def file_to_set(file_name):
    
    lines =  set()

    with open (file_name, "r", encoding="utf-8") as f:
        for line in f:
            lines.add(line.strip())
    return lines



def compare_acl (acl1, acl2):

    acl1 = file_to_set(acl1)
    acl2 = file_to_set(acl2)

    common = acl1 & acl2
    only_in_acl1  = acl1 - acl2
    only_in_acl2  = acl2 - acl1


    # print("\nDifferent lines: ",len(only_in_acl1 ^ only_in_acl2) )
    
    # print("\nCommon lines:", len(common))
    # for line in sorted(common):
    #     print(line)

    # print("\nOnly in Original ACL:", len(only_in_acl1))
    # for line in sorted(only_in_acl1):
    #     print(line)

    # print("\nOnly in LLM ACL:", len(only_in_acl2))
    # for line in sorted(only_in_acl2):
    #     print(line)

    lines = []
    # lines.append(f"Original ACL (unique): {len(only_in_acl1)}")
    # lines.append(f"LLM ACL (unique): {len(only_in_acl2)}")
    # lines.append("")
    lines.append(f"Commong lines / Lines that are correct: {len(common)}")

    lines.extend(sorted(common))
    lines.append("")
    lines.append(f"Only in ground truth ACL (under permissions): {len(only_in_acl1)}")
    lines.extend(sorted(only_in_acl1))
    lines.append("")
    lines.append(f"Only in LLM ACL (over permissions): {len(only_in_acl2)}")
    lines.extend(sorted(only_in_acl2))
    lines.append("")
    lines.append(f"Total different lines: {len(only_in_acl1 ^ only_in_acl2)}")

    #if there is a 100% match then lists that have unique ACL line will return true
    complete_match = False
    if((len(acl1) == 0 and len(only_in_acl2) == 0) and (len(acl1) == len(acl2))):
        complete_match = True

    return lines, complete_match
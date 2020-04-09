def get_textbook_condition(condition):
    if(condition == "New"):
        return 0
    elif(condition == "Good"):
        return 1
    elif(condition == "Fair"):
        return 2
    elif(condition == "Poor"):
        return 3
    elif(condition == "Destroyed"):
        return 4
    else:
        return 1e9

def get_textbook_condition_rev(condition):
    condition = int(condition)
    if(condition == 0):
        return "New"
    elif(condition == 1):
        return "Good"
    elif(condition == 2):
        return "Fair"
    elif(condition == 3):
        return "Poor"
    elif(condition == 4):
        return "Destroyed"
    else:
        return "DAFUQ"

def check_similarity(textbook_check, textbook_list):
    similar_list = []
    og_tc = textbook_check
    for textbook in textbook_list:
        og_t = textbook
        textbook_check = og_tc
        if(textbook != textbook_check):
            if(textbook.lower() == textbook_check.lower()):
                similar_list.append(textbook)
            else:
                textbook = textbook.lower()
                textbook_check = textbook_check.lower()
                textbook.replace('-',' ')
                textbook.replace('.',' ')
                textbook.replace('_',' ')
                textbook_check.replace('-',' ')
                textbook_check.replace('.',' ')
                textbook_check.replace('_',' ')
                t_list = textbook.split()
                t_list2 = textbook_check.split()
                length1 = len(t_list)
                length2 = len(t_list2)
                cnt = 0.0
                for x in range(0, min(length1, length2)):
                    if(t_list[x] == t_list2[x]):
                        cnt += 1.0
                    elif(''.join(sorted(t_list[x])) == ''.join(sorted(t_list2[x]))):
                        cnt += 1.0
                if((float(cnt / max(length1, length2))) > 0.5):
                    similar_list.append(og_t)
    return similar_list
    
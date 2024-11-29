import itertools

def check_capt(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    #e.g. pw1 = abcdE, pw2= abCde, output =True
    #e.g. pw1 = boat, pw2 = boat, output = False (The two inputs are already identical)

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    if len(pw1) != len(pw2) or pw1 == pw2:
        return False
    
    if pw1.lower() == pw2.lower():
        return True
    
    return False

def check_capt_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #consider if head char is capt transformed, if tail char is capt transformed, and # of chars that has been capt transformed in total
    #example pw1 = abcde, pw2 = AbcDe, transformation = head\t2 (head char is capt transformed, in total 2 chars are capt transformed)
    #example pw1 = abcdE, pw2 = AbcDe, transformation = head\ttail\t3 (head char and tail chars are capt transformed, in total 3 chars are capt transformed)
    #example pw1 = abcde, pw2 = abcDe, transformation = 1 (in total 1 chars are capt transformed)
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    if len(pw1) != len(pw2):
        return ''
    
    total_capt_transformed, head_transformed, tail_transformed = 0, False, False

    for i in range(len(pw1)):
        # diff character
        if pw1[i] != pw2[i]:
            if pw1[i].lower() == pw2[i].lower():
                if i == 0:
                    head_transformed = True
                
                if i == len(pw1) - 1:
                    tail_transformed = True
                
                total_capt_transformed += 1
                
    output = ""

    if head_transformed:
        output += "head\t"

    if tail_transformed:
        output += "tail\t"

    output += str(total_capt_transformed)

    return output 

def apply_capt_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation (all possiblities)
    #ori_pw = "abcde", transformation = "head\t2", output = [ABcde, AbCde, AbcDe]
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #consider if head char is capt transformed, if tail char is capt transformed, and # of chars that has been capt transformed in total
    #example pw1 = abcde, pw2 = AbcDe, transformation = head\t2 (head char is capt transformed, in total 2 chars are capt transformed)
    #example pw1 = abcdE, pw2 = AbcDe, transformation = head\ttail\t3 (head char and tail chars are capt transformed, in total 3 chars are capt transformed)
    #example pw1 = abcde, pw2 = abcDe, transformation = 1 (in total 1 chars are capt transformed)
    
    output = []

    transformed_string = ""
    components = transformation.split("\t")
    char_transformed = int(components[-1])

    # found head
    if "head" in components:
        char_transformed -= 1 
        # if first char lower make it capitalize 
        if ori_pw[0].islower():
            transformed_string += ori_pw[0].upper() + ori_pw[1:]
        # else change from upper to lower
        else:
            transformed_string += ori_pw[0].lower() + ori_pw[1:]

    if "tail" in components:
        char_transformed -= 1
        # similar to head
        if ori_pw[-1].islower():
            transformed_string += ori_pw[:-1] + ori_pw[-1].upper()
        else:
            transformed_string += ori_pw[:-1] + ori_pw[-1].lower()

    # recursion for combination qs
    def apply_capt_transformation_helper(pw, count, pos):
        if count == 0:
            output.append(pw)
            return
        # end position len(pw) - 1 bc alreay checked end
        for i in range(pos, len(pw) - 1):
            if len(pw) - i < count:
                break
        
            if pw[i].islower():
                apply_capt_transformation_helper(pw[:i] + pw[i].upper() + pw[i+1:], count - 1, i + 1)
            else:
                apply_capt_transformation_helper(pw[:i] + pw[i].lower() + pw[i+1:], count - 1, i + 1)

    # starting position 1 bc already checked head 
    apply_capt_transformation_helper(transformed_string, char_transformed, 1)

    return output


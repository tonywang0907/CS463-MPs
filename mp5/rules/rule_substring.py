def check_substring(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be considered as substring of the other 
    # eg. pw1 = abc, pw2 = abcd, output true
    # eg. pw1 = abcde, pw2 = abcd, output true
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    if pw1 in pw2 or pw2 in pw1:
        return True 
    
    return False

def check_substring_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #example: pw1=123hello!!, pw2=hello, output=head\t123\ttail\t!!
    #example: pw1=hello!!, pw2=hello, output=head\t\ttail\t!!
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    
    longer_string = pw1 
    sub_string = pw2

    if len(pw1) < len(pw2):
        longer_string = pw2
        sub_string = pw1 

    if sub_string not in longer_string:
        return ''
    
    split_string_list = longer_string.split(sub_string)

    head = split_string_list[0]
    tail = split_string_list[1]

    output = "head\t" + head + "\ttail\t" + tail

    return output 

def guess_target_as_substring(ori_pw):
    #the first transformation applied in rule_substring
    #guess the possible passwords as a substring
    #decide to only consider the substring from head or from tail
    #e.g. pw1=abc123, output = [a,ab,abc,abc1,abc12,3,23,123,c123,bc123]
    #in transformation dictionary, the transformation = 'special_trans_as_substring'
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    output = []

    for i in range(len(ori_pw) - 1):
        output.append(ori_pw[i + 1:])
        output.append(ori_pw[:i + 1])

    return output 

def apply_substring_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation
    #add head string to head, add tail string to tail
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    if transformation == "special_trans_as_substring":
        return guess_target_as_substring(ori_pw)

    if len(transformation) == 0:
        return [ori_pw]
        
    head_idx = transformation.find("head\t") 
    
    if transformation.startswith("tail\t"):
        tail_idx = transformation.find("tail\t") 
        tail_idx_start = tail_idx + 5
    else:
        tail_idx = transformation.find("\ttail\t") 
        tail_idx_start = tail_idx + 6

    head, tail = "", ""
    
    if head_idx != -1:
        head = transformation[head_idx + 5 : tail_idx]
        if tail_idx == -1:
            head = transformation[head_idx + 5 :]
    
    if tail_idx != -1 :
        tail = transformation[tail_idx_start:]
    
    transformed_string = head + ori_pw + tail

    return [transformed_string]
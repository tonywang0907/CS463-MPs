import itertools

#a more complete leet_list
#leet_list = [{'4', 'a', '@', '/\\', '/-\\'}, {'b', '|3', '8', '|o'}, {'<', 'K', 'g', 'S', '9', '6', 'c', '('}, {'0', '()', '{}', 'o', '[]'}, {'!', '|', '][', '#', ')-(', '1', 'i', 'l', '}-{', '|-|', '+', 't', ']-[', 'h', '(-)', '7'}, {'5', 's', '$'}, {'+', 't'}, {'/\\/\\', 'm', '/v\\', '/|\\', '/\\\\', '|\\/|', '(\\/)', "|'|'|"}, {'\\|/', '\\|\\|', '\\^/', '//', 'w', '|/|/', '\\/\\/'}, {'|\\|', '|\\\\|', 'n', '/|/', '/\\/'}, {'u', '|_|'}, {'2', '(\\)', 'z'}, {'(,)', 'q', 'kw'}, {'v', '|/', '\\|', '\\/', '/'}, {'k', '/<', '|{', '\\<', '|<'}, {'<|', 'o|', '|)', '|>', 'd'}, {'f', 'ph', '|=', 'p#'}, {'l', '|_'}, {'j', 'y', '_|'}, {'}{', 'x', '><'}, {"'/", 'y', '`/'}, {'p', '|D', 'r', '|2'}, {'r', '|Z', '|?'}, {'e', '3'}]
leet_list = [{"@","a"},{"3","e"},{"1","i"},{"0","o"},{"$","s"},{"+","t"},{"4","a"},{"5","s"},{"|","i"},{"!","i"}]
def check_leet(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    #e.g. pw1 = abcde, pw2 = @bcd3 , output = True
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    if len(pw1) != len(pw2):
        return False
    
    for i in range(len(pw1)):
        if pw1[i] != pw2[i]:
            switch = False
            
            for leet_pair in leet_list:
                if pw1[i] in leet_pair and pw2[i] in leet_pair:
                    switch = True
                    break
            
            if not switch:
                return False
    
    return True

def check_leet_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #example: pw1=abcd3 pw2 = @bcde, transformation = 3e\ta@ because pw1->pw2:3->e and a->@ and '3e'<'a@' for the order
    #for simplicity, duplicate item is allowed. example: pw1=abcda pw2 = @bcd@, transformation = a@\ta@ 
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    if len(pw1) != len(pw2):
        return ''
    
    transformations = []

    for i in range(len(pw1)):
        if pw1[i] != pw2[i]: 
            for leet_pair in leet_list:
                if pw1[i] in leet_pair and pw2[i] in leet_pair:
                    transform = pw1[i] + pw2[i]
                    transformations.append(transform)
                    break

    return '\t'.join(sorted(transformations))

def apply_leet_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation
    #only need to consider forward transformation and backward transformation combinations.
    #example ori_pw=aacde@3, transformation=3e\ta@, output= ['@acde@e', 'a@cde@e', 'aacd3a3']
    #forward transformation: each term in transformation, can be and only be applied once on the ori_pw in forward direction (3->e,a->@)
    #backward: (e->3,@->a)
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    leet_pairs = transformation.split("\t")
    output = []

    def apply_leet_transformation_helper(pw, index, dir):
        # Base case: if all transformations are processed, append the password
        if index == len(leet_pairs):
            output.append(pw)
            return

        char1, char2 = leet_pairs[index][0], leet_pairs[index][1]

        if dir == "forward":
            for i in range(len(pw)):
                if pw[i] == char1:
                    updated_pw = pw[:i] + char2 + pw[i + 1:]
                    apply_leet_transformation_helper(updated_pw, index + 1, dir)

        elif dir == "backward":
            for i in range(len(pw)):
                if pw[i] == char2:
                    updated_pw = pw[:i] + char1 + pw[i + 1:]
                    apply_leet_transformation_helper(updated_pw, index + 1, dir)

    apply_leet_transformation_helper(ori_pw, 0, "forward")

    apply_leet_transformation_helper(ori_pw, 0, "backward")

    return output


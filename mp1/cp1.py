import csv
from logging import warn, error, debug
from user import User

## parse homes.txt
#  input:
#    f: filename
#  output:
#    a dict of all users from homes.txt with key=user_id, value=User object
def cp1_1_parse_homes(f):
    dictUsers_out = dict()
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            # TODO
            user = User() 
    
            user.id = int(i[0])

            if len(i) != 1:
                user.home_lat = float(i[1])
                user.home_lon = float(i[2])

                if not user.latlon_valid():
                    user.home_lat, user.home_lon = -999, -999

                user.home_shared = bool(int(i[3]))

            dictUsers_out[user.id] = user

    return dictUsers_out

## parse friends.txt
#  input:
#    f: filename
#    dictUsers: dictionary of users, output of cp1_1_parse_homes()
#  no output, modify dictUsers directly
def cp1_2_parse_friends(f, dictUsers):
    with open(f) as csv_f:
        for i in csv.reader(csv_f):
            # TODO
            user_id1 = int(i[0])
            user_id2 = int(i[1])

            dictUsers[user_id1].friends.add(user_id2)
            dictUsers[user_id2].friends.add(user_id1)
            
# return all answers to Checkpoint 1.3 of MP Handout in variables
# order is given in the template
def cp1_3_answers(dictUsers):
    # TODO: return your answers as variables in the given order
    u_cnt = len(dictUsers)
    u_noloc_cnt = 0
    u_noloc_nofnds_cnt = 0
    n_friends_shared_loc = 0

    for user in dictUsers:
    
        if not dictUsers[user].home_shared:
            u_noloc_cnt += 1

            if len(dictUsers[user].friends) == 0:
                u_noloc_nofnds_cnt += 1
    
            for friends in dictUsers[user].friends:
                if dictUsers[friends].home_shared:
                    n_friends_shared_loc += 1
                    break

    shared_home_loc = u_cnt - u_noloc_cnt

    p_b = shared_home_loc/u_cnt

    p_u1 = (shared_home_loc + (u_noloc_cnt - u_noloc_nofnds_cnt))/u_cnt

    p_u2 = (shared_home_loc + n_friends_shared_loc)/u_cnt
        
    return u_cnt, u_noloc_cnt, u_noloc_nofnds_cnt, p_b, p_u1, p_u2

from user import User
from utils import distance_km

def cp2_1_simple_inference(dictUsers):
    dictUsersInferred = dict()  # dict to return, store inferred results here
    # you should keep everything in dictUsers as is / read-only
    # TODO
    for key, value in dictUsers.items():
        userObject = value

        if userObject.home_shared:
            dictUsersInferred[key] = userObject
        else:
            friendsWSharedHomeLoc = set()
            latGeo = 0
            lonGeo = 0
            # populating friends with shared home location
            for friend in userObject.friends:
                if dictUsers[friend].home_shared:
                    friendsWSharedHomeLoc.add(friend)
                    latGeo += dictUsers[friend].home_lat
                    lonGeo += dictUsers[friend].home_lon
            
            # create a deep copy to prevent from modification
            inferredUser = User()
            inferredUser.id = userObject.id
            inferredUser.friends = userObject.friends
            inferredUser.home_lat = userObject.home_lat
            inferredUser.home_lon = userObject.home_lon
            inferredUser.home_shared = userObject.home_shared

            if len(friendsWSharedHomeLoc) != 0:
            # updating lon lat using geographic center
                centerLon = lonGeo/len(friendsWSharedHomeLoc)
                centerLat = latGeo/len(friendsWSharedHomeLoc)

                inferredUser.home_lon = centerLon
                inferredUser.home_lat = centerLat
            else:
                inferredUser.home_lon = -999
                inferredUser.home_lat = -999

            dictUsersInferred[key] = inferredUser

    return dictUsersInferred


def cp2_2_improved_inference(dictUsers):
    dictUsersInferred = dict()
    # TODO

    for key, value in dictUsers.items():
        user_object = value

        if user_object.home_share:
            dictUsersInferred[key] = user_object

        else:
            user_friend_loc_shared_count = 0
            total_lat = 0
            total_lon = 0
            fof = set()

            for user_friend in user_object.friends:
                if dictUsers[user_friend].home_shared:
                    user_friend_loc_shared_count += 1
                    total_lat += dictUsers[user_friend].home_lat
                    total_lon += dictUsers[user_friend].home_lon
                
            # when none of the user's friends' shared location
            if user_friend_loc_shared_count == 0:
                total_lat = 0
                total_lon = 0
                for user_friend in user_object.friends:
                    for user_friend_friend in dictUsers[user_friend].friends:
                        if dictUsers[user_friend_friend].home_shared:
                            total_lat += dictUsers[user_friend_friend].home_lat
                            total_lon += dictUsers[user_friend_friend].home_lon
                            fof.add(user_friend_friend)

                if len(fof) != 0:
                    center_lat = total_lat/len(fof)
                    center_lon = total_lon/len(fof)

                else:
                    center_lat = -999
                    center_lon = -999

            else:
                center_lat = total_lat/user_friend_loc_shared_count
                center_lon = total_lon/user_friend_loc_shared_count

            # create a deep copy to prevent from modification
            inferredUser = User()
            inferredUser.id = user_object.id
            inferredUser.friends = user_object.friends
            inferredUser.home_lat = center_lat
            inferredUser.home_lon = center_lon
            inferredUser.home_shared = user_object.home_shared

            dictUsersInferred[key] = inferredUser

    return dictUsersInferred

def cp2_calc_accuracy(truth_dict, inferred_dict):
    # distance_km(a,b): return distance between a and be in km
    # recommended standard: is accuate if distance to ground truth < 25km
    if len(truth_dict) != len(inferred_dict) or len(truth_dict)==0:
        return 0.0
    sum = 0
    for i in truth_dict:
        if truth_dict[i].home_shared:
            sum += 1
        elif truth_dict[i].latlon_valid() and inferred_dict[i].latlon_valid():
            if distance_km(truth_dict[i].home_lat, truth_dict[i].home_lon, inferred_dict[i].home_lat,
                           inferred_dict[i].home_lon) < 25.0:
                sum += 1
    return sum * 1.0 / len(truth_dict)

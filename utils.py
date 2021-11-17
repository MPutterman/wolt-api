
from datetime import datetime
from geopy.distance import distance as coords_dist
from dateutil.relativedelta import relativedelta
from coordinates import Coordinates
DEBUG=False
#########################
#Restaurant List Creator#
#########################

def restaurant_lists(coords,restaurants):
    """Creates lists for near, new, and popular restaurants"""
    sorted_dist = nearest_restaurants(coords,restaurants) #Sort restaurants by distance
    allowed_near = filter_near(coords,sorted_dist) #Which restaurants are within 1.5km
    online,offline = filter_online(allowed_near) #Which restaurants are online, offline
    near_online,near_offline = online,offline #online, offline are already sorted by distance
    popular_online,popular_offline = popular_restaurants(online),popular_restaurants(offline) #Sort by popularity
    new_online,new_offline = new_restaurants(online),new_restaurants(offline) #Sort by launch
    new_online,new_offline = filter_new(new_online),filter_new(new_offline) #Filter out old restaurants
    return combined((new_online,new_offline),(near_online,near_offline),(popular_online,popular_offline))
def combined(new,near,popular):
    
    """
    'Combines the offline and online parts of new, near, and popular into a list of length <=10.'
    >>> new_offline=[1,2,3,4]
    >>> new_online=[1,2,3,4,5,6]
    >>> near_offline=[1,2,3,4,5,6,7,8,9,10]
    >>> near_online = [1,2,3,4,5,6,7,8,9,10]
    >>> popular_offline =[]
    >>> popular_online = []
    >>> new,near,popular =combined((new_online,new_offline),(near_online,near_offline),(popular_online,popular_offline))
    >>> new
    [1, 2, 3, 4, 5, 6, 1, 2, 3, 4]
    >>> near
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> popular
    []
    """
    new_list = new[0][:10] if len(new[0])>=10 else (new[0]+new[1])[:10]
    near_list = near[0][:10] if len(near[0])>=10 else (near[0]+near[1])[:10]
    popular_list = popular[0][:10] if len(popular[0])>=10 else (popular[0]+popular[1])[:10]
    return new_list,near_list,popular_list
############################
#Distance Related Functions#
############################
def nearest_restaurants(coords,restaurants):
    """'Returns a List of restaurants sorted in ascending order by distance to coords.'
    >>> restaurants = [{'location':[1,1]},{'location':[0,2]},{'location':[0,.5]}]
    >>> coords = Coordinates(0,0)
    >>> near = nearest_restaurants(coords,restaurants)
    >>> near ==[{'location' : [0, .5]},{'location' : [1, 1]},{'location' : [0, 2]}]
    True
    """
    
    
    return sorted(restaurants,key=lambda restaurant: distance(coords,restaurant))
def distance(coords,restaurant):
    """'Finds distance from coords to a given restaurant.'
    >>> coords = Coordinates(1,1)
    >>> restaurant = {'location':[2,3]}
    >>> int(distance(coords,restaurant))
    248
    """
    dist= coords_dist(coords.__tuple__(),tuple(restaurant['location'])).km
    return dist
def filter_near(coords,restaurants_sorted,allowed_dist =1.5):
    """'Returns a List of all restaurants in restaurants_sorted which are within 1.5km of coords'
    >>> coords=Coordinates(1,2.5)
    >>> restaurants = [{'location':[0,.5]},{'location':[1,1]},{'location':[0,2]}]
    >>> allowed_dist = 200
    >>> near_allowed = filter_near(coords,restaurants, allowed_dist)
    >>> near_allowed == [{'location':[1,1]},{'location':[0,2]}]
    True
    """
    return list(filter(lambda restaurant: distance(coords,restaurant)<allowed_dist,restaurants_sorted))

##############################
#Popularity Related Functions#
##############################
def popular_restaurants(restaurants):
    """'Returns a List of restaurants sorted by descending popularity'
    >>> restaurants = [{'popularity':.6},{'popularity':.9},{'popularity':.8}]
    >>> popular =  (popular_restaurants(restaurants))
    >>> popular == [{'popularity':.9},{'popularity':.8},{'popularity':.6}]
    True
    """
    return sorted(restaurants,key=lambda restaurant: -1*restaurant["popularity"]) #Sorts by ascending negative popularity to achieve descending popularity.
###############################
#Launch Date Related Functions#
###############################
def new_restaurants(restaurants):
    """'Returns a List of restaurants sorted by newer->older launch_date'
    >>> restaurants = [{'launch_date':'2021-10-09'},{'launch_date':'2021-11-10'},{'launch_date':'2010-05-05'}]
    >>> new = new_restaurants(restaurants)
    >>> new == [{'launch_date':'2021-11-10'},{'launch_date':'2021-10-09'},{'launch_date':'2010-05-05'}]
    True
    """
    return sorted(restaurants,key=lambda restaurant: time_ago(restaurant["launch_date"]))
def time_ago(launch_date):
    """Returns how long ago a launch date was in seconds."""
    """
    >>> launch_date = '2020-02-10'
    >>> int(time_ago(launch_date))
    55615821
    """
    date_restaurant=datetime.strptime(launch_date,'%Y-%m-%d')
    date_curr= datetime.today()
    return (date_curr.timestamp()-date_restaurant.timestamp())
def filter_new(restaurants_sorted,months_long_ago=4):
    """'Returns a List of all restaurants in restaurants_sorted who are at most <months_long_ago> old'
    >>> restaurants = [{'launch_date':'2021-10-09'},{'launch_date':'2021-11-10'},{'launch_date':'2010-05-05'}]
    >>> restaurants = new_restaurants(restaurants)
    >>> new_filtered = filter_new(restaurants,months_long_ago=1)
    >>> new_filtered == [{'launch_date':'2021-11-10'}]
    True
    """
    months_ago_to_seconds = datetime.today().timestamp()-(datetime.today()-relativedelta(months=months_long_ago)).timestamp()
    return list(filter(lambda restaurant: time_ago(restaurant['launch_date'])<=months_ago_to_seconds,restaurants_sorted))

##########################
#Online Related Functions#
##########################
def filter_online(restaurants_sorted):
    """'Returns two Lists, one for all restaurants in restaurants_sorted that are online, and one for all that ar offline.'
    >>> restaurants = [{'name':'Mcdonalds','online':True},{'name':'foo','online':False},{'name':'bar','online':True}]
    >>> online,offline =filter_online(restaurants)
    >>> online == [{'name':'Mcdonalds','online':True},{'name':'bar','online':True}] 
    True
    >>> offline == [{'name': 'foo', 'online':False}]
    True
    """
    online = [restaurant for restaurant in restaurants_sorted if restaurant['online']]
    offline = [restaurant for restaurant in restaurants_sorted if not restaurant['online']]
    return online, offline
if DEBUG:
    import doctest
    x=doctest.testmod(verbose=True)
    

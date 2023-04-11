# Your name: Alex Chong
# Your student id: 3607 9863
# Your email: alchong@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    restaurants = {}
    cur.execute(
        "SELECT R.name, C.category, B.building, R.rating "
        "FROM restaurants R, categories C, buildings B "
        "WHERE R.category_id = C.id "
        "AND R.building_id = B.id "
    )
    for row in cur:
        name = row[0]
        inner = {}
        inner["category"] = row[1]
        inner["building"] = row[2]
        inner["rating"] = row[3]

        restaurants[name] = inner

    return restaurants

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    categories = {}
    cur.execute(
        "SELECT C.category, COUNT(C.category) "
        "FROM restaurants R, categories C "
        "WHERE R.category_id = C.id "
        "GROUP BY C.category "
        "ORDER BY COUNT(C.category) DESC "
    )
    for row in cur:
        categories[row[0]] = int(row[1])

    names = []
    counts = []
    for category, count in categories.items():
        names.append(category)
        counts.append(count)
    plt.style.use("ggplot")
    plt.barh(names, counts, color="blue")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.title("Types of Restaurant on South University Ave")
    plt.show()

    return categories

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    restaurants = []
    cur.execute(
        "SELECT R.name "
        "FROM restaurants R, buildings B "
        "WHERE R.building_id = B.id "
        "AND B.building = ? "
        "ORDER BY R.rating DESC ",
        (building_num, )
    )
    for row in cur:
        restaurants.append(row[0])
    return restaurants

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute(
        "SELECT C.category, AVG(R.rating) "
        "FROM restaurants R, categories C "
        "WHERE R.category_id = C.id "
        "GROUP BY C.category "
        "ORDER BY AVG(R.rating) "
    )
    categories = []
    avg_ratings = []
    for row in cur:
        categories.append(row[0])
        avg_ratings.append(row[1])
    
    cur.execute(
        "SELECT B.building, AVG(R.rating) "
        "FROM restaurants R, buildings B "
        "WHERE R.building_id = B.id "
        "GROUP BY B.building "
        "ORDER BY AVG(R.rating) "
    )

    buildings = []
    avg_b = []
    for row in cur:
        buildings.append(str(row[0]))
        avg_b.append(row[1])

    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.barh(categories, avg_ratings, color="blue")
    ax1.set_ylabel("Categories")
    ax1.set_xlabel("Ratings")
    ax1.set_title("Average Restaurant Ratings by Category")

    ax2.barh(buildings, avg_b, color="blue")
    ax2.set_ylabel("Buildings")
    ax2.set_xlabel("Ratings")
    ax2.set_title("Average Restaurant Ratings by Building")

    plt.show()
    return [(categories[-1], avg_ratings[-1]),(int(buildings[-1]), avg_b[-1])]

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)

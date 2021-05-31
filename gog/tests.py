from selenium import webdriver
import time
import unittest
import os
from assertpy import assert_that

from wishlistPage import WishlistPage
from wishlistPage import Filters
from wishlistPage import Sorter
from wishlistPage import Cart

class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(f"C:\\Users\\{os.getlogin()}\\Desktop\\gog\\drivers\\chromedriver.exe")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()


    def test_01_use_search_bar(self):
        game_title = "BIOMUTANT"
        wishlist = WishlistPage(self.driver)

        wishlist.get_wishlist_page()
        wishlist.search_bar(game_title)
        time.sleep(0.5)
        found_game_title = wishlist.first_record_title()

        assert_that(game_title).is_equal_to(found_game_title).described_as("Searched game title should match with search bar input.")


    def test_02_filter_games(self):
        game_title = "Siege of Avalon: Anthology"   
        filters = Filters(self.driver)
       
        filters.get_wishlist_page()
        filters.select_genre("57")
        filters.select_system("windows")
        filters.select_language("pl")
        filters.select_features("1")
        filters.select_top_price("2")

        time.sleep(0.5) #short sleep due to page going too fast but same selector is available for different games
        found_game_title = filters.first_record_title()

        assert_that(game_title).is_equal_to(found_game_title).described_as("Searched game title should be adequate to applied filters.")
        
    def test_03_sort_games(self):
        game_title = "Cyberpunk 2077"
        sorter = Sorter(self.driver)

        sorter.get_wishlist_page()
        sorter.choose_sorter("UserReviews")

        time.sleep(0.5)
        found_game_title = sorter.first_record_title()

        assert_that(game_title).is_equal_to(found_game_title).described_as("First displayed game title should be adequate to applied sort.")


    def test_04_add_and_remove_game_from_cart(self):
        game_title = "Heroes of Might and Magic® 3: Complete"
        empty_cart_msg = "Odkryj niezwykłe gry i oferty."
        cart = Cart(self.driver)

        cart.add_game_to_cart_by_gogid("1207658787")
        self.driver.refresh() #refresh due to issue where cart content is empty after first addition
        cart.open_cart()
        added_game = cart.first_record_title()
        
        assert_that(game_title).is_equal_to(added_game).described_as("Game in cart should equal added game.")

        cart.remvoe_first_record()
        time.sleep(0.5)
        empty_cart_displayed_msg = cart.empty_cart_msg()

        assert_that(empty_cart_msg).is_equal_to(empty_cart_displayed_msg).described_as(f"Empty cart message should be 'Odkryj niezwykłe gry i oferty.'")


    def test_05_go_to_game_page(self):
        game_url = "https://www.gog.com/game/prince_of_persia_the_sands_of_time"
        wishlist = WishlistPage(self.driver)

        wishlist.get_wishlist_page()
        wishlist.open_game_main_page("Prince of Persia")
        current_url = self.driver.current_url

        assert_that(game_url).is_equal_to(current_url).described_as(f"URL of the game should lead to its page.")


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()

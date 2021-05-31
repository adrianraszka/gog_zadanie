
class WishlistPage:

    def __init__(self, driver):
        self.driver = driver

        self.base_page = "https://www.gog.com/u/saja9/wishlist"
        self.search_bar_cs = 'input[ng-model="search.term"]'
        self.first_record_cs = 'span[class="product-title__text"]'
        self.add_to_cart_cs = 'div[ng-click="productCtrl.addToCart()"'
    
    
    def get_wishlist_page(self):
        self.driver.get(self.base_page)


    def search_bar(self, game_title):
        self.driver.find_element_by_css_selector(self.search_bar_cs).clear()
        self.driver.find_element_by_css_selector(self.search_bar_cs).send_keys(game_title)


    def first_record_title(self):
        return self.driver.find_element_by_css_selector(self.first_record_cs).text


    def add_game_to_cart_by_gogid(self, gog_product):
        """1207658787 - H3"""
        self.gog_product_cs = f'div[gog-product="{gog_product}"'
        choosen_game = self.driver.find_element_by_css_selector(self.gog_product_cs)
        choosen_game.find_element_by_css_selector(self.add_to_cart_cs).click()


    def open_game_main_page(self, title):
        self.driver.find_element_by_partial_link_text(title).click()


class Filters(WishlistPage):

    def __init__(self, driver):
        super().__init__(driver)

        self.genre_filter_cs = 'div[ng-controller*="accountCategoryFiltersCtrl"]'
        self.system_filter_cs = 'div[ng-controller*="accountSystemFiltersCtrl"]'
        self.langauge_filter_cs = 'div[ng-controller*="accountLanguageFiltersCtrl"]'
        self.feature_filter_cs = 'div[ng-controller*="accountModeFiltersCtrl"]'
        self.price_filter_cs = 'div[ng-controller*="accountPriceFiltersCtrl"]'


    def select_genre(self, genre_id):
        """57 - RPG"""
        self.genre_id_cs = f'div[ng-click="category.toggle(\'{genre_id}\')"'
        self.driver.find_element_by_css_selector(self.genre_filter_cs).click()
        self.driver.find_element_by_css_selector(self.genre_id_cs).click() #57 - RPG


    def select_system(self, system):
        self.system_cs = f'div[ng-click="system.toggleGroup(\'{system}\')"]'
        self.driver.find_element_by_css_selector(self.system_filter_cs).click()
        self.driver.find_element_by_css_selector(self.system_cs).click()


    def select_language(self, language):
        self.language_cs = f'div[ng-click="language.toggle(\'{language}\')"]'
        self.driver.find_element_by_css_selector(self.langauge_filter_cs).click()
        self.driver.find_element_by_css_selector(self.language_cs).click()


    def select_features(self, feautre_id):
        """1 - Single Player"""
        self.feautre_cs = f'div[ng-click="mode.toggle(\'{feautre_id}\')"]'
        self.driver.find_element_by_css_selector(self.feature_filter_cs).click()
        self.driver.find_element_by_css_selector(self.feautre_cs).click()


    def select_top_price(self, price_id):
        """2 - up to 40 pln"""
        self.price_cs = f'div[ng-click="price.selectOne(\'{price_id}\')"]'
        self.driver.find_element_by_css_selector(self.price_filter_cs).click()
        self.driver.find_element_by_css_selector(self.price_cs).click()


class Sorter(WishlistPage):
    
    def __init__(self, driver):
        super().__init__(driver)

        self.sorter_cls = "header__dropdown"

    
    def choose_sorter(self, sort):
        """UserReviews/Title/DateAdded"""
        self.choosen_sorter_cs = f'span[ng-click="sorting.sortBy{sort}()"]'
        self.driver.find_element_by_class_name(self.sorter_cls).click()
        self.driver.find_element_by_css_selector(self.choosen_sorter_cs).click()
        

class Cart(WishlistPage):
    
    def __init__(self, driver):
        super().__init__(driver)

        self.cart_cs = 'div[ng-controller*="menuCartCtrl"]'
    

    def open_cart(self):
        self.driver.find_element_by_css_selector(self.cart_cs).click()


    def first_record_title(self):
        self.game_in_cart_cs = 'div[class="menu-product__title menu-cart-item__title"]'
        return self.driver.find_element_by_css_selector(self.game_in_cart_cs).text


    def remvoe_first_record(self):
        self.remove_cs = 'span[hook-test="cartRemove"]'
        self.driver.find_element_by_css_selector(self.remove_cs).click()


    def empty_cart_msg(self):
        self.empty_cart_cls = "menu-cart-empty__description"
        return self.driver.find_element_by_class_name(self.empty_cart_cls).text
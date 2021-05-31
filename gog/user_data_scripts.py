from requests_html import HTMLSession
import re
import os
import csv
import json

class UserData:

    gog = "https://www.gog.com/"
    gog_u = "https://www.gog.com/u/"
    session = HTMLSession()

    def __init__(self, username):
        self.username = username

        self.download_avatar()
        self.download_wishlist()
        print(f"Estimated games price for user {self.username} is: {self.estimate_games_price()}PLN")
        self.create_json_wishlist()


    def download_avatar(self):
        try:
            user_profile_page = self.session.get(f"{self.gog_u}{self.username}").text
            match = re.search(r"https://images.gog.com/.*_prof_avatar_140x140.jpg", user_profile_page).group(0)
            response = self.session.get(match)
            avatar = open(f"C:\\Users\\{os.getlogin()}\\Desktop\\gog\\{self.username}_avatar140x140.png", "wb")
            avatar.write(response.content)
            avatar.close()
        except Exception as e :
            print(f"Failed to download avatar for user: {self.username}", e)
            
        downloaded_avatars = os.listdir(f"C:\\Users\\{os.getlogin()}\\Desktop\\gog\\")
        if f"{self.username}_avatar140x140.png" not in downloaded_avatars:
            raise FileNotFoundError(f"User's: {self.username} avatar was not downloaded.")

    
    def get_wishlist_source(self):
        user_wishlist_page = self.session.get(f"{self.gog_u}{self.username}/wishlist")
        code = user_wishlist_page.status_code
        if code == 200:
            user_wishlist_page.html.render()
            all_games = user_wishlist_page.html.find(".product-state-holder")
            return all_games
        else:
            raise Exception(f"Wrong return status! Status code: {code}")
    

    def download_wishlist(self):
        try:
            all_games = self.get_wishlist_source()
            with open(f"C:\\Users\\{os.getlogin()}\\Desktop\\gog\\{self.username}_wishlist.csv", "a", encoding="UTF8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'NAME', 'PRICE'])
                for game in all_games:
                    game_id = game.attrs["gog-product"]
                    game_name = game.find(".product-title__text")[0].text
                    game_price = game.find("._price ")[0].text
                    writer.writerow([game_id, game_name, game_price])
        except Exception as e:
            print(f"Failed to download wishlist for user: {self.username}.", e)

    
    def estimate_games_price(self):
        price = 0.00
        all_games = self.get_wishlist_source()
        for game in all_games:
            game_price = float(game.find("._price ")[0].text)
            price += game_price
        return float("{:.2f}".format(price))


    def create_json_wishlist(self):
        wishlist_dict = []
        all_games = self.get_wishlist_source()

        for game in all_games:
            single_game_wish = {"id": "", "name": "", "price": ""}
            game_id = {"id": game.attrs["gog-product"]}
            game_name = {"name": game.find(".product-title__text")[0].text}
            game_price = {"price": game.find("._price ")[0].text}

            single_game_wish.update(game_id)
            single_game_wish.update(game_name)
            single_game_wish.update(game_price)

            wishlist_dict.append(single_game_wish)
        
        with open(f"C:\\Users\\{os.getlogin()}\\Desktop\\gog\\{self.username}_wishlist.json", "w", encoding="UTF8", ) as f:
            json.dump(wishlist_dict, f, ensure_ascii=False)


if __name__ == "__main__":
    user1 = UserData("saja9")


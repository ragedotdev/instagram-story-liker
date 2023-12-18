import time
import json
import random
from typing import Tuple, List
from config import *
from instagrapi import Client
from instagrapi.exceptions import ClientLoginRequired, PleaseWaitFewMinutes

class StoryLiker:
    def __init__(self):
        self.client = Client(proxy=DEFAULT_PROXY)
        self.target_id = None
        self.cursor = None
        self.target = None
        self.done = 0

    def random_delay(self, small = False):
        if small:
            time.sleep(random.uniform(1.5, 3.5))
        else:
            time.sleep(random.uniform(3.5, 5.89))

        
    def login(self):
        #clear_console()
        print(Fore.LIGHTMAGENTA_EX+"* LOGIN *"+Fore.RESET)
        username = input("> Username: ")
        old_acc : Account = root.get_account(username)
        if not old_acc:
            password = input("> Password: ")
            print("Logging in...")
            self.client.login(username, password)
            root.add_account(username, password, self.client.get_settings())
        else:
            password = old_acc.password
            self.client.set_settings(json.loads(old_acc.credentials))
            self.client.username = old_acc.username
            self.client.password = old_acc.password
        
        print("Logged In!")
        time.sleep(1)
        

    def choose_target(self):
        target_id = None
        print()
        print(Fore.LIGHTMAGENTA_EX+"* TARGET SELECTION *"+Fore.RESET)
        target = input("> Account to scrape followers from: ")
        response = self.client.search_users_v1(target, 50)
        for user in response:
            if user.username == target.lower():
                target_id = user.pk
        
        return target, target_id

    def choose_settings(self):
        print()
        print(Fore.LIGHTMAGENTA_EX+"* SETTINGS *"+Fore.RESET)
        like_count = int(input("> Select how many stories to like: "))
        like_all_stories = input("> Like all user stories? (Y/N): ")
        close_friends = input("> Add user to close friends? (Y/N): ")

        like_all_stories = True if like_all_stories.lower() == 'y' else False
        close_friends = True if close_friends.lower() == 'y' else False
        return like_count, like_all_stories, close_friends

    def get_users_chunk(
        self, user_id: str, max_amount: int = 0, max_id: str = ""
    ) -> Tuple[List[User], str]:
        unique_set = set()
        users = []
        result = self.client.private_request(
                f"friendships/{user_id}/followers/",
                params={
                    "max_id": max_id,
                    "count": max_amount,
                    "rank_token": self.client.rank_token,
                    "search_surface": "follow_list_page",
                    "query": "",
                    "enable_groups": "true",
                },
            )
        for user in result["users"]:
            user = extract_user_short(user)
            if user.pk in unique_set:
                continue
            unique_set.add(user.pk)
            users.append(user)
        max_id = result.get("next_max_id")
        return users, max_id

    
    def start(self, target : str, target_id : str, like_count : int, like_all_stories = False,priv_story = False):
        clear_console()
        done = 0
        max_id = True
        print(f'Logged In User: {Back.LIGHTGREEN_EX}{Fore.WHITE}[{self.client.username}]{Fore.RESET}{Back.RESET} | Total Likes: {Back.LIGHTYELLOW_EX}{Fore.WHITE}[{like_count}]{Fore.RESET}{Back.RESET} | Target Account: {Back.LIGHTBLUE_EX}{Fore.WHITE}{target}{Fore.RESET}{Back.RESET}\n')
        while max_id and done < like_count:
            if max_id is True:
                max_id = ""
            logs = root.get_account_logs(self.client.username)
            #input(len(logs))
            users,max_id = self.get_users_chunk(target_id, like_count, max_id)
            print(Fore.LIGHTMAGENTA_EX+f"\nFetched {len(users)} followers | Total Liked: {done}/{like_count}\n"+Fore.RESET)
            for user in users:
                status = f'Story: {Fore.GREEN+"(YES)"+Fore.RESET if user.latest_reel_media else Fore.RED+"(NO)"+Fore.RESET} | [{user.username}]'
                print(status)
                if user.latest_reel_media:
                    stories = self.client.user_stories_v1(user.pk)
                    self.random_delay(small=True)
                    if not like_all_stories:
                        stories = stories[:1]

                    for story in stories:
                        if done >= like_count:
                            break
                        if story.id in logs:
                            print(Fore.LIGHTRED_EX+f"> Skipping story {story.user.username} (Already Liked)"+Fore.RESET)
                            continue
                        self.client.story_seen([story.id])
                        self.random_delay(small=True)
                        self.client.story_like(story.id)
                        root.add_account_log(self.client.username, str(story.id))
                        done+=1
                        print(Fore.LIGHTYELLOW_EX+f'\n[{done}] Story liked -> {story.user.username}'+Fore.RESET)
                        if priv_story:
                                self.client.close_friend_add(user.pk)
                                print(f'[{done}] User: {user.username} -> Added to close friends list')
                        #print(f'Logged In User: {Back.LIGHTGREEN_EX}[{self.client.username}]{Back.RESET} | Stories Liked: {done} | Target Account: {target}')
                        self.random_delay()
            
                
        input(Fore.YELLOW+f"\n[!] Story liking for {self.client.username} has finished! Press enter to return to main menu."+Fore.RESET)        

        

    def run(self):
        while True:
            clear_console()
            self.login()
            target, target_id = self.choose_target()
            like_count, like_all_stories, priv_story = (self.choose_settings())
            self.start(target, target_id, like_count, like_all_stories, priv_story)


if __name__ == '__main__':
    liker = StoryLiker()
    try:
        liker.run()
    except Exception as e:
        if type(e) in [ClientLoginRequired, PleaseWaitFewMinutes]:
            root.delete_account(liker.client.username)
        print("Error: " + str(e))
        print(liker.client.last_json)
        input("Press enter to exit program...")

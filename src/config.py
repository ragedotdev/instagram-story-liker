import os
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl
from dotenv import load_dotenv
from database.models import Account
from database.access import root
from colorama import init, Fore, Back
init()
load_dotenv()


class User(BaseModel):
    model_config = ConfigDict(
        coerce_numbers_to_str=True
    )  # (jarrodnorwell) fixed pk issue

    pk: str
    username: Optional[str] = None
    full_name: Optional[str] = ""
    profile_pic_url: Optional[HttpUrl] = None
    profile_pic_url_hd: Optional[HttpUrl] = None
    is_private: Optional[bool] = None
    # is_verified: bool  # not found in hashtag_medias_v1
    latest_reel_media: Optional[int] = None

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)

def extract_user_short(data):
    """Extract User Short info"""
    data["pk"] = data.get("id", data.get("pk", None))
    assert data["pk"], f'User without pk "{data}"'
    return User(**data)


DEFAULT_PROXY = os.getenv('DEFAULT_PROXY')

BANNER = Fore.BLUE+"""
 (                         (                    
 )\ )    )                 )\ )        )        
(()/( ( /(      (    (    (()/( (   ( /(    (   
 /(_)))\()) (   )(   )\ )  /(_)))\  )\())  ))\  
(_)) (_))/  )\ (()\ (()/( (_)) ((_)((_)\  /((_) 
/ __|| |_  ((_) ((_) )(_))| |   (_)| |(_)(_))   
\__ \|  _|/ _ \| '_|| || || |__ | || / / / -_)  
|___/ \__|\___/|_|   \_, ||____||_||_\_\ \___|  
                     |__/                       


"""+Fore.RESET

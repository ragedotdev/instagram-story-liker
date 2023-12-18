import json
from typing import Optional, List, Union
from .engine import get_db
from .models import Account, Log

class AccountDAO:

    def __init__(self):
        pass


    def get_account(self, username: str) -> Optional[Account]:
        with get_db() as db:
            acc = db.query(Account).filter(Account.username == username.lower()).first()
        return acc
    
    def get_all_account(self) -> List[Account]:
        with get_db() as db:
            accs = db.query(Account).all()
        return accs

    def add_account(self, username : str, password : str, credentials : dict):
        with get_db() as db:
            new_acc = Account(username=username.lower(), password=password, credentials=json.dumps(credentials))
            db.add(new_acc)
            db.commit()
    
    def add_account_log(self, username : str, log : str):
        log_string = f"{username}_{log}"
        with get_db() as db:
            new_log = Log(username=username.lower(), log_string=log_string, log=log)
            db.add(new_log)
            db.commit()
    
    def get_account_logs(self, username : str, raw = True) -> List[Optional[Union[str, Log]]]:
        with get_db() as db:
            logs = db.query(Log).filter(Log.username == username.lower()).all()
        if raw:
            return [str(log.log) for log in logs]
        return logs

    def delete_account(self, username : str):
        acc = self.get_account(username.lower())
        with get_db() as db:
            db.delete(acc)
            db.commit()
    

root = AccountDAO()
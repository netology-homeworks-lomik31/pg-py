from db import DB
import json as JSON

with open("./config.json", encoding = "utf-8") as config:
    config = JSON.load(config)

db = DB(config["host"], config["database"], config["user"], config["password"])

db.newUser("123", "456", "123456@mail.com", (1488, 1337))

print(db.searchUser("123"))
print(db.searchUser(phone = 1488))
db.addUserPhone(1, (228, 164421))
db.delPhone(1, 228)
db.editUser(1, firstName="111", phone=(164421, 164422), email="111456@mail.com")
db.delUser(1)

db.close()
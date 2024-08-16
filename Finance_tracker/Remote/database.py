from pymongo import MongoClient
from data_entry import get_amt, get_date, get_category, get_description

class mongo:
    port = MongoClient("mongodb+srv://Admin:Admin@cluster0.1owdo.mongodb.net/")
    db = port["Finance_Calculator"]

class Function:
    from data_entry import get_amt, get_date, get_category, get_description

    col = mongo.db["Records"]


    def add(self, date, amount, category, description):
        self.col.insert_one({"date": date, "amount": amount, "category": category,"description":description})
    
    
    def update_entry(self, date):
        for i in self.col.find({"date":date}):
            print(f"Date: {i['date']}, Amount: {i['amount']}, Category: {i['category']}, Description: {i['description']}")
        while True:
            print("""What do you want to update?
            1. Amount
            2. Category
            3. Description
            4. All of the above
            0. Return""")
            choice = input("Enter your choice: ")
            if choice == "1":
                amt = get_amt()
                self.col.update_one({"date":date},{'$set':{'amount':amt}})
            elif choice == "2":
                cat = get_category()
                self.col.update_one({"date":date},{'$set':{'category':cat}})
            elif choice == "3":
                desc = get_description()
                self.col.update_one({"date":date},{'$set':{'description':desc}})
            elif choice == "4":
                amt = get_amt()
                cat = get_category()
                desc = get_description()
                self.col.update_one({"date":date},{'$set':{'amount':amt,'category':cat,'description': desc}})
            elif choice == "0":
                break
            else:
                print("Invalid choice")

    def delete_entry(self, date):
        self.col.delete_one({"date":date})
    
    def display(self):
        count = self.col.count_documents({})
        print(f"Total number of entries = {count}")
        for i in self.col.find():
            print(f"Date: {i['date']}, Amount: {i['amount']}, Category: {i['category']}, Description: {i['description']}")
    


def DBrun():
    DB = Function()
    while True:
        print("""What whould you like to do?
              1. Add a new entry
              2. Update an existing entry
              3. Delete an existing entry
              4. Display all entries
              0. Return
              """)
        
        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter the date: ")
            amount = get_amt()
            category = get_category()
            description = get_description()
            DB.add(date, amount, category, description)
            print("Entry added successfully")

        elif choice == "2":
            date = get_date("Enter the date of the entry you want to update: ")
            DB.update_entry(date)
            print("Entry updated successfully")

        elif choice == "3":
            date = input("Enter the date of the entry you want to delete: ")
            DB.delete_entry(date)
            print("Entry deleted successfully")

        elif choice == "4":
            DB.display()

        elif choice == "0":
            print("Returning....")
            break
        else:
            print("Invalid input. Enter choice from 1-4. ")
        
if __name__=="__main__":
    DBrun()

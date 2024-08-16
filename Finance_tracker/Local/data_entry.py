from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I":"Income", "E":"Expense"}

def get_date(prompt, allow_default = False):
    date = input(prompt)
    if allow_default and not date:
        return datetime.today().strftime(date_format)
    try:
            valid_date = datetime.strptime(date,date_format)
            return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default = False)
        
def get_amt():
    try:
        amount = float(input("Enter amount: "))
        if amount<=0:
            raise ValueError("Amount must be a non negative and non-zero value")
    except ValueError as e:
        print(e)
        return get_amt()
    return amount

def get_category():
    category = input("Enter category ('I' for Income and 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    else:
        print("Invalid category. Please enter 'I' for Income and 'E' for Expense.")
        return get_category()

def get_description():
    return input("Enter a description (Optional): ")
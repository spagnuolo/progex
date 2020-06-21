'''Methods for all our main queries'''
import sqlalchemy

ENGINE = sqlalchemy.create_engine('sqlite:///src/groceries.db')

def is_scancode(scancode):
    '''Searching for Existing link'''
    result = ENGINE.execute('''
        Select product_id
        from ScannCodes
        where code = ?
    ''', (scancode))

    answer = result.fetchall()

    # List is empty. There is no such scancode.
    if not answer:
        return False

    # Found scancode.
    return True
def get_product_id(scancode):
    result = ENIGNE.execute('''Select product_id From ScannCodes where code = ?''', (scancode))
    answer = result.scalar()
    if not answer:
        return -1
    return answer

def link_code_product(scancode, product_id):
    result = ENGINE.execute('''Insert Into ScannCodes(code, product_id) Values(?,?); ''',(scancode, product_id))
    

def new_product(name, product_category_id,description):
    result = ENGINE.execute('''Insert Into Product(name, product_category,description) Values(?,?,?); ''',(name, product_category_id,description))
    result = ENGINE.execute('''Select id From Product Where name = ? and description = ? Order by id desc''', (name,description))
    answer = result.scalar()   
    return answer

def new_product_category(name):
    result = ENGINE.execute('''INSERT INTO Product_Category(name) VALUES(?) ''',(name))
    result = ENGINE.execute('''Select id From Product_Category Where name = ? Order by id desc''', (name))
    answer = result.scalar()   
    return answer
def new_household(name):
    result = ENGINE.execute('''INSERT INTO Household(name) VALUES(?) ''',(name))
    result = ENGINE.execute('''Select id From Household Where name = ? Order by id desc''', (name))
    answer = result.scalar()
    return answer
    
def example():
    '''An Example on how to use sqlalchemy with simple queries'''
    result = ENGINE.execute('select * from user')
    answer = result.fetchall()
    first_ans = answer[0]

    print(first_ans) # returns tuple
    print(first_ans.keys())
    print(first_ans.values()) # returns list

if __name__ == '__main__':
    example()

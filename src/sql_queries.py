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
    result = ENGINE.execute('''Select product_id From ScannCodes where code = ?''', (scancode))
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
    result = ENGINE.execute('''INSERT INTO Product_Category(name) VALUES(?); ''',(name))
    result = ENGINE.execute('''Select id From Product_Category Where name = ? Order by id desc''', (name))
    answer = result.scalar()   
    return answer
def new_household(name):
    result = ENGINE.execute('''INSERT INTO Household(name) VALUES(?); ''',(name))
    result = ENGINE.execute('''Select id From Household Where name = ? Order by id desc''', (name))
    answer = result.scalar()
    return answer

def get_product_category_id_byname(name):
    result = ENGINE.execute('''Select id From Product_Category Where name = ? ''',(name))
    answer = result.scalar()
    if not answer:
        return -1
    return answer
def get_product_name(product_id):
    result = ENGINE.execute('''Select name From Product Where id = ? ''',(product_id))
    answer = result.scalar()
    return answer
#inventory
def get_inventory(household_id):
    result = ENGINE.execute('''Select i.id as id , p.name as Name, c.name as Category,i.due_date From Item i,Product p,Product_Category c Where household_id = ? and i.product_id = p.id and p.product_category = c.id ''',(household_id))
    answer = result.fetchall()
    return answer

def get_inventory_by_product(household_id):
    result = ENGINE.execute('''Select p.name as Name, c.name as Category,Count(i.id) as Amount From Item i,Product p,Product_Category c Where household_id = ? and i.product_id = p.id and p.id = c.product_id Group By i.id''',(household_id))
    answer = result.fetchall()
    return answer
    
def get_invetory_for_Recipe(household_id,recipe_id):
    result = ENGINE.execute('''Select p.name as Name, c.name as Category,Count(i.id) as Amount_stored, r.amount as Amount_needed From Product p,Product_Category c, RecipeIngredients r Left Join Item i on p.id = i.product_id
    Where household_id = ? and p.id = c.product_id and p.id = r.product_id and r.recipe_id = ? Group By p.id''',(household_id, recipe_id))
    answer = result.fetchall()
    return answer	    
#item
def new_item(household_id, product_id, due_date):
    result = ENGINE.execute('''INSERT INTO Item(household_id, product_id, due_date) VALUES(?,?,?); ''',(household_id,product_id,due_date))


#Recipe
def new_recipe(name, instructions, dificulty, time):
    result = ENGINE.execute('''INSERT INTO Recipe(name, instructions, dificulty, time) VALUES(?,?,?,?); ''',(name, instructions, dificulty, time))
    result = ENGINE.execute('''Select id From Recipe Where name = ? and instructions = ? Order by id desc''', (name,instructions))
    answer = result.scalar()   
    return answer
    
def get_all_recipe(recipe_id):
    result = ENGINE.execute('''Select * From Recipe where id = ?''', (recipe_id))
    answer = result.fetchall()
    return answer

def set_name_recipe(recipe_id, name):
    result = ENGINE.execute('''Update Recipe Set name=? where id = ? ''', (name,recipe_id))
def set_instructions_recipe(recipe_id, instructions):
    result = ENGINE.execute('''Update Recipe Set instructions=? where id = ?''', (instructions,recipe_id))
def set_dificulty_recipe(recipe_id, dificulty):
    result = ENGINE.execute('''Update Recipe Set dificulty=? where id = ?''', (dificulty,recipe_id))
def set_time_recipe(recipe_id, time):
    result = ENGINE.execute('''Update Recipe Set time=? where id = ?''', (time,recipe_id))
#deletes
def delete_item(item_id):
    result = ENGINE.execute('''Delete From Item Where id = ? ''',(item_id))

def delete_product(product_id):
    result = ENGINE.execute('''Delete From ScannCodes Where product_id = ? ''',(product_id))
    result = ENGINE.execute('''Delete From RecipeIngredients Where product_id = ? ''',(product_id))
    result = ENGINE.execute('''Delete From Item Where product_id = ? ''',(product_id))

def delete_recipe(recipe_id):
    result = ENGINE.execute('''Delete From RecipeIngredients Where recipe_id = ? ''',(recipe_id))
    result = ENGINE.execute('''Delete From Recipe Where id = ? ''',(recipe_id))

def delete_scancode(scancode):
    result = ENGINE.execute('''Delete From ScannCodes Where code = ? ''',(scancode))

def delete_recipe_ingredients(recipe_id, product_id):
    result = ENGINE.execute('''Delete From RecipeIngredients Where recipe_id = ? and product_id = ?''',(recipe_id, product_id))

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

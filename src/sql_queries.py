'''Methods for all our main queries'''
import sqlalchemy

ENGINE = sqlalchemy.create_engine('sqlite:///src/groceries.db')

def is_scancode(scancode):
    '''Searching for Existing link'''
    result = ENGINE.execute('''
        Select Product_ID
        from ScannCodes
        where code = ?
    ''', (scancode))

    answer = result.fetchall()

    # List is empty. There is no such scancode.
    if not answer:
        return False

    # Found scancode.
    return True


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

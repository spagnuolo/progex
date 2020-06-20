'''Methods for all our main queries'''
import sqlalchemy

ENGINE = sqlalchemy.create_engine('sqlite:///groceries.db')

def is_scancode(scancode):
    '''Searching for Existing link'''
    result = ENGINE.execute('''
        Select Product_ID
        from ScannCodes
        where code = ?
    ''', (scancode))

    # Found scancode.
    if result.fetchall()[0] is not None:
        return True

    # There is no such scancode.
    return False


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

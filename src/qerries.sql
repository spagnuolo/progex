For Scanner:
//Searching for Existing link
	Select Product_ID
	from ScannCodes
	where code = scanned_code
	
//Createing Scann Code Entry
	Insert Into ScannCodes(code, product_id)
	Values(scanned_code, product_id)
//Creating Item Entry 
	Insert Into Item(product_id, DueDate, houshold_id )
	Values(product_id, DueDate,'household id of the acitve user')
//Deleting Item Entry based on scanncode
	Delete from Item
	where Item.id =(
	Select Item.id
	From Item i, Product p, ScannCodes s
	Where i.product_id = p.id and p.id = s.product_id and
		s.code = 'scanned_code' and i.household_id = 'household id of the acitve user'  )
		
For Overview of the Invetory:

	Select i.id, i.duedate, p.name,c.name
	From Item i, Product p, Product_Category c, Household h
	where i.Product_id = p.id and p.product_category = c.id and i.household_id = 'household id of the acitve user'
	Order by i.id 
	//Furter modifiacation neccesary for diffrent fillters
	
For Overview of the Recipes/Recipe Book
	Select r.id, r.name, r.discritption
	From Recipe r
	//Furter modifiacation neccesary for diffrent fillters
	
For Detailed view of a Recipe:
	Select r.id, r.name, r.description, r.instructions
	from Recipe r
	Where r.id == id_of_the_selected
	
	/returns all ingrediants of the Recipe with the amount in stock
	Select avalablity.name, avalablity.count
	From Recipe r, Ingredients d, (Select p.id as id, p.name as name, count(Item.id) as count
					from Product p
					right join Item on p.id = Item.product_id
					where i.household_id = 'household id of the acitve user'
					group by p.id					
					) as avalablity
	Where r.id == d.Recipe_id and p.id == d.product_id and 
		d.product_id = avalablity.id
		

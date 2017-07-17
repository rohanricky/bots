import sqlite3

class DB:

	def __init__(self,dbname="bots.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	def setup(self):
		cmd = "CREATE TABLE IF NOT EXISTS items (description text)"
		self.conn.execute(cmd)
		self.conn.commit()

	def add_item(self,item_name):
		cmd = "INSERT INTO items (description) VALUES (?)"
		arg = (item_name, )
		self.conn.execute(cmd,arg)
		self.conn.commit()

	def delete_item(self,item_name):
		cmd ="DELETE FROM items WHERE description= (?)"
		arg = (item_name, )
		self.conn.execute(cmd,arg)
		self.conn.commit()

	def delete_all(self):
		cmd="DELETE FROM items WHERE description > -1;"
		self.conn.execute(cmd)
		self.conn.commit()

	def items_list(self):
		cmd = "SELECT description FROM items"
		return [x[0] for x in self.conn.execute(cmd)]


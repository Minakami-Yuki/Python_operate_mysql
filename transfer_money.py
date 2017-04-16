import pymysql

class transfer_money(object):
	def __init__(self, conn):
		self.conn = conn
	
	def transfer(self, source_id, target_id, money):
		try:
			self.check_account_availiable(source_id, target_id)
			self.have_enough_money(source_id, money)
			self.reduce_money_and_add_money(source_id, target_id, money)
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()
			raise e
	
	def check_account_availiable(self, source_id, target_id):
		cursor = self.conn.cursor()
		try:
			sql = "select * from account where userid=%s" % source_id
			cursor.execute(sql)
			result = cursor.fetchall()
			#print(result)
			if len(result) != 1:
				raise Exception("ID为%s的账号不存在" % source_id)
			sql = "select * from account where userid=%s" % target_id
			cursor.execute(sql)
			result = cursor.fetchall()
			#print(result)
			if len(result) != 1:
				raise Exception("ID为%s的账号不存在" % target_id)
		finally:
			cursor.close()
	
	def have_enough_money(self, source_id, money):
		cursor = self.conn.cursor()
		try:
			sql = "select * from account where userid=%s and money>=%s" % (source_id, money)
			cursor.execute(sql)
			result = cursor.fetchall()
			#print(result)
			if len(result) != 1:
				raise Exception("账号%s没有足够的钱" % source_id)
		finally:
			cursor.close()
	
	def reduce_money_and_add_money(self, source_id, target_id, money):
		cursor = self.conn.cursor()
		try:
			sql = "update account set money=money-%s where userid=%s" % (money, source_id)
			cursor.execute(sql)
			#result = cursor.fetchall()
			#print(result)
			sql = "update account set money=money+%s where userid=%s" % (money, target_id)
			cursor.execute(sql)
			#result = cursor.fetchall()
			#print(result)
			print("转账成功")
		finally:
			cursor.close()


class add_account(object):
	def __init__(self, conn):
		self.conn = conn
	
	def add(self, username, userid, money):
		try:
			self.check_username_avaliable(username)
			self.add_account(username, userid, money)
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()
			raise e
		
	def check_username_avaliable(self, username):
		cursor = self.conn.cursor()
		try:
			sql = "select * from account where username='%s'" % username
			cursor.execute(sql)
			result = cursor.fetchall()
			#print(result)
			#print("执行到这里了line82")
			if len(result) == 1:
				raise Exception("用户名%s不可用" % username)
		finally:
			cursor.close()
			
	def add_account(self, username, userid, money):
		cursor = self.conn.cursor()
		try:
			sql = "insert into account(username,userid,money) values('%s',%s,%s)" %(username,userid,money)
			cursor.execute(sql)
			result = cursor.fetchall()
			if len(result) == 1:
				raise Exception("账户创建失败")
			print("创立新账户成功，请牢记账户的ID为：%s" % userid)
		finally:
			cursor.close()


class search_account(object):
	def __init__(self, conn):
		self.conn = conn
	
	def search(self, order):
				self.s_a(order)
				#self.conn.commit()
	
	def s_a(self, order):
		cursor = self.conn.cursor()
		try:
				sql = "select username from account where userid=%s" % order
				cursor.execute(sql)
				result_username = cursor.fetchall()
				if len(result_username) != 1:
					raise Exception("ID为%s的账号不存在" % order)
				for (un,) in result_username:
					print("该账户的用户名为："+str(un))
				sql = "select money from account where userid=%s" % order
				cursor.execute(sql)
				result_money = cursor.fetchall()
				#if len(result_money) != 1:
				#	raise Exception("ID为%s的账号不存在" % order)
				for (um,) in result_money:
					print("该账户的金额为："+str(um))
		finally:
				cursor.close()
	
					
class delete_account(object):
	def __init__(self, conn):
		self.conn = conn
	
	def delete(self, trid):
		self.d_a(trid)
		self.conn.commit()
	
	def d_a(self, trid):
		cursor = self.conn.cursor()
		try:
			sql = "select username from account where userid=%s" % trid
			cursor.execute(sql)
			result_username = cursor.fetchall()
			if len(result_username) != 1:
				raise Exception("ID为%s的账号不存在" % trid)
			#print("zhixingdaozheli")
			sql = "delete from account where userid=%s" % trid
			cursor.execute(sql)
			print("ID为%s的账号删除成功"%trid)
		finally:
			cursor.close()


conn = pymysql.Connect(
	host='127.0.0.1',
	port=3306,
	user='root',
	passwd='123456',
	db='bank_account',
	charset='utf8'
)

print("此程序模拟银行账户的创立（1），转账（2），查询（3）及删除（4）")
num = input("输入对应数字进行相应操作（输入0退出）:")
num = int(num)
#print(num)

userid=1

while num != 0:
	if num == 1:
		ad_account=add_account(conn)
		new_username = input("输入账户名称:")
		new_money = input("输入初始存款数额:")
		#print(new_username+" "+new_money)
		try:
			ad_account.add(new_username,userid, new_money)
		except Exception as e:
			print("出现的问题是:" + str(e))
		userid=userid+1
		
	elif num == 2:
		tr_money = transfer_money(conn)
		source_id = input("输入转出账号ID:")
		target_id = input("输入转入账号ID:")
		money = input("输入转账金额:")
		#print(source_id + " " + target_id + " " + money)
		try:
			tr_money.transfer(source_id, target_id, money)
		except Exception as e:
			print("出现的问题是:" + str(e))
	
	elif num == 3:
		s_money=search_account(conn)
		order=input("输入ID以查看指定ID账号详情:")
		#print(order)
		order=int(order)
		try:
			s_money.search(order)
		except Exception as e:
			print("出现的问题是"+str(e))
	
	elif num ==4:
		del_account=delete_account(conn)
		trid=input("输入ID删除指定账号")
		#print(trid)
		trid=int(trid)
		try:
			del_account.delete(trid)
		except Exception as e:
			print("出现的问题是"+str(e))
	
	else:
		print("请重新输入对应数字")
	num = input("输入对应数字进行相应操作（创立（1）转账（2）查询（3）删除（4）退出（0））:")
	num = int(num)
	#print(num)
	
print("Bye~")
conn.close()
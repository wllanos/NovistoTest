import pandas as pd
import sqlite3
import json


with open('config.json', 'r') as file:     config = json.load(file)

database = config['DEFAULT']['DATABASE'] 

#initializing the database connector
conn = sqlite3.connect(database)
cursor = conn.cursor()

#function to insert a register in our database receiving a class 
def insertMetric(metric):
	with conn:
		sql = 'INSERT OR IGNORE INTO metric(code,description) VALUES(?,?)'
		cursor.execute(sql,(metric.code,metric.description))
		return cursor.lastrowid

#funtion to insert multiple registers at once 
def insertValueDefinition(registers):
	with conn:
		sql = 'INSERT OR IGNORE INTO value_definition(metric_id,label,type) VALUES(?,?,?)'
		cursor.executemany(sql, registers)

#function to complete the database schema
def createValueDefinitionTable():
	with conn:
		conn.execute("""
			create table IF NOT EXISTS value_definition
			(
				id	INTEGER,
				metric_id	INTEGER NOT NULL,
				label	TEXT NOT NULL,
				type	TEXT NOT NULL,
				PRIMARY KEY(id AUTOINCREMENT),
				FOREIGN KEY(metric_id) REFERENCES metric(id)
			)
		""")

class Metric:
	def __init__(self, code, description):
		self.code = code
		self.description = description

def main():	
	createValueDefinitionTable()
	#read the csv using pandas and create a data frame
	df = pd.read_csv('resources/metrics.csv')
	#there are two registers in one row so, grouping by metric_code we will get the registers to be inserted in metric
	grouped = df.groupby('metric_code')[['metric_code','metric_description']].first()	
	#loop to insert in our database 
	for i,row in grouped.iterrows():
		code = i
		description = row['metric_description']
		metric = Metric(code,description)
		metricId = insertMetric(metric)
		#to avoid duplicating registers in value_definition table
		if metricId != 0:
			detail = df.loc[df['metric_code'] == metric.code][['value_label','value_type']]
			detail.insert(loc=0, column='metric_id', value = metricId)
			insertValueDefinition(detail.values.tolist())
			print('CSV loaded!')
	
	print('Import script completed!')
	conn.close()

if __name__ == '__main__':
	main()



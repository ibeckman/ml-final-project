import numpy as np
import os.path 
import csv

def api_info():

	nasdaq_data = []
	amex_data = []
	nyse_data = []
	nasdaq_symbols = []
	amex_symbols = []
	nyse_symbols = []
	# *** NOTE ***
	# rU refers to read - universal new line. U is necessary to get data split into lines (rows)
	cik_ticker = np.genfromtxt(fname = "cik-ticker_v2.csv", dtype = str, unpack = True, delimiter = ",")
		#print cik_ticker
	cik_ticker_dict = {}
	for i in range(1, len(cik_ticker[0])):
		cik_ticker_dict[cik_ticker[0][i]] = cik_ticker[1][i]

	cik_ticker_2 = np.loadtxt(fname = "cik_ticker.txt", dtype = str, unpack = True, delimiter = "|")
	#print cik_ticker_2
	cik_ticker_dict_2 = {}
	for i in range(1, len(cik_ticker_2[0])):
		cik_ticker_dict_2[cik_ticker_2[0][i]] = cik_ticker_2[1][i]
	with open("nasdaq.csv", "rU") as nasdaq_info:
		for line in nasdaq_info:
			arr = line.split(',')
			nasdaq_data.append(arr)
	with open("amex.csv", "rU") as amex_info:
		for line in amex_info:
			arr = line.split(',')
			amex_data.append(arr)
	with open("nyse.csv", "rU") as nyse_info:
		for line in nyse_info:
			arr = line.split(',')
			nyse_data.append(arr)
	for k in range(1, len(nasdaq_data)):
		nasdaq_symbols.append(nasdaq_data[k][0])
	nasdaq_symbols_enum = list(enumerate(nasdaq_symbols))
	for k in range(1, len(amex_data)):
		amex_symbols.append(amex_data[k][0])
	nasdaq_symbols_enum = list(enumerate(nasdaq_symbols))
	for k in range(1, len(nyse_data)):
		nyse_symbols.append(nyse_data[k][0])
	nasdaq_symbols_enum = list(enumerate(nasdaq_symbols))
	amex_symbols_enum = list(enumerate(amex_symbols))
	nyse_symbols_enum = list(enumerate(nyse_symbols))
	api_data_output = open("2006_features_test.csv", 'w')
	api_data_output.write("Identifier,CIK,Ticker,Co_name,IPO_year,Sector,Industry,Historical_Volatilities,Wikipedia_1st_Sent" +"\n")

	for year in range(2006, 2007):
		historical_volatilities = np.loadtxt(fname = str(year)+".logvol.-12.txt", dtype = str, unpack = True)
		wiki_data = []
		with open(str(year) + "_wikipedia.csv", "rU") as wiki:
			for line in wiki:
				arr = line.split(',')
				wiki_data.append(arr)
		#print wiki_data
		meta_data = []
		with open(str(year) + "_metadata.txt", "rU") as meta:
			for line in meta:
				arr = line.split()
				meta_data.append(arr)
		#print meta_data
		next_iter = False
		cik_ctr = 0
		for i in range(0, len(meta_data)):
			CIK = meta_data[i][len(meta_data[i]) - 1]
			str_cik = str(CIK)
			ticker = cik_ticker_dict.get(str_cik)
			if ticker == None:
				ticker = cik_ticker_dict_2.get(str_cik)
				if ticker == None:
					#print "I'm here"
					api_data_output.write(meta_data[i][0] + "," + str_cik + "," + " ," + " ," + " ," + " ," + " ," + str(historical_volatilities[0][i]) + "," + str(wiki_data[i+1][3]))
					cik_ctr+=1
					continue
			if ticker != None: 
				for ind, symbol in nasdaq_symbols_enum:
					if symbol == ticker:
						api_data_output.write(meta_data[i][0] + "," + str_cik + "," + ticker + "," + nasdaq_data[ind][1] + "," + nasdaq_data[ind][4] + "," + nasdaq_data[ind][5] + "," + nasdaq_data[ind][6] + "," + str(historical_volatilities[0][i]) + "," + str(wiki_data[i+1][3]))
						next_iter = True
						#print "nasdaq here!"
						cik_ctr+=1
						break
				if next_iter == True:
					next_iter = False
					continue
				for ind, symbol in amex_symbols_enum:
					if symbol == ticker:
						api_data_output.write(meta_data[i][0] + "," + str_cik + "," + ticker + "," + amex_data[ind][1] + "," + amex_data[ind][4] + "," + amex_data[ind][5] + "," + amex_data[ind][6] + "," + str(historical_volatilities[0][i]) + "," + str(wiki_data[i+1][3]) )
						next_iter = True
						#print "amex here!"
						cik_ctr+=1
						break
				if next_iter == True:
					next_iter = False
					continue
				for ind, symbol in nyse_symbols_enum:
					if symbol == ticker:
						api_data_output.write(meta_data[i][0] + "," + str_cik + "," + ticker + "," + nyse_data[ind][1] + "," + nyse_data[ind][4] + "," + nyse_data[ind][5] + "," + nyse_data[ind][6] + "," + str(historical_volatilities[0][i]) + "," + str(wiki_data[i+1][3]) )
						next_iter = True
						#print "nyse here!"
						cik_ctr+=1
						break
				if next_iter == True:
					next_iter = False
					continue
				api_data_output.write(meta_data[i][0] + "," + str_cik + "," + " ," + " ," + " ," + " ,"  + " ," + str(historical_volatilities[0][i]) + "," + str(wiki_data[i+1][3]) )
				cik_ctr+=1
				#print "sad days"
			#print (str(CIK) + " " + str(cik_ctr))
	api_data_output.close()
		# *** NOTE for nasdaq_data structure ****
		# col 0 = CIK, col 1 = NAME, col 2 = EXCHANGE, col 3 = SIC, 
		# ... col 4 = BUSINESS, col 5 = Incorporated, col 6 = IRS
		# iterate over meta data and create txts 
	return nasdaq_data

if __name__ == "__main__":
	api_info()
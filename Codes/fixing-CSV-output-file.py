import fitz
import re
import pandas as pd
import codecs



if __name__ == "__main__":

	extracted_flora_book_data = pd.DataFrame(columns = ['Genus','Epithet','Lebanon','GeneralLocation','SubLocation'])
	extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0

	
	fifth_destination_file = codecs.open("cleansed-extracted-flora-data-from-book-03.txt",encoding='utf-8')
	info_lines_list = []
	for line in fifth_destination_file:
		info_lines_list.append(line.strip())
	
		
	for line_nbr in range(len(info_lines_list)):
		genus,epithet,lebanon,location,sub_location = info_lines_list[line_nbr].split(",",4)
		
		extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0
		extracted_flora_book_data.iloc[-1]['Genus'] = genus
		extracted_flora_book_data.iloc[-1]['Epithet'] = epithet
		extracted_flora_book_data.iloc[-1]['Lebanon'] = lebanon
		extracted_flora_book_data.iloc[-1]['GeneralLocation'] = location
		extracted_flora_book_data.iloc[-1]['SubLocation'] = sub_location
		
	
	extracted_flora_book_data.to_csv("cleansed-extracted-flora-data-from-book-03.csv")	
		
			
	

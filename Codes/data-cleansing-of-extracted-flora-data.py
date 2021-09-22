import csv
import os
import codecs
import shutil
import re

if __name__ == "__main__":
	
	extracted_flora_data_from_books_list = ['extracted-flora-data-from-book-01.csv','extracted-flora-data-from-book-02.csv','extracted-flora-data-from-book-03.csv']
	
	for extract_flora_data_from_book in extracted_flora_data_from_books_list:
	
		extracted_flora_data_book_number = extracted_flora_data_from_books_list.index(extract_flora_data_from_book) + 1
         					
		first_destination_file_name = 'first-step-useful-extracted-flora-data-book-0' + str(extracted_flora_data_book_number) + '.txt'
		second_destination_file_name = 'second-step-cleansing-of-extracted-flora-data-book-0' + str(extracted_flora_data_book_number) + '.txt'
		third_destination_file_name = 'third-step-cleansing-of-extracted-flora-data-book-0' + str(extracted_flora_data_book_number) + '.txt'
		fourth_destination_file_name = 'fourth-step-arragement-of-extracted-flora-data-book-0' + str(extracted_flora_data_book_number) + '.txt'
		fifth_destination_file_name = 'fifth-step-arragement-of-extracted-flora-data-book-0' + str(extracted_flora_data_book_number) + '.txt'
		sixth_destination_file_name = 'sixth-step-arragement-of-extracted-flora-data-book-0' + str(extracted_flora_data_book_number) + '.txt'
		
		
		first_destination_file = codecs.open(first_destination_file_name,encoding='utf-8',mode="w+")
		second_destination_file = codecs.open(second_destination_file_name,encoding='utf-8',mode="w+")
		third_destination_file = codecs.open(third_destination_file_name,encoding='utf-8',mode="w+")
		fourth_destination_file = codecs.open(fourth_destination_file_name,encoding='utf-8',mode="w+")
		fifth_destination_file = codecs.open(fifth_destination_file_name,encoding='utf-8',mode="w+")
		sixth_destination_file = codecs.open(sixth_destination_file_name,encoding='utf-8', mode="w+")
	
	
		with open(extract_flora_data_from_book, newline='') as csvfile:
			extracted_flora_data = csv.DictReader(csvfile)
			for flora_data_row in extracted_flora_data:
				if (flora_data_row['Genus'] != '0' and flora_data_row['Epithet'] != '0'):
					useful_row_info = []
					useful_row_info.append(flora_data_row['Genus'].strip())
					useful_row_info.append(flora_data_row['Epithet'].strip())
					first_destination_file.write(",".join(useful_row_info) + "\n")
				

				if(flora_data_row['LebanonLocations'] != '0'):
					useful_row_info = []
					useful_row_info.append('Lebanon')				
					useful_row_info.append(flora_data_row['LebanonLocations'])
					first_destination_file.write(",".join(useful_row_info) + "\n")
							
	
		first_destination_file.close()
		first_destination_file = codecs.open(first_destination_file_name,encoding='utf-8')
		info_lines_list = []
	
		for line in first_destination_file:
			info_lines_list.append(line.strip())
	
	
		for info_line_nbr,info_line in enumerate(info_lines_list):
			if info_line.startswith('Lebanon'):
				if info_line == 'Lebanon,L.' or re.match('^.*\(.*\)\.$',info_line):
					lebanon_locations_info = info_line
			
				else:
					last_author_name_position= info_line.rfind(").")
					if last_author_name_position != -1:
						lebanon_locations_info = info_line[:last_author_name_position+2]
					else:
						lebanon_locations_info = ''	

				if lebanon_locations_info != '':
					cleaned_lebanon_locations_info = re.sub('^Lebanon,L\.\s|^Lebanon,L\.|^Lebanon,L\.\-S\.','Lebanon,',lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('\(.*?\)','',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('\'Akkar\.','#\'Akkar:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Ct\.','#Coast:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Ctlitt\.','#Littoral Coast:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Met\.','#Continental Mediterranean:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Sud\.','#South:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Me\.','#High Mountain:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Mi\.','#Lower Mountain:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Mm\.','#Medium Mountain:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('env\.','#Surroundings:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Herm\.','#Hermon:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Hem\.','#Hermon:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('A\.L\.','#Anti-Lebanon Mountains:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Dam\.','#Damascus:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Haur\.','#Hawran:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('H\.J\.','#Upper Jezire:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('J\.D\.','#Jabal al-Druze:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('K\.D\.','#Kurd Mountains:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('NLatt\.','#North of Latakia:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('St\.','#Steppes:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Sy\.','#Syrian Climat:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Ve\.','#East Mountain:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('W\.Homs\.','#West of Homs:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Beyrouth\sce\.','Beyrouth',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Beyrouth\sce\.','Beyrouth',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('NOUVELLE\sFLORE|0|1|2|3|4|5|6|7|8|9|\s.$|et\sML,\sCe\.\s|km\.','',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub(',\s|\s,',',',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub(',\s|\s,',',',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub(',,|,,,',',',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('Hem,,','#Hermon:',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub(',,',',',cleaned_lebanon_locations_info)
					cleaned_lebanon_locations_info = re.sub('\s\.\s\#','#',cleaned_lebanon_locations_info)			
					useful_row_info = []
					useful_row_info.append(cleaned_lebanon_locations_info)
					second_destination_file.write(",".join(useful_row_info) + "\n")			
			
			else:
				useful_row_info = []
				useful_row_info.append(info_line)
				second_destination_file.write(",".join(useful_row_info) + "\n")
			
		
		
		second_destination_file.close()
		second_destination_file = codecs.open(second_destination_file_name,encoding='utf-8')
		info_lines_list = []	
				
		for line in second_destination_file:
			info_lines_list.append(line.strip())
	
	
		for info_line_nbr,info_line in enumerate(info_lines_list):	
			if (not info_line.startswith('Lebanon')):
				if info_line_nbr != len(info_lines_list) - 1:
					if info_lines_list[info_line_nbr+1].startswith('Lebanon'):
						useful_row_info = []
						useful_row_info.append(info_line)
						third_destination_file.write(",".join(useful_row_info) + "\n")
				else:
					break
				
			else:
				useful_row_info = []
				useful_row_info.append(info_line)
				third_destination_file.write(",".join(useful_row_info) + "\n")
				
	
		third_destination_file.close()
		third_destination_file = codecs.open(third_destination_file_name,encoding='utf-8')
		info_lines_list = []	
		
				
		for line in third_destination_file:
			info_lines_list.append(line.strip())
	
	
		for info_line_nbr,info_line in enumerate(info_lines_list):		
			if (not info_line.startswith('Lebanon')):
				for line_nbr in range(info_line_nbr+1,len(info_lines_list)):
					info_line_internal = info_lines_list[line_nbr]
					if info_line_internal.startswith('Lebanon'):
						useful_row_info = []
						useful_row_info.append(info_line+','+info_line_internal)
						fourth_destination_file.write(",".join(useful_row_info) + "\n")			
				
					else:
						break
					
	
		current_path = os.getcwd()
		os.remove(current_path+'/'+first_destination_file_name)
		os.remove(current_path+'/'+second_destination_file_name)						
		os.remove(current_path+'/'+third_destination_file_name)
	
	
		fourth_destination_file.close()
		fourth_destination_file = codecs.open(fourth_destination_file_name, encoding='utf-8')
		info_lines_list = []	
				
	
		for line in fourth_destination_file:
			info_lines_list.append(line.strip())
	
		
		for line_nbr in range(len(info_lines_list)):
			genus,epithet,lebanon,locations = info_lines_list[line_nbr].split(",",3)
		
			if locations == '':
				useful_row_info = []
				useful_row_info.append(genus)
				useful_row_info.append(epithet)
				useful_row_info.append(lebanon)
				useful_row_info.append(locations)
				fifth_destination_file.write(",".join(useful_row_info) + "\n")
			
			else:
				sub_locations = locations.split("#")
			 
			for sub_location_nbr,sub_location in enumerate(sub_locations):
				if not sub_location_nbr == 0:
					useful_row_info = []
					useful_row_info.append(genus)
					useful_row_info.append(epithet)
					useful_row_info.append(lebanon)
					useful_row_info.append(sub_location)
					fifth_destination_file.write(",".join(useful_row_info) + "\n")
	
	
		fifth_destination_file.close()
		fifth_destination_file = codecs.open(fifth_destination_file_name,encoding='utf-8')
		info_lines_list = []
	
	
		for line in fifth_destination_file:
			info_lines_list.append(line.strip())
	
		
		for line_nbr in range(len(info_lines_list)):
			genus,epithet,lebanon,locations = info_lines_list[line_nbr].split(",",3)
		
		
			if locations != '':
				location,sub_locations = locations.split(":",1)
			
				
				sub_locations = sub_locations.split(",")
			
				for sub_location in sub_locations:
					useful_row_info = []
					useful_row_info.append(genus.strip())
					useful_row_info.append(epithet.strip())
					useful_row_info.append(lebanon.strip())
					useful_row_info.append(location.strip())
					useful_row_info.append(sub_location.strip())
					sixth_destination_file.write(",".join(useful_row_info) + "\n")
		
			else:
				sixth_destination_file.write(",".join(useful_row_info) + "\n")


		
		os.remove(current_path+'/'+fourth_destination_file_name)
		os.remove(current_path+'/'+fifth_destination_file_name)
			

		end_result_file_name = 'cleansed-extracted-flora-data-from-book-0' + str(extracted_flora_data_book_number) + '.txt'
		os.rename(sixth_destination_file_name,end_result_file_name)
		
		
		current_path = os.getcwd()
		destination_file_path = current_path + '/cleansed-extracted-flora-data-from-book-0' + str(extracted_flora_data_book_number) + '.txt'
		destination_file_csv_path = current_path + '/cleansed-extracted-flora-data-from-book-0' + str(extracted_flora_data_book_number) + '.csv'
		shutil.copyfile(destination_file_path,destination_file_csv_path)
		
		os.remove(current_path+'/'+end_result_file_name)
		

import fitz
import re
import pandas as pd


class Text_Characteristics:
	def __init__(self, font, size, color, flags=0):
		self.font = font
		self.size = size
		self.color = color
		self.flags = flags
		self.style = readable_flags(self.flags)
	
	def __str__(self):
		return f"Text Characteristics: '{self.font}' ({self.style}), size {self.size:g}, color " + ("#%06x" % self.color)
      

def readable_flags(flags):
	flags_list = []
	if flags == 1:
		flags_list.append("superscript")
	if flags == 2:
		flags_list.append("italic")
	if flags == 4:
        	flags_list.append("serifed")
	else:
        	flags_list.append("sans")
	if flags == 8:
        	flags_list.append("monospaced")
	else:
        	flags_list.append("proportional")
	if flags == 16:
        	flags_list.append("bold")
	return ", ".join(flags_list)
    

def flora_family_name(span_text,span_characteristics):
	family_name_typical_characteristics = "Text Characteristics: 'Times-Roman' (serifed, proportional), size 10.9449, color #000000"
	return re.match('^.*ACEAE$',span_text) and (str(span_characteristics) == family_name_typical_characteristics)


def general_genus(span_text):
	return re.match('[A-Z]+[A-Za-z\s.]*\s\—\s[A-Z]([a-z]|\s|,|[a-zàâçéèêëîïôûùüÿñæœ .-])+',span_text)	

	
def general_genus_description(span_text,span_characteristics,previous_text_ends_with_period):
    	general_genus_typical_characteristics = "Text Characteristics: 'Times-Roman' (serifed, proportional), size 10.9449, color #000000"
    	if general_genus_typical_characteristics != str(span_characteristics) and previous_text_ends_with_period:
        	return False
    	return True


def genus_and_epithet(span_font,span_text,span_size):
    	if (span_font == "Times-Bold") and (span_size > 10) and (re.match('[A-Z][a-z]+\s[a-z]+',span_text)):
        	return True
    	else:
    		return False

	
def genus_alone(span_font,span_text,span_size):
    	if (span_font == "Times-Bold") and (span_size > 10) and (re.match('^[A-Z][a-z]+$',span_text)):
        	return True
    	else:
    		return False

	
def epiphet_alone(span_font,span_text,span_size):
    	if (span_font == "Times-Bold") and (span_size > 10) and (re.match('\s[a-z]+',span_text) or re.match('[a-z]+',span_text)):
        	return True
    	else:
    		return False


def lebanon_locations(span_text,span_size,span_font):
    	return re.match('L\..*',span_text) and (span_size < 10) and (span_font == 'Times-Italic' or span_font == 'Times-Roman')
        

def syrian_locations(span_text,span_size,span_font):
    	return re.match('S\..*',span_text) and (span_size < 10) and (span_font == 'Times-Italic' or span_font == 'Times-Roman')
    

def current_text_ends_with_period(span_text):
    	return re.match('.*(\.)$',span_text)


def appropriate_page_numbers(current_pdf_file,pdf_doc_1,pdf_doc_2,pdf_doc_3):
	if current_pdf_file == pdf_doc_1:
		return 78,642
	elif current_pdf_file == pdf_doc_2:
		return 7,701
	else:
		return 7,588


if __name__ == "__main__":

	pdf_doc_1 = fitz.open("flora-book-01.pdf")
	pdf_doc_2 = fitz.open("flora-book-02.pdf")
	pdf_doc_3 = fitz.open("flora-book-03.pdf")
	pdf_docs_list = [pdf_doc_1,pdf_doc_2,pdf_doc_3]


	for pdf_file in pdf_docs_list:
		extracted_flora_book_data = pd.DataFrame(columns = ['FamilyName','FamilyNameDescription','GeneralGenusAndDescription','Genus','Epithet','LebanonLocations','SyrianLocations'])
		extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0

		starting_page_number, ending_page_number = appropriate_page_numbers(pdf_file,pdf_doc_1,pdf_doc_2,pdf_doc_3)
		
		text_belongs_to_flora_family_description = False
		text_belongs_to_genus_description = False
		text_is_epithet= False
		text_belongs_to_lebanon_locations = False
		text_belongs_to_syrian_locations = False
			
		for page in (pdf_file[x] for x in range(starting_page_number,ending_page_number)):
			blocks = page.getText("dict", flags=11)["blocks"]
			for x,b in enumerate(blocks):
				for y,l in enumerate(b["lines"]):
					for z,s in enumerate(l["spans"]):
						span_text = s["text"]
						span_characteristics = Text_Characteristics(s["font"], s["size"], s["color"], s["flags"])
						span_font = s["font"]
						span_size = s["size"]
					
						if text_belongs_to_flora_family_description:							
							if re.match('[A-Z][A-Z]+.*\s',span_text):
								extracted_flora_book_data.iloc[-1]['FamilyNameDescription'] = family_description_encoded_text.decode('utf-8')
								text_belongs_to_flora_family_description = False
							else:
								
								family_description_encoded_text += span_text.encode('utf-8')
					
					
						elif flora_family_name(span_text,span_characteristics):
							extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0
							extracted_flora_book_data.iloc[-1]['FamilyName'] = span_text
							text_belongs_to_flora_family_description = True
							family_description_encoded_text = ''.encode('utf-8')
					
					
						elif text_belongs_to_genus_description:
							if general_genus_description(span_text,span_characteristics,previous_text_ends_with_period):
                        					genus_description_encoded_text += span_text.encode('utf-8')
                        					previous_text_ends_with_period = current_text_ends_with_period(span_text)
							else:
								extracted_flora_book_data.iloc[-1]['GeneralGenusAndDescription'] = genus_description_encoded_text.decode('utf-8')
								text_belongs_to_genus_description = False
                        		

						elif general_genus(span_text):
                    					text_belongs_to_genus_description = True
                    					if not re.match('.*(\.)$', span_text):
                        					previous_text_ends_with_period = False
                    					else:
                        					previous_text_ends_with_period = True
                        
                    					extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0
                    					genus_description_encoded_text = span_text.encode('utf-8')
                   
					
						elif genus_and_epithet(span_font,span_text,span_size):
							extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0
							extracted_flora_book_data.iloc[-1]['Genus'] = span_text.split()[0]
							extracted_flora_book_data.iloc[-1]['Epithet'] = span_text.split()[1].strip()
					
					
						elif text_is_epithet:
                    					extracted_flora_book_data.iloc[-1]['Epithet'] = span_text.strip()
                    					text_is_epithet= False		

					
						elif genus_alone(span_font,span_text,span_size):
							extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0
							extracted_flora_book_data.iloc[-1]['Genus'] = span_text
							text_is_epithet = True
						
					
						elif lebanon_locations(span_text,span_size,span_font):
							extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0
							extracted_flora_book_data.iloc[-1]['LebanonLocations'] = span_text
							text_belongs_to_lebanon_locations = True
							leb_locations_encoded_text = span_text.encode('utf-8')
						
					
						elif text_belongs_to_lebanon_locations:
							if (not re.match('S\.',span_text)) and (not re.match('Aire',span_text)):
								leb_locations_encoded_text += span_text.encode('utf-8')
							else:
								extracted_flora_book_data.iloc[-1]['LebanonLocations'] = leb_locations_encoded_text.decode('utf-8')
								text_belongs_to_lebanon_locations = False
						
						
						elif syrian_locations(span_text,span_size,span_font):
							extracted_flora_book_data.loc[len(extracted_flora_book_data)] = 0
							extracted_flora_book_data.iloc[-1]['SyrianLocations'] = span_text
							text_belongs_to_syrian_locations = True
							syr_locations_encoded_text = span_text.encode('utf-8')
					
					
						elif text_belongs_to_syrian_locations:		
							if (not re.match('Aire\sg.*\.',span_text)) and (not re.match('\sAire\sgéogr\.\s\—',span_text)) and (not re.match('Aire',span_text)) and (not re.match('Air\sgéog',span_text)):
								syr_locations_encoded_text += span_text.encode('utf-8')
							
							else:
								extracted_flora_book_data.iloc[-1]['SyrianLocations'] = syr_locations_encoded_text.decode('utf-8')
								text_belongs_to_syrian_locations = False
						

		book_number = pdf_docs_list.index(pdf_file) + 1
         					
		output_file_name = 'extracted-flora-data-from-book-0' + str(book_number) + '.csv'
			
		extracted_flora_book_data.to_csv(output_file_name)

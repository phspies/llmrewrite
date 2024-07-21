import xml.etree.ElementTree as ET

class ProcessXML:
	code = ""
	def __init__(self,inputxml):
		try:
			self.code = ET.fromstring(inputxml).text			
		except:
			print(inputxml)
       
        
import os
from pathlib import Path
from color import *
import json

class Rewritemodels:
	def __init__(self,llm, inputpath, outputpath):
		print(f"{color.BOLD}{color.UNDERLINE}Working on Models{color.END}")
		self.llm = llm
		self.inputpath = f"{inputpath}"
		self.outputpath = f"{outputpath}/models.py"

		sourceschema = f"{self.inputpath}/db/schema.rb"
		print(f"\tUsing schema file: {sourceschema}")        
		print(f"\tUsing LLM to convert schema to django model code")

		with open(sourceschema, "r") as file:
			sourceschemafile = file.read()
		targetmodelcode = self.llm.completion(f"Convert the following rubyonrails schema.rb file to python django model full code without comments or explanations.\n\n\n {sourceschemafile}")

		print(f"\tWriting new view file to {self.outputpath}")        
		f = open(self.outputpath, "w")
		f.write(targetmodelcode)
		f.close()

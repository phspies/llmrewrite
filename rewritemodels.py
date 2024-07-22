import os
from pathlib import Path
from color import *
from codetools import *
import json


class Rewritemodels:
	modeldump = ""

	def __init__(self,llm, inputpath, outputpath):
		print(f"{color.BOLD}{color.UNDERLINE}Working on Models{color.END}")
		self.llm = llm
		self.inputpath = f"{inputpath}"
		self.outputpath = f"{outputpath}/models.py"

		sourceschema = f"{self.inputpath}/db/schema.rb"
		print(f"Using schema file: {sourceschema}")        
		print(f"Using LLM to convert schema to django model code")

		with open(sourceschema, "r") as file:
			sourceschemafile = file.read()

		prompt = f"<code>{sourceschemafile}</code>"
		prompt += f"<instructions> \
			- REWRITE THE SPECIFIC RUBYONRAILS DATABASE SCHEMA IN THE <code> </code> TAG INTO PYTHON USING THE DJANGO FRAMEWORK. \
			- Use the same class for named method. \
			- Use recommended code security practices that would prevent major security coding exploits \
			- Only output the python code asked for. \
			- Provide only the updated code, without any explanations or additional text. \
			- If no change is needed, do not make any changes. \
			- Do not include a ```python wrapper in the code \
			- CREATE OUTPUT WITHOUT ANY COMMENTS OR ANY EXPLANATIONS OR ADDITIONAL TEXT. \
		</instructions>"


		targetmodelcode = self.llm.completion(prompt)
		codeobject = CodeTools(sourceschema, self.outputpath, sourceschemafile, targetmodelcode)
		codeobject.printcode()
		codeobject.savecode()
		self.modeldump = targetmodelcode

		print(f"Writing new view file to {self.outputpath}")        


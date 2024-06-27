import os
from pathlib import Path
from color import *

class RewriteControllers:
	def __init__(self,llm, inputpath, outputpath):
		print(f"{color.BOLD}{color.UNDERLINE}Working on Controllers{color.END}")
		self.llm = llm
		self.inputpath = inputpath
		self.outputpath = f"{outputpath}/views"
		os.makedirs(f"{self.outputpath}", mode=0o777, exist_ok=True)

		sourcecontrollerfolder = f"{self.inputpath}/app/controllers"
		controllers = [f for f in os.listdir(sourcecontrollerfolder) if os.path.isfile(f"{sourcecontrollerfolder}/{f}")]
		for controller in controllers:
			sourcecontroller = f"{sourcecontrollerfolder}/{controller}"
			targetview = f"{self.outputpath}/{controller.split('_')[0]}.py"

			print(f"\tWorking on {sourcecontroller} -> {targetview}")
			with open(sourcecontroller, "r") as file:
				controllerfile = file.read()
			print(f"\t\tUsing LLM to convert controller to view code")
			newviewcode = self.llm.completion(f"rewrite the following rubyonrails controller into python using the django framework without comments or explanations\n\n\n \
									 <documents> \
										<document index='1'> \
										 <document_content> {controllerfile} </document_content> \
									 	</document> \
									 </documents> ")

			print(f"\t\tWriting new view file to {targetview}")        
			f = open(targetview, "w")
			f.write(newviewcode)
			f.close()

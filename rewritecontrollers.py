import os
from pathlib import Path
from color import *
from processxml import ProcessXML
from codetools import *

class RewriteControllers:
	def __init__(self,llm, inputpath, outputpath, models, urls):
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

			print(f"Reading {sourcecontroller}")
			with open(sourcecontroller, "r") as file:
				controllerfile = file.read()
			
			prompt = f"<models>{models}</models>"
			prompt += f"<urls>{urls}</urls>"
			prompt += f"<code>{controllerfile}<code>"
					
			print(f"Rewriting {controller}")
			sourcecontroller = f"{sourcecontrollerfolder}/{controller}"
			prompt += "Please follow the steps: \
						- REWRITE THE SPECIFIC RUBYONRAILS CODE IN THE <code> </code> TAG INTO PYTHON USING THE DJANGO FRAMEWORK WITHOUT ANY COMMENTS OR ANY EXPLANATIONS OR ADDITIONAL TEXT. \
						- USE RECOMMENDED CODE SECURITY PRACTICES THAT WOULD PREVENT ALL KNOWN SECURITY CODING EXPLOITS \
						- DO NOT INCLUDE A ```PYTHON WRAPPER IN THE CODE \
						- DON'T RETURN THE <code> </code> TAG IN THE OUTPUT.  \
						- THE DATAMODELS USED IN THIS CONTROLLER IS LOCATED IN A PARENT FOLDER SO PLEASE ADJUST THE MODEL LOCATION ACCORDINGLY \
						- ENSURE THAT EACH RUBYONRAILS METHOD USED IN THE IN THE <CODE> </CODE> TAG IS CONVERTED TO A DJANGO EQUIVALENT CODE.  \
						- MAKE SURE RETURN TYPES SUPPORT BOTH HTML AND JSON RESPONSES \
						- TAKE NOTE OF THE params.require AND params.permit METHODS USED IN THE CONTROLLER. \
						- TAKE NOTE OF THE flash[:notice] METHOD USED WHEN RENDERING CONTROLLER.  \
						- TAKE NOTE OF THE URLS IN THE <urls> </urls> TAG WHEN GENERATING THE PYTHON METHODS AS OUTLIND IN THE urlpatterns VARIABLE.  \
						- TAKE NOTE OF THE URLS IN THE <models> </models> TAG."
			
			pythoncode = self.llm.completion(prompt)
			self.llm.completion("/clear")
			
			codeobject = CodeTools(controller, targetview, controllerfile, pythoncode)
			codeobject.printcode()
			codeobject.savecode()
			

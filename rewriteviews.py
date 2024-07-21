import os
from pathlib import Path
from color import *
from codetools import *


class RewriteViews:
    def __init__(self,llm, inputpath, outputpath):
        print(f"{color.BOLD}{color.UNDERLINE}Working on Views{color.END}")
        self.llm = llm
        self.inputpath = inputpath
        self.outputpath = outputpath
        self.viewspath = f"{outputpath}/templates"

        os.makedirs(f"{self.viewspath}", mode=0o777, exist_ok=True)

        # discovery all views in RoR project
        sourceviewfolder = f"{self.inputpath}/app/views"
        viewfolders = next(os.walk(f"{sourceviewfolder}"))[1]
        currenttargetfolder = ""
        for folder in viewfolders:
            currentsourcefolder = f"{sourceviewfolder}/{folder}"
            if folder == "layouts":
                currenttargetfolder = f"{self.viewspath}/templates"
            else:
                currenttargetfolder = f"{self.viewspath}/{folder}"
            os.makedirs(currenttargetfolder, mode=0o777, exist_ok=True)
            print(f"\t{color.BOLD}Working on {currentsourcefolder} -> {currenttargetfolder}{color.END}")
            for file in os.listdir(currentsourcefolder):
                if ".html" in file:
                    sourcefile = f"{currentsourcefolder}/{file}"
                    print(f"Reading {sourcefile}")
                    with open(sourcefile, "r") as file:
                        viewfilecontent = file.read()
                    
                    prompt = f"<code> \
                                    {viewfilecontent} \
                                <code>"
                
                    print(f"Rewriting {file}")

                    prompt += f"<instructions> \
                                - REWRITE THE SPECIFIC RUBYONRAILS VIEW CODE IN THE <code> </code> TAG INTO PYTHON USING THE DJANGO FRAMEWORK WITHOUT ANY COMMENTS OR ANY EXPLANATIONS OR ADDITIONAL TEXT. \
                                - USE RECOMMENDED CODE SECURITY PRACTICES THAT WOULD PREVENT ALL KNOWN SECURITY CODING EXPLOITS \
                                - DO NOT INCLUDE A ```PYTHON WRAPPER IN THE CODE \
                                - DON'T RETURN THE <CODE> </CODE> TAG IN THE OUTPUT.  \
                                - THE DATAMODELS USED IN THIS CONTROLLER IS LOCATED IN A PARENT FOLDER SO PLEASE ADJUST THE MODEL LOCATION ACCORDINGLY \
                                - ENSURE THAT EACH RUBYONRAILS METHOD USED IN THE IN THE <CODE> </CODE> TAG IS CONVERTED TO A DJANGO EQUIVALENT CODE.  \
                                </instructions>"
                    
                    pythoncode = self.llm.completion(prompt)
                    self.llm.completion("/clear")
                    

                    codeobject = CodeTools(sourcefile, outputpath, viewfilecontent, pythoncode)
                    codeobject.printcode()
                    codeobject.savecode()                    

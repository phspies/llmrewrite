import os
from pathlib import Path
from color import *

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
                    outputpath = f"{currenttargetfolder}/{file.split('.')[0]}.html"
                    print(f"\t\tWorking on view file -> {file}")
                    with open(f"{currentsourcefolder}/{file}", "r") as file:
                        viewfilecontent = file.read()
                    print(f"\t\t\tUsing LLM to convert view to python code")
                    newviewcode = self.llm.completion(f"""rewrite the following rubyonrails view into python using the django framework template without comments or explanations.\n\n\n 
                                                     <documents> 
														<document index='1'> 
															<document_content>
                                                       			{viewfilecontent}
															</document_content>
														</document>
													</documents> ")
													""")
                    print(f"\t\t\tWriting new view file to {outputpath}")        
                    f = open(outputpath, "w")
                    f.write(newviewcode)
                    f.close()

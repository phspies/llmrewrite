import subprocess
from callllm import *
from color import *
from codetools import *



class GenerateURLS:
    def __init__(self,llm, inputpath, outputpath):
        print(f"{color.BOLD}{color.UNDERLINE}Working on URLS{color.END}")

        #read current urls file
        outputfile = f"{outputpath}/urls.py"

        print(f"Learning routes from RoR app in {inputpath}")
        p = subprocess.Popen(['rake', 'routes'], cwd=inputpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        output = out.decode("utf-8")

        prompt = f"<code>{output}<code>"
        print(f"Rewriting routes")

        prompt += f"<instructions> \
                    - REWRITE THE SPECIFIC RUBYONRAILS RAKE ROUTES OUT IN THE <CODE> </CODE> TAG INTO PYTHON DJANGO DISPATCHER CONFIGURATION. \
                    - USE RECOMMENDED CODE SECURITY PRACTICES THAT WOULD PREVENT ALL KNOWN SECURITY CODING EXPLOITS \
                    - DON'T RETURN THE <CODE> </CODE> TAG IN THE OUTPUT.  \
                    - THE DATAMODELS USED IN THIS CONTROLLER IS LOCATED IN A PARENT FOLDER SO PLEASE ADJUST THE MODEL LOCATION ACCORDINGLY \
                    - ENSURE THAT EACH RUBYONRAILS METHOD USED IN THE IN THE <CODE> </CODE> TAG IS CONVERTED TO A DJANGO EQUIVALENT CODE.  \
                    - DO NOT INCLUDE A ```PYTHON WRAPPER IN THE CODE \
                    - DO NOT WITHOUT ANY COMMENTS OR ANY EXPLANATIONS OR ADDITIONAL TEXT. \
                    </instructions>"
        
        pythoncode = llm.completion(prompt)
        llm.completion("/clear")        
    
        codeobject = CodeTools("rake routes output", outputfile, output, pythoncode)
        codeobject.printcode()
        codeobject.savecode()

        self.djangoroutes = pythoncode
     
    
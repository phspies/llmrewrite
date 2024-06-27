import subprocess
from callllm import *
from color import *


class GenerateURLS:
    def __init__(self,llm, inputpath, outputpath):
        print(f"{color.BOLD}{color.UNDERLINE}Working on URLS{color.END}")
        self.llm = llm
        self.inputpath = inputpath
        self.outputpath = outputpath

        #read current urls file
        with open(f"{outputpath}/urls.py", "r") as file:
            self.currenturls = file.read()

        print(f"\tLearning routes from RoR app in {self.inputpath}")
        p = subprocess.Popen(['rake', 'routes'], cwd=self.inputpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print(f"\tUsing LLM to generate and merge the new urls into current")     
        
        mergedurls = self.llm.completion(f"rewrite the following rake routes out to URL python django dispatcher configuration in full without comments or explanations\n\n\n {out} \n\n \
                                         while merging the new routes into the following urls {self.currenturls} file without comments or explanations")

        print(f"\tWriting new urls.py file to {self.outputpath}/urls.py")        
        f = open(f"{self.outputpath}/urls.py", "w")
        f.write(mergedurls)
        f.close()

     
    
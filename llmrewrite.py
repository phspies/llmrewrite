from generateurls import *
from rewriteviews import *
from rewritecontrollers import *
from rewritemodels import *
from callllm import *
from processxml import ProcessXML


import argparse
import os
from litellm import completion

#llmmodel = "bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
#llmmodel ="bedrock/anthropic.claude-v2"
#llmmodel="claude-3-5-sonnet-20240620"
llmmodel="claude-3-opus-20240229"

for evar in 'AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION_NAME'.split(','):
    if evar not in os.environ:
        raise ValueError('Environment variable "%s" was not set' % evar)

parser = argparse.ArgumentParser()
parser.add_argument('--inputpath', help='Input path to the RubyOnRails project', required=True)
parser.add_argument('--outputpath', help='Output path to the Python Django project', required=True)
args = parser.parse_args()

llm = CallLLM(llmmodel)


# with open('testxml.xml', 'r') as file:
#     data = file.read()
#     ProcessXML(data)

models = Rewritemodels(llm, args.inputpath, args.outputpath).modeldump
RewriteControllers(llm, args.inputpath, args.outputpath, models)
#RewriteViews(llm, args.inputpath, args.outputpath)
#GenerateURLS(llm, args.inputpath, args.outputpath)

print(f"\n\n\n{color.BOLD}{color.UNDERLINE}Done!{color.END}")
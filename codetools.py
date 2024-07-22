from side_by_side import print_side_by_side
import os

class CodeTools:
    code = ""
    def __init__(self,inputfilename, outputfilename, inputcode, outputcode):
        self.inputcode = inputcode
        self.inputfilename = inputfilename
        self.outputfilename = outputfilename
        self.outputcode = outputcode

    def printcode(self):
        termsize = os.get_terminal_size()
        print(u'\u2015' * termsize.columns)        
        print_side_by_side(self.inputfilename + "\n" + u'\u2015' * int(((termsize.columns/2)-20)) + "\n" + self.inputcode, self.outputfilename + "\n" + u'\u2015' * int(((termsize.columns/2)-20)) + "\n" + self.outputcode, print_line_numbers=True, col_padding=10, delimiter='|++++|')
        print(u'\u2015' * termsize.columns)        

    def savecode(self):
        f = open(self.outputfilename, "w")
        f.write(self.outputcode)
        f.close()
        print(f"Writing new file to {self.outputfilename}")        

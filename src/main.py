import sys
from util import copy_files, generate_page_recursive

default_basepath = "/"

def main():

   basepath = default_basepath
   if len(sys.argv) > 1:
       basepath = sys.argv[1]

   copy_files("static", "docs")
   generate_page_recursive("content", "template.html", "docs", basepath)
   
main()
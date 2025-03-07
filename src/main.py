from util import copy_files, generate_page_recursive


def main():

   copy_files("static", "public")
   generate_page_recursive("content", "template.html", "public")
   
main()
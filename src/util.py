import re
import os
import shutil
from textnode import TextNode, TextType
from htmlnode import LeafNode

#Create functions that are generally utility functions.
#Function to split nodes based on a list of nodes, delimiter and text type
# -- input: old_nodes (list of TextNode), delimiter (string), text_type (TextType)
# -- output: list of TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes
#Function to extract markdown images from a string.
# -- input: text (string)
# -- output: list of tuples (image_text, image_url)
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#Function to extract markdown links from a string.
# -- input: text (string)
# -- output: list of tuples (link_text, link_url)
def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

#Function to split nodes based on images
# -- input: old_nodes (list of TextNode)
# -- output: list of TextNode
def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        extracted_images = extract_markdown_images(original_text)
        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue 
        for image in extracted_images:
            image_text = image[0]
            image_url = image[1]
            sections = original_text.split(f"![{image_text}]({image_url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
#Function to split nodes based on links
# -- input: old_nodes (list of TextNode)
# -- output: list of TextNode
def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue 
        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{link_text}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
#Function to convert text to textnode by running text through all the split functions
# -- input: text (string)
# -- output: TextNode
def text_to_textnode(text):
    node = TextNode(text, TextType.TEXT)
    node = split_nodes_delimiter([node], "**", TextType.BOLD)
   # node = split_nodes_delimiter(node, ">", TextType.QUOTE)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "*", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_delimiter(node, "```", TextType.CODE)
    node = split_nodes_images(node)
    node = split_nodes_links(node)
    return node


def text_node_to_html_node(text_node):
   # use a match case statement to convert the TextNode based on what the Enum type is into a HTMLNode
   match text_node.text_type:
      case TextType.TEXT:
         return LeafNode(None, text_node.text)
      case TextType.BOLD:
         return LeafNode("b", text_node.text)
      case TextType.ITALIC:
         return LeafNode("i", text_node.text)
      case TextType.CODE:
         return LeafNode("code", text_node.text)
      case TextType.LINK:
         return LeafNode("a", text_node.text, {"href": text_node.url})
      case TextType.IMAGE:
         return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
      case _:
         raise ValueError(f"invalid text type: {text_node.text_type}")
       
#recursive function to copy files from a source directory to a destination directory.
# -- input: src (Path), dest (Path)
def copy_files(source, destination):

    if os.path.exists(destination):
        print(f"The destination directory exists: {destination}")
        print(f"Deleting the destination directory and contents: {destination}")
        shutil.rmtree(destination)


    print(f"Creating directory: {destination}")
    os.mkdir(destination)
    print("*" * 20)


    for item in os.listdir(source):
        src_item = os.path.join(source, item)
        dst_item = os.path.join(destination, item)
        if os.path.isfile(src_item):
            print(f"We're looking at the file: {src_item}")
            print(f"* Copying {src_item} -> {dst_item}")
            shutil.copy(src_item, dst_item)
        else:
            print(f"This is a folder: {src_item}")
            copy_files(src_item, dst_item)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}.")

    if not os.path.exists(from_path):
        raise ValueError(f"Invalid from_path: {from_path}")
    
    with open(from_path, "r") as f:
        content = f.read()
        print(f"Read content from {from_path}")
        #print(content)

    with open(template_path, "r") as f:
        template = f.read()
        print(f"Read template from {template_path}")

    # import the markdown_to_html_node function from markdown_blocks.py
    from markdown_blocks import markdown_to_html_node, extract_title
    
    title = extract_title(content)

    content = markdown_to_html_node(content).to_html()
    print(f"Converted markdown to html")
    #print(content)

    #print(f"Extracted title: {title}")

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', 'href="' + basepath).replace('src="/', 'src="' + basepath)
    print(f"Replaced title and content in template")
    print(template)

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        print(f"Created destination directory: {dest_path}")

    with open(dest_path, "w") as f:
        f.write(template)
        print(f"Generated page in {dest_path}")
        f.close()


def generate_page_recursive(from_path, template_path, dest_path, basepath):
    for file in os.listdir(from_path):
        file_path = os.path.join(from_path, file)
        dest_base_path = os.path.join(dest_path, file)
        template = template_path
        dest_html = os.path.splitext(file)[0] + ".html"
        new_dest_path = os.path.join(dest_path, dest_html)
        ext = os.path.splitext(file)[1]

        print(f"checking file_path: {file_path}, dest_base_path: {dest_base_path}, template: {template}, new_dest_path: {new_dest_path}, ext: {ext}")


        if os.path.isfile(file_path) and ext == ".md":
            print(f"Generating page from {file_path} -> {new_dest_path} using template {template}.")
            generate_page(file_path, template, new_dest_path, basepath)
        else:
            generate_page_recursive(file_path, template, dest_base_path, basepath)
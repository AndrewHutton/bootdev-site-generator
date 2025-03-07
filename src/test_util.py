import unittest
from util import (
   split_nodes_delimiter, 
   extract_markdown_links, 
   extract_markdown_images, 
   split_nodes_images, 
   split_nodes_links, 
   text_to_textnode
   )
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
   def test_delim_bold(self):
      node = TextNode("This is a text node with a **bolded** word in the middle.", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      self.assertEqual(
         [
            TextNode("This is a text node with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word in the middle.", TextType.TEXT)
         ],
         new_nodes
      )

   def test_delim_italic(self):
      node = TextNode("This is a text node with *some italic words* in the middle.", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
      self.assertEqual(
         [
            TextNode("This is a text node with ", TextType.TEXT),
            TextNode("some italic words", TextType.ITALIC),
            TextNode(" in the middle.", TextType.TEXT)
         ],
         new_nodes
      )

   def test_delim_bold_double(self):
      node = TextNode("This is a **text node** with two **bold sections** in the middle.", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      self.assertEqual(
         [
            TextNode("This is a ", TextType.TEXT),
            TextNode("text node", TextType.BOLD),
            TextNode(" with two ", TextType.TEXT),
            TextNode("bold sections", TextType.BOLD),
            TextNode(" in the middle.", TextType.TEXT)
         ],
         new_nodes
      )

   def test_multi_markdown_types(self):
      node = TextNode("**Bold** and _italic_ text", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
      self.assertEqual(
         [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
         ],
         new_nodes
      )


class TestRegex(unittest.TestCase):
   def test_extract_markdown_images(self):
      matches = extract_markdown_images(
         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
      )
      self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
      

   def test_extract_markdown_links(self):
      matches = extract_markdown_links(
         "This is text with an link ![link to web](https://www.google.com)"
      )
      self.assertListEqual([("link to web", "https://www.google.com")], matches)

   def test_extract_markdown_multi_links(self):
      matches = extract_markdown_links(
         "This is text with an link [link to web](https://www.google.com) and another [](https://www.google.com/image.png)"
      )
      self.assertListEqual(
         [
            ("link to web", "https://www.google.com"),
            ("", "https://www.google.com/image.png")
         ], 
         matches
      )

   def test_split_images_single(self):
      node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
      new_nodes = split_nodes_images([node])
      self.assertEqual(
         [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
         ],
         new_nodes
      )

   def test_split_images_multiple(self):
      node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://i.imgur.com/wow.png)", TextType.TEXT)
      new_nodes = split_nodes_images([node])
      self.assertEqual(
         [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://i.imgur.com/wow.png")
         ],
         new_nodes
      )

   def test_split_links_single(self):
      node = TextNode("This is text with an [this link rocks](https://www.google.com/rocks)", TextType.TEXT)
      new_nodes = split_nodes_links([node])
      self.assertEqual(
         [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("this link rocks", TextType.LINK, "https://www.google.com/rocks")
         ],
         new_nodes
      )

   def test_split_links_plain(self):
      node = TextNode("This is text with no links, oops!", TextType.TEXT)
      new_nodes = split_nodes_links([node])
      self.assertEqual(
         [
            TextNode("This is text with no links, oops!", TextType.TEXT)

         ],
         new_nodes
      )

   def test_to_textnode(self):
      text = "This is a test with **bold** and _italic_ text"
      node = text_to_textnode(text)
      self.assertEqual(
         [
            TextNode("This is a test with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
         ], 
         node
         )
      
   def test_text_to_textnodes_full(self):
      nodes = text_to_textnode(
         "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
      )
      self.assertListEqual(
         [
               TextNode("This is ", TextType.TEXT),
               TextNode("text", TextType.BOLD),
               TextNode(" with an ", TextType.TEXT),
               TextNode("italic", TextType.ITALIC),
               TextNode(" word and a ", TextType.TEXT),
               TextNode("code block", TextType.CODE),
               TextNode(" and an ", TextType.TEXT),
               TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
               TextNode(" and a ", TextType.TEXT),
               TextNode("link", TextType.LINK, "https://boot.dev"),
         ],
         nodes,
      )

   
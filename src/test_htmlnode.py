import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from util import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
   def test_single_prop(self):
      node = HTMLNode("h1", "this is a title", None, {"href": "https://www.google.com"})
      expected = ' href="https://www.google.com"'
      self.assertEqual(node.props_to_html(), expected)

   def test_multiple_props(self):
      node = HTMLNode("h1", "this is a title", None, {"href": "https://www.google.com", "class": "title"})
      expected = ' href="https://www.google.com" class="title"'
      self.assertEqual(node.props_to_html(), expected)

   def test_empty_props(self):
      node = HTMLNode("h1", "this is a title", None, None)
      expected = ""
      self.assertEqual(node.props_to_html(), expected)

   def test_leaf_node(self):
      node = LeafNode("h1","this is a title")
      expected = "<h1>this is a title</h1>"
      self.assertEqual(node.to_html(), expected)

   def test_leaf_node_no_tag(self):
      node = LeafNode(None, "this is a title")
      expected = "this is a title"
      self.assertEqual(node.to_html(), expected)

   def test_leaf_node_empty_value(self):
      node = LeafNode("h1", None)
      with self.assertRaises(ValueError):
         node.to_html()
      

   def test_leaf_node_empty_tag(self):
      node = LeafNode(None, "this is a title")
      expected = "this is a title"
      self.assertEqual(node.to_html(), expected)

   def test_leaf_node_props(self):
      node = LeafNode("h1","this is a title", {"class": "title"})
      expected = '<h1 class="title">this is a title</h1>'
      self.assertEqual(node.to_html(), expected)

   def test_leaf_node_empty_props(self):
      node = LeafNode("h1", "this is a title", None)
      expected = "<h1>this is a title</h1>"
      self.assertEqual(node.to_html(), expected)

   def test_leaf_node_multi_props(self):
      node = LeafNode("h1", "this is a title", {"class": "title", "id": "title"})
      expected = '<h1 class="title" id="title">this is a title</h1>'
      self.assertEqual(node.to_html(), expected)

   def test_to_html_with_children(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode("div", [child_node])
      expected = "<div><span>child</span></div>"
      self.assertEqual(parent_node.to_html(), expected)

   def test_to_html_with_grandkids(self):
      grandchild_node = LeafNode("span", "grandchild")
      child_node = ParentNode("div", [grandchild_node])
      parent_node = ParentNode("div", [child_node])
      expected = "<div><div><span>grandchild</span></div></div>"
      self.assertEqual(parent_node.to_html(), expected)

   def test_to_html_many_children(self):
      child_node1 = LeafNode("b", "child1")
      child_node2 = LeafNode("i", "child2")
      child_node3 = LeafNode(None, "child3")
      parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
      expected = "<div><b>child1</b><i>child2</i>child3</div>"
      self.assertEqual(parent_node.to_html(), expected)

class TestTextNodeToHTMLNode(unittest.TestCase):
   def test_text(self):
      node = TextNode("this is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "this is a text node")

   def test_bold(self):
      node = TextNode("this is a bold node", TextType.BOLD)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "b")
      self.assertEqual(html_node.value, "this is a bold node")

   def test_image(self):
      node = TextNode("This is an image", TextType.IMAGE, "https://www.google.com")
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "img")
      self.assertEqual(html_node.value, "")
      self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is an image"})

if __name__ == "__main__":
   unittest.main()
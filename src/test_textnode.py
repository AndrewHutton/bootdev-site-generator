import unittest
from textnode import TextNode, TextType

class TestTestNode(unittest.TestCase):
   def test_eq(self):
      node = TextNode("This is a text node", TextType.BOLD, None)
      node2 = TextNode("This is a text node", TextType.BOLD)
      self.assertEqual(node, node2)

      node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
      node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
      self.assertEqual(node, node2)


      node = TextNode("This is a text node", TextType.TEXT)
      node2 = TextNode("This is a text node", TextType.BOLD)
      self.assertNotEqual(node, node2)

      node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
      node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.co.uk")
      self.assertNotEqual(node, node2)

      node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
      node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.co.uk")
      self.assertNotEqual(node, node2)

if __name__ == "__main__":
   unittest.main()
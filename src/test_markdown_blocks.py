import unittest
from markdown_blocks import (
   markdown_to_blocks, 
   block_to_block_type, 
   BlockType,
   markdown_to_html_node,
   extract_title
)

class TestMarkdownToHTML(unittest.TestCase):
   def test_markdown_to_blocks_empty(self):
      md = """




      """
      blocks = markdown_to_blocks(md)
      self.assertEqual([], blocks)

   def test_markdown_to_blocks_single(self):
      md = """ This is a single line of **markdown** """
      blocks = markdown_to_blocks(md)
      self.assertEqual([
         "This is a single line of **markdown**"
      ],
      blocks
      )

   def test_markdown_to_blocks_multi(self):
      md = """
This is a line of markdown in plain text

This is line one of a paragraph with **bold** and
here is line two with _italic_ text.

-This is a list item
-This is another list item
"""      
      blocks = markdown_to_blocks(md)
      self.assertEqual(blocks,
                       [
                          "This is a line of markdown in plain text",
                          "This is line one of a paragraph with **bold** and\nhere is line two with _italic_ text.",
                          "-This is a list item\n-This is another list item"
                       ])
      
   def test_block_to_block_types(self):
      block = "```\ndef hello()\n```"
      self.assertEqual(block_to_block_type(block), BlockType.CODE)
      block = "### This is a heading"
      self.assertEqual(block_to_block_type(block), BlockType.HEADING)
      block = "\n> This is a quote\n> with multiple lines"
      self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
      block = "- Item 1\n- Item 2\n- Item 3"
      self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
      block = "1. First item\n2. Second item"
      self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
      block = "Just some normal text."
      self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

   def test_paragraph(self):
      md = """
This is **bolded** paragraph
text in a p
tag here

      """
      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(html,
                     "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
                    ) 
      
   def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

   def test_lists(self):
      md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(
         html,
         "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
      )

   def test_headings(self):
      md = """
# this is an h1

this is paragraph text

## this is an h2
"""

      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(
         html,
         "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
      )

   def test_blockquote(self):
      md = """
> This is a
> blockquote block

this is paragraph text

"""

      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(
         html,
         "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
      )

   def test_code(self):
      md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(
         html,
         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
      )

   def test_title_extraction(self):
      md = """
# This is a H1 title

This is a paragraph

## This is a H2 title
"""
      title = extract_title(md)
      self.assertEqual(title, "This is a H1 title")

        
   def test_title_extraction_no_title(self):
      md = """
This is a paragraph

## This is a H2 title
"""
      #title = extract_title(md)
      with self.assertRaises(Exception) as context: 
         extract_title(md)

if __name__ == "__main__":
   unittest.main()
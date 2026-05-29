from enum import Enum
import re

class BlockType(Enum):
   PARAGRAPH = 1
   HEADING = 2
   CODE = 3
   QUOTE = 4
   UNORDERED_LIST = 5
   ORDERED_LIST = 6


def markdown_to_blocks(markdown:str)->list[str]:
   final = []
   blocks = markdown.split("\n\n")
   for block in blocks:
      if not block.strip():
         continue
      block = block.strip()
      block = block.replace("  ","")
      final.append(block)
   return final

def block_to_blocktype(block:str)->BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

      


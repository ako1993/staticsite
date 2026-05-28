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

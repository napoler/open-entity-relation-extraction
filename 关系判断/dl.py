
from harvesttext import HarvestText



ht0 = HarvestText()
s="nnn"
print("ht知识：",ht0.triple_extraction(sent=s,expand = "exclude_entity"))
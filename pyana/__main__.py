import string
from examples.utils import checkSymLink
from examples.gp_datdir import gp_datdir

checkSymLink()

for l in list(string.ascii_uppercase):
  print gp_datdir(l, 6)

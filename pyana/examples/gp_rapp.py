import logging, argparse, os, re
import numpy as np
from ..ccsgp.config import default_colors
from ..ccsgp.ccsgp import make_plot
from .utils import getWorkDirs, checkSymLink
from .gp_rdiff import getUArray, getEdges, getCocktailSum, enumzipEdges
from decimal import Decimal

ranges = [0.3, 0.7] # TODO: same for IMR

def gp_rapp():
  """rho in-medium ratios by Rapp (based on protected data)"""
  inDir, outDir = getWorkDirs()
  eRanges = np.array([Decimal(str(e)) for e in ranges])
  # prepare data
  yields = []
  for infile in os.listdir(inDir):
    energy = re.compile('\d+').search(infile).group()
    medium = np.loadtxt(open(os.path.join(inDir, infile), 'rb'))
    uMedium = getUArray(medium)
    eMedium = getEdges(medium)
    for i, (e0, e1) in enumzipEdges(eRanges):
      uSum = getCocktailSum(e0, e1, eMedium, uMedium)
      logging.debug('%s> %g - %g: %r' % (energy, e0, e1, uSum))
      yields.append([float(energy), uSum.nominal_value, 0, 0, 0])
  data = np.array(sorted(yields))
  data[:,1] /= data[-1,1] # divide by 200
  # make plot
  make_plot(
    data = [ data[:-1] ],
    properties = [ 'lt 1 lw 4 ps 1.5 lc %s pt 18' % default_colors[0] ],
    titles = [ 'LMR (0.3 - 0.7 GeV/c^{2})' ],
    name = os.path.join(outDir, 'rapp'),
    xlabel = '{/Symbol \326}s_{NN} (GeV)', ylabel = 'Rapp Ratio to 200 GeV',
    lmargin = 0.1, key = ['width -3', 'left']
  )
  return 'done'

if __name__ == '__main__':
  checkSymLink()
  parser = argparse.ArgumentParser()
  parser.add_argument("--log", help="show log output", action="store_true")
  args = parser.parse_args()
  loglevel = 'DEBUG' if args.log else 'WARNING'
  logging.basicConfig(
    format='%(message)s', level=getattr(logging, loglevel)
  )
  print gp_rapp()

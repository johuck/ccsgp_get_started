import logging, argparse, os, sys, re
import numpy as np
from fnmatch import fnmatch
from collections import OrderedDict
from .utils import getWorkDirs, checkSymLink, getEnergy4Key
from ..ccsgp.ccsgp import make_plot
from ..ccsgp.utils import getOpts
from ..ccsgp.config import default_colors

cocktail_style = 'with filledcurves pt 0 lc %s lw 5 lt 1' % default_colors[8]
pseudo_point = np.array([ [-1,1e-7,0,0,1] ])

def gp_stack(version):
  """example for a plot w/ stacked graphs using QM12 data (see gp_panel)

  * how to omit keys from the legend
  * manually add legend entries
  * automatically plot arrows for error bars larger than data point value

  .. image:: pics/stackQM12.png
     :width: 550px

  :param version: plot version / input subdir name
  :type version: str
  """
  shift = {
    '200': 200., '62': 15., '39': 0.5, '27': 0.01, '19': 1e-4
  } if (
    version != 'QM12' and version != 'Latest19200_PatrickQM12' and version != 'QM12Latest200'
  ) else {
    '200': 200., '62': 20., '39': 1., '19': 0.05
  }
  inDir, outDir = getWorkDirs()
  inDir = os.path.join(inDir, version)
  data, cocktail = OrderedDict(), OrderedDict()
  for file in os.listdir(inDir):
    energy = re.compile('\d+').search(file).group()
    data_type = re.sub('%s\.dat' % energy, '', file)
    file_url = os.path.join(inDir, file)
    data_import = np.loadtxt(open(file_url, 'rb'))
    # following scaling is wrong for y < 0 && shift != 1
    data_import[:,(1,3,4)] *= shift[energy]
    if fnmatch(file, 'data*'):
      data[energy] = data_import
    elif fnmatch(file, 'cocktail*'):
      data_import[:,(2,3)] = 0 # don't plot dx,dy for cocktail
      if energy == '19' and version == 'QM12':
        # cut off cocktail above 1.1 GeV/c^2
        cocktail[energy] = data_import[data_import[:,0] < 1.3]
      else:
        cocktail[energy] = data_import
  dataOrdered = OrderedDict(
    (' '.join([
      getEnergy4Key(k), 'GeV', '{/Symbol \264} %g' % shift[k],
      '            STAR Preliminary' if version == 'QM12Latest200' and k == '39' else '',
      '    [arXiv:1312.7397]' if version == 'QM12Latest200' and k == '200' else ''
    ]), data[k])
    for k in sorted(data, key=int)
  )
  nSetsData, nSetsCocktail = len(dataOrdered), len(cocktail)
  yr_low = 3e-7 if version == 'QM12' else 1e-10
  if version == 'Latest19200_PatrickQM12': yr_low = 1e-7
  if version == 'QM12Latest200': yr_low = 2e-6
  make_plot(
    data = cocktail.values() + [ pseudo_point ] + dataOrdered.values(),
    properties = [ cocktail_style ] * (nSetsCocktail+1) + [
      'lt 1 lw 4 ps 1.5 lc %s pt 18' % default_colors[i]
      for i in xrange(nSetsData)
    ],
    titles = [''] * nSetsCocktail + ['Cocktail w/o {/Symbol \162}'] + dataOrdered.keys(),
    name = os.path.join(outDir, 'stack%s' % version),
    ylabel = '1/N@_{mb}^{evt} dN@_{ee}^{acc.}/dM_{ee} [ (GeV/c^2)^{-1} ]',
    xlabel = 'invariant dielectron mass, M_{ee} (GeV/c^{2})',
    ylog = True, xr = [0, 3.5], yr = [yr_low, 2e3],
    lmargin = 0.09, arrow_offset = 0.8,
    tmargin = 0.9 if version != 'QM12Latest200' else 0.99,
    key = [
      'width -3', 'at graph 1.,1.2', 'maxrows 2'
    ] if version != 'QM12Latest200' else [
      'width -14', 'maxcols 1'
    ],
    #labels = {'BES Energies are STAR Preliminary': [0.38,0.9,False]}
    labels = {'{/Symbol=50 \775}': [0.64,0.81,False]}
    #arrows = [ # example arrow
    #  [ [2.4, 5e-5], [2.3, 1e-5], 'head filled lc 1 lw 5 lt 1 front' ],
    #],
  )
  return 'done'

if __name__ == '__main__':
  checkSymLink()
  parser = argparse.ArgumentParser()
  parser.add_argument("version", help="version = subdir name of input dir")
  parser.add_argument("--log", help="show log output", action="store_true")
  args = parser.parse_args()
  loglevel = 'DEBUG' if args.log else 'WARNING'
  logging.basicConfig(
    format='%(message)s', level=getattr(logging, loglevel)
  )
  print gp_stack(args.version)

import logging, argparse, os, sys
import numpy as np
import pandas as pd
from collections import OrderedDict
from ..ccsgp.ccsgp import make_plot
from ..examples.utils import getWorkDirs
from ..ccsgp.utils import getOpts
from ..ccsgp.config import default_colors

def gp_isotherms(guest, struc):
  """example for plotting from a comma separated file via pandas.read_csv

  1. prepare input/output directories
  2. load the data into an OrderedDict() [adjust axes units]
  3. sort countries from highest to lowest population
  4. select the <topN> most populated countries
  5. call ccsgp.make_plot with data from 4

  Below is an output image for country initial T and the 4 most populated
  countries for this initial (click to enlarge). Also see::

    $ python -m ccsgp_get_started.isoplots.gp_isotherms -h

  for help on the command line options.

  .. image:: pics/T.png
     :width: 450 px

  .. image:: pics/U.png
     :width: 450 px

  :param initial: country initial
  :type initial: str
  :param topN: number of most populated countries to plot
  :type topN: int
  :ivar inDir: input directory according to package structure and initial
  :ivar outDir: output directory according to package structure
  :ivar data: OrderedDict with datasets to plot as separate keys
  :ivar file: data input file for specific country, format: [x y] OR [x y dx dy]
  :ivar file_url: absolute url to input file
  """
  # prepare input/output directories
  inDir, outDir = getWorkDirs()
  inDir = os.path.join(inDir, guest)
  outDir = os.path.join(outDir, guest, struc)
  if not os.path.exists(inDir): # catch missing initial
    return "guest %s doesn't exist" % guest
  # prepare data
  file_name = os.path.join(inDir, '{}_{}.csv'.format(struc, guest))
  df = pd.read_csv(file_name)
  df['Pressure'] /= 1000.
  for istruc, struc_name in enumerate(df.columns):
    if istruc == 0 or istruc == 1: continue
    if not struc_name.startswith('TBM_'): continue
    struc_std = df.columns[istruc+1]
    data = OrderedDict()
    data[struc_name] = df[df[struc_name]>0.].as_matrix(columns=['Pressure',
      struc_name, struc_std]) # load data
    #logging.debug(data) # shown if --log flag given on command line
    # generate plot using ccsgp.make_plot
    #make_plot(
    #  data = data.values(),
    #  properties = [ 'lt 1 lw 4 ps 1.7 lc %s pt 18' % default_colors[(int(guest ==
    #                                                                    'N2'))] ],
    #  titles = [ key.replace('_', ' ') for key in data.keys()], # use data keys as legend titles
    #  name = os.path.join(outDir, '{}'.format(struc_name)),
    #  xlog = True, ylog = True,
    #  key = [ 'top left', 'nobox' ],
    #  ylabel = '{} loading in (kg/mol)'.format(guest),
    #  xlabel = 'pressure in (Pa)', rmargin = 0.99, tmargin = 0.95, size='8.5in,8in'
    #)
    data = pd.DataFrame(data)
    data.pd.DataFrame.to_csv(path_or_buf=struc_name, sep=' ',columns=3)
    break
  return 'done'

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("guest", help="guest molecule adsorbed in framework")
  parser.add_argument("struc", help="structure name")
  parser.add_argument("--log", help="show log output", action="store_true")
  args = parser.parse_args()
  loglevel = 'DEBUG' if args.log else 'WARNING'
  logging.basicConfig(
    format='%(message)s', level=getattr(logging, loglevel)
  )
  print gp_isotherms(args.guest, args.struc)

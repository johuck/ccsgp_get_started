import logging, argparse, os, sys
import numpy as np
from collections import OrderedDict
from ..ccsgp.ccsgp import make_plot
from ..examples.utils import getWorkDirs
from ..ccsgp.utils import getOpts

def gp_datdir(gas, mats):
  """example for plotting from a text file via numpy.loadtxt

  1. prepare input/output directories
  2. load the data into an OrderedDict() [adjust axes units]
  3. call ccsgp.make_plot with data from 4

  Below is an output image for country initial T and the 4 most populated
  countries for this initial (click to enlarge). Also see::

    $ python -m ccsgp_get_started.examples.gp_datdir -h

  for help on the command line options.

  .. image:: pics/T.png
     :width: 450 px

  .. image:: pics/U.png
     :width: 450 px

  :param gas: gas composition 
  :type gas: str
  :param mats: specific class of materials to plot or all of them
  :type mats: str
  :ivar inDir: input directory according to package structure and gas
  :ivar outDir: output directory according to package structure
  :ivar data: OrderedDict with datasets to plot as separate keys
  :ivar file: data input file for specific mats, format: [x y] OR [x y dx dy]
  :ivar country: country, filename stem of input file
  :ivar file_url: absolute url to input file
  :ivar nSets: number of datasets
  """
  # prepare input/output directories
  inDir, outDir = getWorkDirs()
  inDir = os.path.join(inDir, gas)
  print inDir
  if not os.path.exists(inDir): # catch missing gas
    return "gas composition %s doesn't exist" % gas
  # prepare data
  data = OrderedDict()
  if 'all' in mats:
      for classes in os.listdir(inDir):
        namemats = os.path.splitext(classes)[0]
        file_url = os.path.join(inDir, classes)
        print classes, namemats, file_url
        data_import = np.genfromtxt(file_url, delimiter=' ', dtype=None,
                                    usecols=(1,2)) # load data
        data_import[:,1] /= 1e3
        data[namemats]=data_import
      print data
  nSets = len(os.listdir(inDir))
  print data, nSets
  logging.debug(data) # shown if --log flag given on command line
  # generate plot using ccsgp.make_plot
  make_plot(
    data = data.values(),
    properties = [ getOpts(i) for i in xrange(nSets) ],
    titles = data.keys(), # use data keys as legend titles
    name = os.path.join(outDir, gas),
    key = [ 'top right', 'maxrows 2', 'width 1.5' ],
    ylabel = 'parasitic energy ({/Symbol \664} 10^{3} kJ/kg CO_2)',
    xlabel = 'Henry coefficient at 300K (mol/kg/Pa)', rmargin = 0.99, size='8.5in,8in'
  )
  return 'done'

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("gas", help="gas composition = input subdir with txt files, e.g. 'coal'")
  parser.add_argument("mats", help="material classes to plot, e.g. 'COFs' or 'all' for all classes")
  parser.add_argument("--log", help="show log output", action="store_true")
  args = parser.parse_args()
  loglevel = 'DEBUG' if args.log else 'WARNING'
  logging.basicConfig(
    format='%(message)s', level=getattr(logging, loglevel)
  )
  print gp_datdir(args.gas, args.mats)

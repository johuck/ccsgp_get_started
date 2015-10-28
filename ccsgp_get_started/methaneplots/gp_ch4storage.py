import logging, argparse, os, sys
import numpy as np
from collections import OrderedDict
from ..ccsgp.ccsgp import make_plot
from ..examples.utils import getWorkDirs
from ..ccsgp.utils import getOpts
from ..ccsgp.config import default_colors

def gp_ch4storage(prop, mats):
  """example for plotting from a text file via numpy.genfromtxt

  1. prepare input/output directories
  2. load the data into an OrderedDict() [adjust axes units]
  3. call ccsgp.make_plot with data from 4

  Below is an output image for country initial T and the 4 most populated
  countries for this initial (click to enlarge). Also see::

    $ python -m ccsgp_get_started.examples.gp_datdir -h

  for help on the command line options.

  :param prop: property name 
  :type prop: str
  :param mats: specific class of materials to plot or all of them
  :type mats: str
  :ivar inDir: input directory according to package structure and gas
  :ivar outDir: output directory according to package structure
  :ivar data: OrderedDict with datasets to plot as separate keys
  :ivar classes: data input file for specific mats, format: [x y] OR [x y dx dy]
  :ivar file_url: absolute url to input file
  :ivar nSets: number of datasets
  """
  # prepare color arrays for dataset
  my_color_set = [default_colors[i] for i in range(0, 3)] + [default_colors[6]] + [default_colors[i] for i in range(4, 5)] + [default_colors[3]] + [default_colors[5]] + [default_colors[7]]
  # prepare input/output directories
  inDirMEA, outDir = getWorkDirs()
  inDir = os.path.join(inDirMEA, prop)
  if not os.path.exists(inDir): # catch missing gas
    return "property name %s doesn't exist" % gas
  # prepare data
  data = OrderedDict()
  mea = OrderedDict() 
  if 'all' in mats:
      for classes in os.listdir(inDir):
        namemats = os.path.splitext(classes)[0]
        file_url = os.path.join(inDir, classes)
        if prop == 'di':
            #if classes == 'COFs.csv': continue
            if classes == 'expMOFs.csv': continue
            if classes == 'newCOFs.csv': continue
            if classes == 'ZIFs.csv': continue
            if classes == 'MOFs.csv': continue
            if classes == 'PPNs.csv': continue
            if classes == 'zeolites.csv': continue
            data_import = np.genfromtxt(file_url, delimiter=' ', dtype=None,
                                    usecols=(1,2)) # load data
            data[namemats]=data_import
            xlabel = 'diameter of largest included sphere ({/E \305})'
            xr = [0.0, 70]
            yr = [0.0, 200]
            key = [ 'top right', 'width -1.5']
            xlog = False
        elif prop == 'asa':
            if classes == 'newCOFs.csv': continue
            data_import = np.genfromtxt(file_url, delimiter=' ', dtype=None,
                                    usecols=(1,2)) # load data
            data_import[:,0] /= 1e3
            data[namemats]=data_import
            xlabel = 'accessible surface area ({/Symbol \664} 10^{3} m^2/cm^3)'
            xr = [0.0, 3.5]
            yr = [0.0, 200]
            key = [ 'top left', 'width -1.5']
            xlog = False
        elif prop == 'vf':
            if classes == 'newCOFs.csv': continue
            data_import = np.genfromtxt(file_url, delimiter=' ', dtype=None,
                                    usecols=(1,2)) # load data
            data[namemats]=data_import
            xlabel = 'void fraction'
            xr = [0.0, 1.0]
            yr = [0.0, 200]
            key = [ 'bottom right', 'width -1.5']
            xlog = False
        else:
            if classes == 'newCOFs.csv': continue
            data_import = np.genfromtxt(file_url, delimiter=' ', dtype=None,
                                    usecols=(1,2)) # load data
            #data_import[:,0] *= 1e3
            data[namemats]=data_import
            xlabel = 'crystal density ({/Symbol \664} 10^{3} kg/m^3)'
            xr = [0.0, 2.000]
            yr = [0.0, 200]
            key = [ 'top right', 'width -1.5']
            xlog = False
  #if prop == 'di':
      #data_import = np.genfromtxt(os.path.join(inDir, 'expMOFs.csv'), delimiter=' ', dtype=None,
      #                                  usecols=(1,2)) # load COF data
      #data['expt\'l MOFs'] = data_import
      #data_import = np.genfromtxt(os.path.join(inDir, 'COFs.csv'), delimiter=' ', dtype=None,
      #                                  usecols=(1,2)) # load COF data
      #data['COFs'] = data_import
      data_import = np.genfromtxt(os.path.join(inDir, 'newCOFs.csv'), delimiter=' ', dtype=None,
                                        usecols=(1,2)) # load COF data
      data_import[:,0] /= 1e3
      data['this work'] = data_import
  nSets = len(os.listdir(inDir))
  logging.debug(data) # shown if --log flag given on command line
  # generate plot using ccsgp.make_plot
  make_plot(
    data = data.values(),
    #properties =  [ 'with points pt 18 ps 1.1 lc %s' % my_color_set[i] for i in xrange(nSets) ],
    properties =  [ 'with points pt 18 ps 2.0 lc %s' % my_color_set[i] for i in [5,6] ],
    titles = data.keys(), # use data keys as legend titles
    name = os.path.join(outDir, prop), #gp_calls = [ 'format y %f' ],
    key = key,
      lines = {'x=59.2': 'lc {} lw 4 lt 1'.format(default_colors[-10])},
    ylabel = 'deliverable capacity (v STP/v)',
    xlabel = xlabel, xlog = xlog, ylog = False, xr = xr, yr = yr, rmargin = 0.97, lmargin = 0.15, bmargin = 0.14, size='9.5in,8in'
  )
  return 'done'

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("prop", help="property name = input subdir with txt files, e.g. 'sel'")
  parser.add_argument("mats", help="material classes to plot, e.g. 'COFs' or 'all' for all classes")
  parser.add_argument("--log", help="show log output", action="store_true")
  args = parser.parse_args()
  loglevel = 'DEBUG' if args.log else 'WARNING'
  logging.basicConfig(
    format='%(message)s', level=getattr(logging, loglevel)
  )
  print gp_ch4storage(args.prop, args.mats)

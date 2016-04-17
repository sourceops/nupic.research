# ----------------------------------------------------------------------
# Copyright (C) 2016, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#i
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import multiprocessing
import subprocess
import pprint

def runOneExperiment(args):
  print "In runOneExperiment with", args
  subprocess.call(list(args))
  print "Done with", args


def createExperimentArgs():
  """Run the basic probability of false positives experiment."""
  experimentArguments = []
  for n in [300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300,
            2500, 2700, 2900, 3100, 3300, 3500, 3700, 3900]:
    for a in [64, 128, 256]:
      # Some parameter combinations are just not worth running!
      if ( a==64 and n<=1500 ) or ( a==128 and n<= 1900 ) or ( a==256 ):
        experimentArguments.append(
          ("./sdr_calculations2", "results/temp_"+str(n)+"_"+str(a)+".csv",
           "200000", str(n), str(a), "0"),
        )
  return experimentArguments


def createNoiseExperimentArgs():
  """Run the probability of false negatives with noise experiment."""
  experimentArguments = []
  n = 4000
  for a in [128]:
    for noisePct in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3,
                     0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
                     0.65, 0.7, 0.75, 0.8, 0.85]:
      noise = int(round(noisePct*a,0))
      # Some parameter combinations are just not worth running!
      experimentArguments.append(
        ("./sdr_calculations2",
         "results_noise/temp_"+str(n)+"_"+str(a)+"_"+str(noise)+".csv",
         "200000", str(n), str(a), str(noise))
      )
  return experimentArguments


def mp_handler(numProcesses, experimentArguments):
  print "Running",len(experimentArguments),"experiments with",
  print numProcesses, "processes"
  pool = multiprocessing.Pool(numProcesses)
  pool.map(runOneExperiment, experimentArguments)


if __name__ == '__main__':
  # Uncomment out based on which experiment you want to run:
  # args = createExperimentArgs()
  args = createNoiseExperimentArgs()

  # Run the experiment using 6 processors
  pprint.pprint(args)
  mp_handler(6, args)

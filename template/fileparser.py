import sys, os
import json

if __name__ == '__main__':

  argNames = ['Script', 'Arg1']
  args = dict(zip(argNames, sys.argv))
  cfgName = args['Script'].split('.')[0]
  cfgExt = 'json'

  try:
      with open (cfgName + '.' + cfgExt, 'r') as j:
          cfg = json.load(j)
  except:
      sys.exit()

  if len(args) > 1:
    if os.path.isfile(args['Arg1']):
      with open(args['Arg1'], 'r') as f:
        pass

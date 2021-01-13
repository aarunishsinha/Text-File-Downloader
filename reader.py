import sys
import pandas as pd
import numpy as np
import subprocess

inp = pd.read_csv(sys.argv[1], header = None)
inputs = np.array(inp)
for i in range(np.shape(inputs)[0]):
    url = inputs[i][0]
    num_threads = inputs[i][1]
    print ("For", url)
    host = url.split(':')[1].split('/')[0]
    file = url.split(':')[1].split('/')[1]
    subprocess.run(["python3","downloader.py",str(host),str(num_threads)])

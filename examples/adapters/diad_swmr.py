import tomop
import numpy as np
import scipy.misc
import argparse

import time

import h5py
from swmr_tools import KeyFollower
from swmr_tools.datasource import FrameReader

parser = argparse.ArgumentParser(
    description='Push a diad data set to Slicerecon.')
parser.add_argument('path', metavar='path', help='path to the data')
parser.add_argument(
    '--sample',
    type=int,
    default=1,
    help='the binning to use on the detector, and how many projections to skip'
)
parser.add_argument(
    '--host', default="localhost", help='the projection server host')
parser.add_argument(
    '--port', type=int, default=5558, help='the projection server port')

parser.add_argument(
    '--skipgeometry',
    action='store_true',
    help='assume the geometry packet is already sent')
args = parser.parse_args()

sample = args.sample
print("sample", sample)
path = args.path

start_time = time.time()


key = "/entry1/tomo_entry/data/image_key"
images = "/entry1/tomo_entry/data/data"

time.sleep(5)

with h5py.File(path, "r", libver='latest', swmr=True) as fh:
    k = fh[key][...]
    p = np.argwhere(k == 0)
    d = np.argwhere(k == 2)
    f = np.argwhere(k == 1)
 
    print(k,len(k))

    if len(f) == 0 or len(d) == 0 or len(p) == 0:
        print("Data missing, could not reconstruct")

    proj_count = int(len(p)/sample)
    dark_count = len(d)
    flat_count = len(f)

    pub = tomop.publisher(args.host, args.port)

    lzpro = fh[images]
    ps = lzpro.shape
    print("shape : " + str(ps))

    rows = int(ps[1]/sample)
    cols = int(ps[2]/sample)

    #rows = int(ps[1]/2)
    #cols = int(ps[2]/2)

    print((rows,cols))

    packet_scan_settings = tomop.scan_settings_packet(0, 0, 0, False)
    pub.send(packet_scan_settings)

    window_min_point = [-cols // 2, -cols // 2, -rows // 2]
    window_max_point = [cols // 2, cols // 2, rows // 2]

    pub.send(
        tomop.geometry_specification_packet(0, window_min_point,
                                         window_max_point))

    angles = np.linspace(0, np.pi, proj_count, endpoint=False)
    packet_geometry = tomop.parallel_beam_geometry_packet(0, rows, cols, proj_count, angles)
    pub.send(packet_geometry)

#    keys = "/entry/solstice_scan/keys"
#    finished = "/entry/solstice_scan/scan_finished"

    keys = "/entry1/tomo_entry/data/image_key"
    finished = "/entry1/tomo_entry/data/image_key"


    kf = KeyFollower(fh,[keys],timeout = 10, finished_dataset = finished)

    for kddey in kf:
        print(kddey)

    k = np.append(k, 2)

    kf.check_datasets()

    p_counter = sample -1
    f_counter = 0
    d_counter = 0

    ps_sent = 0
    print("Sending projections " + str(proj_count))

#    for index in kf:
#        nxtomo = k[index]
#        tomopac = abs(nxtomo-2)
#        print("nxtomo is", nxtomo)
#
#        if (nxtomo == 0 and p_counter != sample-1):
#            p_counter = p_counter+1
#            continue
#        elif (nxtomo == 0):
#            p_counter = 0
#            print('111.1')
#
#
#        if nxtomo == 2 and d_counter != 0:
#            continue
#        elif nxtomo == 2:
#            d_counter = 1
#
#        if nxtomo == 1 and f_counter != 0:
#            continue
#        elif nxtomo == 1:
#            f_counter = 1
#
#        print("Reading packet index: " + str(index))
#
#        indps = 0
#        if (nxtomo == 0):
#            indps = ps_sent
#            ps_sent = ps_sent + 1
#        lzpro = None
#        lzpro = fh[images]
#        lzpro.refresh()
#        inmem = lzpro[index, :, :]
#        pac = tomop.projection_packet(
#           tomopac, indps,
#           [rows, cols],
#           np.ascontiguousarray(inmem[::sample, ::sample].flatten()))

    acount = 0
    while (acount < len(k)) and (acount < (len(k)-1)):
        nxtomo = k[acount]
        tomopac = abs(nxtomo-2)

        if (nxtomo == 0 and p_counter != sample-1):
            p_counter = p_counter+1
            continue
        elif (nxtomo == 0):
            p_counter = 0


        if nxtomo == 2 and d_counter != 0:
            continue
        elif nxtomo == 2:
            d_counter = 1

        if nxtomo == 1 and f_counter != 0:
            continue
        elif nxtomo == 1:
            f_counter = 1

        print("Reading packet acount: " + str(acount))
        print("nxtomo is", nxtomo)
        indps = 0
        if (nxtomo == 0):
            indps = ps_sent
            ps_sent = ps_sent + 1
        lzpro = None
        lzpro = fh[images]
        lzpro.refresh()
        inmem = lzpro[acount, :, :]
        pac = tomop.projection_packet(
           tomopac, indps,
           [rows, cols],
           np.ascontiguousarray(inmem[::sample, ::sample].flatten()))
#          np.ascontiguousarray(inmem[::1, ::1           ].flatten()))
        pub.send(pac)

        if (nxtomo == 0 and p_counter != sample-1):
            acount = acount + sample
            continue
        elif (nxtomo == 0):
            acount = acount + sample


        if nxtomo == 2 and d_counter != 0:
            acount = acount + 1
            continue
        elif nxtomo == 2:
            acount = acount + 1

        if nxtomo == 1 and f_counter != 0:
            acount = acount + 1
            continue
        elif nxtomo == 1:
            acount = acount + 1


end_time = time.time()
print(end_time - start_time)

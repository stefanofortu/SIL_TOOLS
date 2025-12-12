import numpy as np
import pandas as pd

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as pll
import matplotlib.cm as mplcm
import matplotlib.colors as mcolors
from matplotlib.transforms import Bbox
from matplotlib.widgets import Button, TextBox, RadioButtons

import io
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage

from datetime import datetime
from datetime import timedelta

import os
import glob

import json

import math
import re
import time

from scipy.interpolate import interp1d

import tempfile

##############################################################

from LDF_Parser_LIB.LDF_Parser import LDF_Parser_Class
from openpyxl.utils import dataframe

##############################################################

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
pd.options.display.max_columns = None
pd.options.display.max_rows = None
# --------------------------------------------------------------------------------

global FilterSelection
global EmphSelection

global OnEdit
global msec_sampling

global LDF_Frames
global dframe_ID

global ann_list

global tref, tri

# *******************************************************************************
# CONSTANTS
# *******************************************************************************
DATA_Types = [
    {
        'type': 'PLIN',
        'ext': '.pdat',
        'header_lines': 1,
        'header_names': ['idx', 'usec', 'Ftype', 'ID', 'len', 'DATA', 'CKS', 'Err'],
        'separator': '\t',
        'dtype': {
            'idx': 'str',
            'usec': 'int64',
            'Ftype': 'str',
            'ID': 'str',
            'len': 'int64',
            'DATA': 'str',
            'CKS': 'str',
            'Err': 'str',
        }
    },
    {
        'type': 'PPLIN',
        'ext': '.ltrc',
        'header_lines': 44,
        'header_names': ['idx', 'usec', 'Ftype', 'ID', 'len', 'DATA', 'CKS', 'CKSType', 'Err'],
        'separator': '[ ][ ]+',
        'dtype': {
            'idx': 'str',
            'usec': 'int64',
            'Ftype': 'str',
            'ID': 'str',
            'len': 'int64',
            'DATA': 'str',
            'CKS': 'str',
            'CKSType': 'str',
            'Err': 'str',
        }
    },
    {
        'type': 'PCAN',  # default ;$FILEVERSION=1.1
        'ext': '.trc',
        'header_lines': 19,
        'header_names': ['idx', 'msec', 'Ftype', 'ID', 'len', 'DATA', 'Err'],
        'separator': '[ ][ ]+',
        'dtype': {
            'idx': 'str',
            'msec': 'float',
            'Ftype': 'str',
            'ID': 'str',
            'len': 'int64',
            'DATA': 'str',
            'Err': 'str',
        }
    },
    {
        'type': 'PCAN_2.0',
        'ext': '.trc',
        'header_lines': 20,
        'header_names': ['idx', 'msec-Type', 'ID-Ftype-len', 'DATA', 'Err'],
        'separator': '[ ][ ]+',
        'dtype': {
            'idx': 'int64',
            'msec-Type': 'str',
            'Type': 'str',
            'ID-Ftype-len': 'str',
            'DATA': 'str',
            'Err': 'str',
        }
    },
    {
        'type': 'Inth',
        'ext': '.data',
        'header_lines': 0,
        'header_names': ['idx', 'msec', 'Ftype', 'ID', 'DATA', 'CKS', 'CKSType', 'Err'],
        'separator': '[ ][ ]+',
        'dtype': {
            'idx': 'str',
            'usec': 'int64',
            'Ftype': 'str',
            'ID': 'str',
            'DATA': 'str',
            'CKS': 'str',
            'CKSType': 'str',
            'Err': 'str',
        }
    },
    {
        'type': 'BUSMASTER',  # default ;$FILEVERSION=1.1
        'ext': '.log',
        'header_lines': 19,
        'header_names': ['time', 'Ftype', 'ch', 'ID', 'ty', 'len', 'DATA'],
        'separator': '[ ][ ]+',
        'dtype': {
            'time': 'str',
            'Ftype': 'str',
            'ch': 'int64',
            'ID': 'str',
            'ty': 'str',
            'len': 'int64',
            'DATA': 'str',
        }
    }
]

global LDF_Frames
global dframe_ID

global FilterSelection
FilterSelection = []
global EmphSelection
EmphSelection = []

global Zoom
global Emphasize
global OnEdit
global msec_sampling
global default_lw
global default_leg

global ann_list
ann_list = []

global tref, tri

global export_type
export_type = 'near-nearest'


# ---------------------------------------------------------------
# Elapsed time function for elaboration time INFOs
def elapsed_time_tic():
    global tref, tri
    tref = [0, 0];
    tri = 1
    tri += 1;
    tri %= 2;
    tref[tri] = time.time()


def elapsed_time_toc():
    global tref, tri
    tri += 1;
    tri %= 2;
    tref[tri] = time.time()
    print("Elapsed time: ", (tref[tri] - tref[(tri + 1) % 2]))


# ---------------------------------------------------------------

def floatHourToTime(fh):
    days, remHours = divmod(fh, 1)
    hours, remMinutes = divmod(remHours * 24, 1)
    minutes, seconds = divmod(remMinutes * 60, 1)
    return (
        int(days),
        int(hours),
        int(minutes),
        int(seconds * 60),
    )

def val2val64_Inth(val):
    if val == 'NaN':
        return pd.NA
    # Big Endian to little endian
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()
    str_little = ''.join(format(x, '02x') for x in little_hex)

    val64 = int(str_little, 16)
    return val64

def DatatoData64(dataIN):
    intDATA = [int(i, 16) if i != 'NaN' else pd.NA for i in dataIN.split()]
    if any([pd.isna(val) for val in intDATA]):
        return pd.NA
    intDATA64 = 0
    for x, val in enumerate(intDATA):
        intDATA64 += val * (2 ** (8 * x))
    return intDATA64


def val64asbig(val64):
    bytes_num = [0, 1, 2, 3, 4, 5, 6, 7]
    val64_bigendian = 0
    for byte_num in bytes_num:
        val64_bigendian += ((val64 >> ((byte_num) * 8)) & 0xFF) << ((7 - byte_num) * 8)
    return val64_bigendian


def prependnan(df):
    IDs = pd.unique(df['ID'])
    print("Found IDs: ", IDs)
    first = True
    for linid in IDs:
        tmpdf = df.iloc[[0]].copy(deep=True)
        tmpdf.iloc[0, df.columns.get_loc("DATA")] = "NaN"
        tmpdf.iloc[0, df.columns.get_loc("ID")] = linid
        tmpdf.index = tmpdf.index - pd.DateOffset(seconds=0.000001)
        if first:
            df0 = tmpdf
            first = False
        else:
            df0 = pd.concat([df0, tmpdf])

    # print(df.head(10))
    df = pd.concat([df0, df])
    # print(df.head(10))
    return df

def insertnans(df, idxs, json_dict):
    IDs = pd.unique(df['ID'])
    print("Found IDs: ", IDs)
    for idx in idxs:
        first = True

        LDF_Frames = [entry for entry in json_dict['LDF_Frames']]
        LDF_Frames_IDs = [entry['ID'] for entry in LDF_Frames]
        LDF_Frames_LENs = [entry['LEN'] for entry in LDF_Frames]

        LDF_Frames_Nodes = [entry['Node'] for entry in LDF_Frames]
        Slaves = json_dict['LDF_Nodes']["Slaves"]
        LDF_Frames_Types = ['Rx' if entry in Slaves else 'Tx' for entry in LDF_Frames_Nodes]

        for linid in IDs:
            if not int(linid, 16) in LDF_Frames_IDs:
                continue
            len = LDF_Frames_LENs[LDF_Frames_IDs.index(int(linid, 16))]
            Ftype = LDF_Frames_Types[LDF_Frames_IDs.index(int(linid, 16))]

            tmpdf = df.iloc[df.index == idx].copy(deep=True)
            tmpdf.iloc[0, df.columns.get_loc("DATA")] = "NaN"
            tmpdf.iloc[0, df.columns.get_loc("ID")] = str(linid)
            tmpdf.iloc[0, df.columns.get_loc("len")] = len
            tmpdf.iloc[0, df.columns.get_loc("Ftype")] = Ftype
            tmpdf.index = tmpdf.index + pd.DateOffset(seconds=0.000001)
            if first:
                df0 = tmpdf
                first = False
            else:
                df0 = pd.concat([df0, tmpdf])

        df = pd.concat([df0, df])
    df = df.sort_index()
    return df

def start_time_calc(time):
    timere = r'(\d+):(\d+):(\d+):(\d+)'
    start_time_ms = int(re.search(timere, time).group(1)) * 60 * 60 * 1000 + \
                    int(re.search(timere, time).group(2)) * 60 * 1000 + \
                    int(re.search(timere, time).group(3)) * 1000 + \
                    int(re.search(timere, time).group(4)) / 10
    return start_time_ms

def DateTimeReIndex(df, Type=None, StartDateTime=None):
    # ----------------------------------------------------------------------------------
    # Convert Time
    # DateTime = [ (start_time_sec +usec*1e-6)/24/60/60 for usec in df['usec']]
    # df['DateTime'] = DateTime
    if len(df) > 0:
        if (Type == 'PLIN'):
            basetime = df['usec'].iloc[0] * 1e-6
            endtime = df['usec'].iloc[-1] * 1e-6
            TimeSec = [(usec * 1e-6) - basetime for usec in df['usec']]
        elif (Type == 'PPLIN'):
            basetime = df['usec'].iloc[1] * 1e-6  # Index to 1 to skip dummy line
            endtime = df['usec'].iloc[-1] * 1e-6
            TimeSec = [(usec * 1e-6) - basetime for usec in df['usec']]
        elif (Type == 'PCAN') or (Type == 'PCAN_2.0'):
            basetime = df['msec'].iloc[1] * 1e-3  # Index to 1 to skip dummy line
            endtime = df['msec'].iloc[-1] * 1e-3
            TimeSec = [(msec * 1e-3) - basetime for msec in df['msec']]
        elif (Type == 'Inth'):
            basetime = df['msec'].iloc[0] * 1e-3
            endtime = df['msec'].iloc[-1] * 1e-3
            TimeSec = [(msec * 1e-3) - basetime for msec in df['msec']]
        elif (Type == 'BUSMASTER'):
            '''FIGLI DI SAEIDIIIIIII'''

        else:
            basetime = None
            endtime = None
            TimeSec = []

        if (Type == 'BUSMASTER'):
            dframe_StartTime = StartDateTime

            start_time0_ms = start_time_calc(df['time'].iloc[0])

            start_time1_ms = start_time_calc(df['time'].iloc[-1])

            dframe_EndTime = StartDateTime + timedelta(milliseconds=(start_time1_ms - start_time0_ms))

            TimeSec = []
            for time in df['time']:
                TimeSec.append(1e-3 * (start_time_calc(time) - start_time0_ms))
        else:
            # ----------------------------------------------------------------------------------
            # Update Start datetime start_dt
            ddays, dhour, dminute, dsecond = floatHourToTime((basetime) / 24 / 60 / 60)
            ddt = timedelta(days=ddays, hours=dhour, minutes=dminute, seconds=dsecond)
            dframe_StartTime = StartDateTime + ddt  # start_dt
            ddays, dhour, dminute, dsecond = floatHourToTime((endtime) / 24 / 60 / 60)
            ddt = timedelta(days=ddays, hours=dhour, minutes=dminute, seconds=dsecond)
            dframe_EndTime = StartDateTime + ddt  # start_dt

        print(dframe_StartTime.strftime('%Y-%m-%d %H:%M:%S'))
        print(dframe_EndTime.strftime('%Y-%m-%d %H:%M:%S'))
        # ----------------------------------------------------------------------------------

        if (Type == 'BUSMASTER'):
            # df['Time[sec]'] = TimeSec
            df['DateTime'] = [pd.Timedelta(seconds=s) + dframe_StartTime for s in TimeSec]
        else:
            df['Time[sec]'] = TimeSec
            # df.set_index(df['Time[sec]']/24/60/60+start_dt)
            # df['Time[days]'] = np.array(TimeSec)/24/60/60
            df['DateTime'] = [pd.Timedelta(seconds=s) + dframe_StartTime for s in TimeSec]
            # df.set_index('Time[days]', inplace=True)
            # print(df.head(10))

        df.set_index('DateTime', inplace=True)
        # print(df.head(10))
    else:
        TimeSec = []

    return (dframe_StartTime, dframe_EndTime)


import re
import json
import sys
from datetime import datetime
import pandas as pd
from pathlib import Path
class PeakLIN_to_MDF:

    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name,
         PATH='C:/logger',
         filename=['C:\\Users\\stefano.fortunati\\Documents\\_TOOLS\\Python\\Pycharm_Projects\\SIL_TOOLS\\lowVoltage.ltrc']
                        ):

        # heuristics / regex patterns:
        # - header lines start with '$' (keywords) or ';' (comments)
        # - data lines: whitespace-separated columns; payload may be a variable-length hex list or text like "Bus event"
        # We attempt to parse common columns: Index, Time, Bus (optional), Type, ID, Data bytes (hex) or Bus event, CK/Checksum or Status

        rx_time = re.compile(r"^\d+\s+([\d:.]+)")  # quick check for a leading index+time
        rx_generic = re.compile(r"""
            ^\s*(?P<frame_number>\d+)\s+                        # index
            (?P<timestamp>[\d:.]+)\s+                           # time offset (ms or ms.us)
            (?:(?P<Direction>\S+)\s+)?                          # optional bus id
            (?P<type>Rx|Tx|EV|ST|Warng|Error|Frame|Msg|Evt)\s+  # message type (common tokens)
            (?P<id>0x[0-9A-Fa-f]+|[0-9A-Fa-f]+)\s+              # ID / PID (hex)
            (?P<rest>.+)$                                       # rest (data bytes or event text)
        """, re.VERBOSE)
        rx_simpler = re.compile(r"""
            ^\s*                                # check all spaces
            (?P<frame_number>\d+)\)             # frame number (e.g. "2)")
            \s+                                 # check all spaces
            (?P<timestamp_us>\d+)               # timestamp in microseconds (digits only)
            \s+                                 
            (?P<direction>Pub|Sub|SubAL|---)    # direction
            \s+
            (?P<frame_id>[0-9A-Fa-f]{1,2}|--)       # frame id (hex 1-2 digits) or '--'
            \s+
            (?P<length>\d+|-)                     # length (digits) or '-' placeholder
            \s+
            (?P<rest>.+)                          # Everything after length (data bytes, checksum, etc.)
            \s*$
        """, re.VERBOSE)


        meta_data = {}
        rows = []
        not_parsed_lines = []
        with open(filename[0], "r", encoding="utf-8", errors="replace") as f:
            for line_num, raw in enumerate(f, start=1):
                line = raw.rstrip("\r\n")
                if not line:
                    continue
                # header/keyword
                if line.startswith("$"):
                    # capture known keywords
                    try:
                        key, val = line.split(None, 1)
                    except ValueError:
                        key, val = line, ""
                    meta_data[key] = val.strip()
                    continue
                # ignore comment lines (often start with ';' in PEAK files)
                if line.lstrip().startswith(";"):
                    print("Line with ; found : ", line)

                # try regex generic
                m = rx_simpler.match(line)
                if m:
                    rec = m.groupdict()
                    '''
                    rest = rec.pop("rest") or ""
                    # try extract data bytes (hex pairs) and checksum tokens like CK, CK1, CK2
                    # data bytes often as hex pairs separated by space: "01 02 03 CK" or "01 02 03 (Bus event)"
                    data_bytes = []
                    ck = ""
                    # split rest by spaces but keep parenthesized text as single token
                    rest_tokens = re.findall(r"\([^)]+\)|\S+", rest)
                    # identify hex bytes (1-2 byte hex)
                    for t in rest_tokens:
                        if re.fullmatch(r"[0-9A-Fa-f]{2}", t):
                            data_bytes.append(t.upper())
                        elif re.fullmatch(r"CK|CK1|CK2|Ck|ck|Checksum|CS", t, re.IGNORECASE):
                            ck = t.upper()
                        else:
                            # could be bus event or status text; keep as extra
                            pass
                    rec['data_bytes'] = " ".join(data_bytes) if data_bytes else ""
                    rec['rest_text'] = rest
                    '''
                    rows.append(rec)
                    continue
                else:
                    not_parsed_lines.append(line)


        df = pd.DataFrame(rows)
        # normalize columns
        for c in ['frame_number', 'timestamp_us', 'direction', 'frame_id', 'length', 'rest']:
            if c not in df.columns:
                print("Error - wrong column names")

        df = df.drop(columns=['frame_number'])
        df = df.drop(columns=['direction'])
        print(df.head(10))

        # Creiamo due DataFrame separati
        df_bus_events = df[df['frame_id'] == '--']
        df_data = df[df['frame_id'] != '--']

        df_data_by_id = {k: v for k, v in df_data.groupby('frame_id')}

        for id_val, group in df_data_by_id.items():
            print(f"ID {id_val} frames:\n", group.head(10), "\n")

    @staticmethod
    def exec_conversion2(input_file_list, use_same_input_file_name, output_file_name,
                        PATH='C:/logger',
                 filename=['C:\\Users\\stefano.fortunati\\Documents\\_TOOLS\\Python\\Pycharm_Projects\\SIL_TOOLS\\lowVoltage.ltrc'],
                 jsonfilename='', verbose=False,
                Type='PPLIN',
                 filter_out=[], filter_sel=[], filter_emph=[], filter_soft=False,
                 plot_filename='', show=True, Limits_Struct=[], Limits_Check=False,
                 export_sampling=None, plot_xlabel='[]', NaNonError=True):
        EXPORT_CSV = False

        types = [t['type'] for t in DATA_Types]
        if not Type in types:
            return None
        print("eccolo")
        f_ext = DATA_Types[types.index(Type)]['ext']
        HEADER_LINES = DATA_Types[types.index(Type)]['header_lines']
        names = DATA_Types[types.index(Type)]['header_names']
        sep = DATA_Types[types.index(Type)]['separator']
        dtype = DATA_Types[types.index(Type)]['dtype']

        # --------------------------------------------------------------------------------
        if filename == '':
            files = [os.path.join(PATH, name) for name in os.listdir(PATH) if name.endswith(f_ext)]
            filename = [max(files, key=os.path.getctime)]
        else:
            if isinstance(filename, list):
                filename = filename
                print(f"filename {filename}")

            else:
                filename = os.path.join(PATH, filename)
                print(f"ERROR - filename not a list")


        # --------------------------------------------------------------------------------
        # Overwrite file types in case of explicit filename definition
        name, extension = os.path.splitext(filename[0])
        exts = [t['ext'] for t in DATA_Types]
        print(f"extension {extension}")
        if extension in exts:
            Type = DATA_Types[exts.index(extension)]['type']
            HEADER_LINES = DATA_Types[exts.index(extension)]['header_lines']
            names = DATA_Types[exts.index(extension)]['header_names']
            sep = DATA_Types[exts.index(extension)]['separator']
            dtype = DATA_Types[exts.index(extension)]['dtype']
        # --------------------------------------------------------------------------------

        do_json_parsing = False
        if do_json_parsing:
            if isinstance(jsonfilename, str):
                if jsonfilename == '':
                    jsonfilename = filename[0].replace(f_ext, '.json')

                name, extension = os.path.splitext(jsonfilename)
                if (extension == '.json' or extension == '.JSON'):
                    with open(jsonfilename, 'r') as j:
                        json_dict = json.loads(j.read())
                elif (extension == '.ldf' or extension == '.LDF'):
                    # print("LDF parsing not yet implemented")
                    try:
                        LDF_parser = LDF_Parser_Class(jsonfilename, 'utf8')
                        LDF_parser.LDFparse(DEBUG=False)
                        LDF = LDF_parser.LDF_Struct
                        json_dict_str = LDF.dump_json(os.path.abspath(jsonfilename + '.json'))
                        json_dict = json.loads(json_dict_str)
                        # json_dict.dump_json("LDF_Struct.json")
                    except:
                        print("LDF Parsing Error")
                        return None

                else:
                    print("Invalid json/Ldf")
                    return None
            else:
                try:
                    LDF_parser = LDF_Parser_Class(jsonfilename)
                    LDF_parser.LDFparse(DEBUG=False)
                    LDF = LDF_parser.LDF_Struct
                    json_dict_str = LDF.dump_json()
                    json_dict = json.loads(json_dict_str)
                except:
                    print("LDF Parsing Error")
                    return None

        # --------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------
        if verbose:
            # print('FILE NAME EXTRACTED: ')        # CHECK FILE NAME
            print(filename)
            print('Importing Data ...')

        # --------------------------------------------------------------------------------
        start_times = []
        start_dts = []

        dframe_StartTime = []
        dframe_EndTime = []

        for y, filen in enumerate(filename):
            file = open(filen, "r")
            print("Searching for $STARTTIME ...")
            start_time = 0
            print("Type" , Type)
            if Type == "BUSMASTER":
                busm_regexp = '^\*\*\*START DATE AND TIME\s+(\d+:\d+:\d+\s+\d+:\d+:\d+:\d+)'
                for x, line in enumerate(file):
                    if x > HEADER_LINES:
                        break
                    if re.match(busm_regexp, line):
                        print("STARTTIME = " + re.search(busm_regexp, line).group(1))
                        try:
                            start_time_str = (re.search(busm_regexp, line).group(1))
                            start_time = pd.to_datetime(start_time_str, format='%d:%m:%Y %H:%M:%S:%f')
                            print(start_time)
                        except:
                            start_time = 0
                        break
            else:
                for x, line in enumerate(file):
                    if x > HEADER_LINES:
                        break
                    if re.match(';\$STARTTIME\s*=\s*(\d+.\d+)', line):
                        print("STARTTIME = " + re.search(';\$STARTTIME\s*=\s*(\d+.\d+)', line).group(1))
                        try:
                            start_time = float(re.search(';\$STARTTIME\s*=\s*(\d+.\d+)', line).group(1))
                            print("STARTTIME = %.16f" % start_time)
                        except:
                            start_time = 0
                        break

            start_times.append(start_time)

            # $FILEVERSION=1.1

            if Type == "PCAN":  # Check only when needed
                file_version = ""
                print("Searching for $FILEVERSION ...")
                file.seek(0)
                for x, line in enumerate(file):
                    if x > HEADER_LINES:
                        break
                    if re.match(';\$FILEVERSION\s*=\s*(\S+)', line):
                        # print("$FILEVERSION = " + re.search(';\$FILEVERSION\s*=\s*(\S+)', line).group(1))
                        try:
                            file_version = re.search(';\$FILEVERSION\s*=\s*(\S+)', line).group(1)
                            print("$FILEVERSION = %.s" % file_version)
                        except:
                            file_version = ""
                        break
                TypeVer = Type + "_" + file_version
                Types = [x['type'] for x in DATA_Types]
                if TypeVer in Types:
                    Type = DATA_Types[Types.index(TypeVer)]['type']
                    HEADER_LINES = DATA_Types[Types.index(TypeVer)]['header_lines']
                    names = DATA_Types[Types.index(TypeVer)]['header_names']
                    sep = DATA_Types[Types.index(TypeVer)]['separator']
                    dtype = DATA_Types[Types.index(TypeVer)]['dtype']

            file.close()

            if Type == "BUSMASTER":
                start_dt = start_time
                print("STARTTIME=" + start_dt.strftime('%Y-%m-%d %H:%M:%S'))
                start_dts.append(start_dt)
            elif Type == "Inth":
                start_dt = datetime.fromordinal(datetime(1970, 1, 1).toordinal() - 0)
                print("STARTTIME=" + start_dt.strftime('%Y-%m-%d %H:%M:%S'))
                start_dts.append(start_dt)
            else:

                start_dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(start_time) - 2)
                ddays, dhour, dminute, dsecond = floatHourToTime(start_time % 1)
                ddt = timedelta(days=ddays, hours=dhour, minutes=dminute, seconds=dsecond)
                start_dt += ddt
                print("STARTTIME=" + start_dt.strftime('%Y-%m-%d %H:%M:%S'))
                start_dts.append(start_dt)
                # --------------------------------------------------------------------------------

            elapsed_time_tic()
            print('Retrieving data ...')
            if Type == 'Inth':
                with open(filen, 'r') as f:
                    lines = f.readlines()
                PeakLIN_to_MDF.elapsed_time_toc()
                print('Retrieving data (reformatting table) ...')

                lines = [re.sub(r'[ ][ ]+', ' ', line) for line in lines]
                lines = [line for line in lines if re.match(r'LIN .*', line)]

                PeakLIN_to_MDF.elapsed_time_toc()
                print('Retrieving data (SpooledTemporaryFile) ...')
                with tempfile.SpooledTemporaryFile(mode='tw+') as ftmp:
                    ftmp.writelines(lines)
                    ftmp.seek(0)
                    PeakLIN_to_MDF.elapsed_time_toc()
                    print('Retrieving data (pd.read_table) ...')

                    df = pd.read_table(filepath_or_buffer=ftmp,
                                       sep=' ', header=0,
                                       names=names,
                                       dtype=dtype,
                                       engine='c')

                    (StartTime, EndTime) = PeakLIN_to_MDF.DateTimeReIndex(df, Type=Type, StartDateTime=start_dt)
                    dframe_StartTime.append(StartTime)
                    dframe_EndTime.append(EndTime)

                    if y == 0:
                        dframe = df
                    else:
                        dframe = pd.concat([dframe, PeakLIN_to_MDF.prependnan(df)])

            elif Type == 'PPLIN':
                #print("here")
                lines = []
                with open(filen, 'r', buffering=1000) as f:
                    # lines = f.readlines()
                    line_count = 0
                    for line in f:
                        lines.append(line)
                        line_count += 1
                        # if line_count > 6000:
                        #    break
                #print("there")
                elapsed_time_toc()
                #print(lines)
                print('Retrieving data (reformatting table) ...')

                lines = [re.sub(r'^\t', '', re.sub(r'[ ][ ]+', "\t", line)) for line in lines]
                lines.insert(HEADER_LINES, '0)\t0\tSub\t00\t1\t00\t00\tEH\tdummy \n')

                elapsed_time_toc()
                print('Retrieving data (SpooledTemporaryFile) ...')
                # print(lines)
                with tempfile.SpooledTemporaryFile(mode='tw+') as ftmp:
                    ftmp.writelines(lines)
                    ftmp.seek(0)
                    elapsed_time_toc()
                    print('Retrieving data (pd.read_table) ...')

                    df = pd.read_table(filepath_or_buffer=ftmp,
                                       sep='\t', header=HEADER_LINES - 1,
                                       names=names,
                                       dtype=dtype,
                                       engine='c')

                    (StartTime, EndTime) = DateTimeReIndex(df, Type=Type, StartDateTime=start_dt)
                    dframe_StartTime.append(StartTime)
                    dframe_EndTime.append(EndTime)
                    #print("dframe.columns", df.columns)

                    if y == 0:
                        dframe = df
                    else:
                        dframe = pd.concat([dframe, prependnan(df)])

            elif Type == 'PCAN':
                with open(filen, 'r') as f:
                    lines = f.readlines()

                elapsed_time_toc()
                print('Retrieving data (reformatting table) ...')

                lines = [re.sub(r'^\t', '', re.sub(r'[ ][ ]+', "\t", line)) for line in lines]
                lines.insert(HEADER_LINES, '0)\t0.0\tDummy\tFFFFFFFF\t1\t00 00 00 00 00 00 00 00\tDUMMY\n')

                elapsed_time_toc()
                print('Retrieving data (SpooledTemporaryFile) ...')
                with tempfile.SpooledTemporaryFile(mode='tw+') as ftmp:
                    ftmp.writelines(lines)
                    ftmp.seek(0)
                    print('Retrieving data (pd.read_table) ...')

                    df = pd.read_table(filepath_or_buffer=ftmp,
                                       sep='\t', header=HEADER_LINES - 1,
                                       names=names,
                                       dtype=dtype,
                                       engine='c')

                    (StartTime, EndTime) = DateTimeReIndex(df, Type=Type, StartDateTime=start_dt)
                    dframe_StartTime.append(StartTime)
                    dframe_EndTime.append(EndTime)

                    if y == 0:
                        dframe = df
                    else:
                        dframe = pd.concat([dframe, prependnan(df)])

            elif Type == 'PCAN_2.0':
                with open(filen, 'r') as f:
                    lines = f.readlines()

                elapsed_time_toc()
                print('Retrieving data (reformatting table) ...')

                lines = [
                    re.sub(r'^\t', '',
                           re.sub(r'[ ][ ]+', "\t",
                                  re.sub(r'[ ]+DT[ ]+', " DT\t", line))) for line in lines]
                # lines = [line for line in lines if not re.match(r'.+ ST\tRx\t.+', line)]
                lines.insert(HEADER_LINES, '0\t0.0 DT\tFFFFFFFF Xx 8\t00 00 00 00 00 00 00 00 \tDUMMY\n')

                elapsed_time_toc()
                print('Retrieving data (SpooledTemporaryFile) ...')

                with open(filen + '.tmp', 'w') as f:
                    f.writelines(lines)

                with tempfile.SpooledTemporaryFile(mode='tw+') as ftmp:
                    ftmp.writelines(lines)
                    ftmp.seek(0)
                    print('Retrieving data (pd.read_table) ...')

                    df = pd.read_table(filepath_or_buffer=ftmp,
                                       sep='\t', header=HEADER_LINES - 1,
                                       names=names,
                                       dtype=dtype,
                                       engine='c')

                    df["msec"] = df["msec-Type"].str.split(" ").str[0].astype(float)
                    df["FT"] = df["msec-Type"].str.split(" ").str[1].astype(str)
                    df["ID"] = df["ID-Ftype-len"].str.split(" ").str[0].astype(str)
                    df["Ftype"] = df["ID-Ftype-len"].str.split(" ").str[1].astype(str)
                    df["len"] = df["ID-Ftype-len"].str.split(" ").str[2].astype(str)

                    (StartTime, EndTime) = DateTimeReIndex(df, Type=Type, StartDateTime=start_dt)
                    dframe_StartTime.append(StartTime)
                    dframe_EndTime.append(EndTime)

                    if y == 0:
                        dframe = df
                    else:
                        dframe = pd.concat([dframe, prependnan(df)])

            elif Type == 'PLIN':
                with open(filen, 'r') as f:
                    lines = f.readlines()

                PeakLIN_to_MDF.elapsed_time_toc()
                print('Retrieving data (reformatting table) ...')

                df = pd.read_table(filepath_or_buffer=filen,
                                   sep='\t', header=HEADER_LINES - 1,
                                   names=names,
                                   dtype=dtype,
                                   engine='c')

                (StartTime, EndTime) = PeakLIN_to_MDF.DateTimeReIndex(df, Type=Type, StartDateTime=start_dt)
                dframe_StartTime.append(StartTime)
                dframe_EndTime.append(EndTime)

                # print(df.head())
                # print(dframe.columns)

                if y == 0:
                    dframe = df
                else:
                    dframe = pd.concat([dframe, PeakLIN_to_MDF.prependnan(df)])

            elif Type == 'BUSMASTER':
                with open(filen, 'r') as f:
                    lines = f.readlines()

                PeakLIN_to_MDF.elapsed_time_toc()
                print('Retrieving data (reformatting table) ...')

                lines = [re.sub(r'[ ]', "\t", line, count=6) for line in lines]
                lines = [line for line in lines if not re.match(r'^\*\*\*.*', line)]

                PeakLIN_to_MDF.elapsed_time_toc()
                print('Retrieving data (SpooledTemporaryFile) ...')
                with tempfile.SpooledTemporaryFile(mode='tw+') as ftmp:
                    ftmp.writelines(lines)
                    ftmp.seek(0)
                    print('Retrieving data (pd.read_table) ...')

                    df = pd.read_table(filepath_or_buffer=ftmp,
                                       sep='\t', header=HEADER_LINES - 1,
                                       names=names,
                                       # dtype=dtype,
                                       engine='c')

                    (StartTime, EndTime) = PeakLIN_to_MDF.DateTimeReIndex(df, Type=Type, StartDateTime=start_dt)
                    dframe_StartTime.append(StartTime)
                    dframe_EndTime.append(EndTime)

                    if y == 0:
                        dframe = df
                    else:
                        dframe = pd.concat([dframe, PeakLIN_to_MDF.prependnan(df)])

            else:
                print('ERROR(PlotData): Unsupported data format')
                exit(1)

            #print(df.head(2))
            #print(tref[tri] - tref[(tri + 1) % 2])
            #print('Retrieving data OK')

        #print("dframe.head")
        # print(dframe.head(2))
        #print("dframe.tail")
        # print(dframe.tail(2))
        # --------------------------------------------------------------------------------
        # Get start/end Time
        StartTime = min(dframe_StartTime)
        EndTime = max(dframe_EndTime)
        DeltaTime = EndTime - StartTime
        print("StartTime: " + StartTime.strftime('%Y-%m-%d %H:%M:%S'))
        print("EndTime: " + EndTime.strftime('%Y-%m-%d %H:%M:%S'))
        print("DeltaTime: " + str(DeltaTime))

        #dframe.to_csv("temp1.csv", sep='\t', decimal=',')

        if Type == 'PCAN_2.0':
            dframe.loc[dframe["FT"] == "ST", "DATA"] = 'NaN'
            dframe.loc[dframe["FT"] == "ST", "ID"] = 'FFFFFFFF'  # dummy ID
            dframe.loc[dframe["FT"] == "ST", "len"] = '0'  # dummy len
            dframe.loc[dframe["FT"] == "EV", "DATA"] = 'NaN'
            dframe.loc[dframe["FT"] == "EV", "ID"] = 'FFFFFFFF'  # dummy ID
            dframe.loc[dframe["FT"] == "EV", "len"] = '0'  # dummy len
            dframe['len'] = df['len'].apply(lambda x: int(x))  # int(value, 16) for value in strArray])
            idxs = dframe.loc[dframe["FT"] == "ST"].index
            #print(len(idxs))
            dframe = PeakLIN_to_MDF.insertnans(dframe, idxs, json_dict)

        # dframe.to_csv("temp2.csv", sep ='\t', decimal=',')

        # --------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------
        dframe['ID'] = dframe['ID'].apply(lambda x: int(x, 16))  # int(value, 16) for value in strArray])
        if (Type == 'PLIN') or (Type == 'Inth'):
            dframe['Err'] = dframe['Err'].apply(lambda x: int(x, 16))  # int(value, 16) for value in strArray])

        # dframe.to_csv("temp3.csv", sep ='\t', decimal=',')

        # --------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------

        # print(dframe.describe())
        #print(dframe.columns.tolist())
        #print(dframe.columns)

        #print(dframe.head(10))

        print('Retrieving data (pd.read_table) (end)')
        elapsed_time_toc()
        print('Encoding HEX ...')
        # --------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------
        # Filter out bus Errors
        # --------------------------------------------------------------------------------
        if NaNonError:
            if (Type == 'PLIN') or (Type == 'Inth'):
                dframe.loc[dframe["Err"] != 0, "DATA"] = 'NaN'
            elif (Type == 'PPLIN' or Type == 'PCAN'):
                dframe.loc[dframe["Err"].notna(), "DATA"] = 'NaN'
            # tmpdf.iloc[ 0 , df.columns.get_loc("DATA")] = "NaN"
        else:
            if (Type == 'PLIN') or (Type == 'Inth'):
                dframe = dframe[dframe['Err'] == 0]  # TODO: Do put Nan instead
            elif (Type == 'PPLIN' or Type == 'PCAN'):
                dframe = dframe[dframe['Err'].isnull()]

        print(dframe.head(5))
        print(dframe.tail(5))

        return
        # --------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------
        # Ged IDs
        # --------------------------------------------------------------------------------
        print('Encoding HEX (end)')
        elapsed_time_toc()
        print("Encoding Frames: ...")

        LDF_Frames = [entry for entry in json_dict['LDF_Frames']]

        LDF_Signals = [entry for entry in json_dict['LDF_Signals']]
        LDF_Signals_Names = [entry['Name'] for entry in json_dict['LDF_Signals']]

        LDF_SignalReprs = [entry for entry in json_dict['LDF_SignalReprs']]

        LDF_Encodings = [entry for entry in json_dict['LDF_Encodings']]
        LDF_Encodings_Names = [entry['Encoder'] for entry in json_dict['LDF_Encodings']]

        if len(filter_sel) > 0:
            for LDF_Frame in LDF_Frames:
                LDF_Frame['FrameSignals'] = [x for x in LDF_Frame['FrameSignals'] if x['Signal'] in filter_sel]
            LDF_Signals = [x for x in LDF_Signals if x['Name'] in filter_sel]
            LDF_Signals_Names = [x['Name'] for x in LDF_Signals if x['Name'] in filter_sel]

        dframe_ID = []
        for x, LDF_Frame in enumerate(LDF_Frames):
            if len(LDF_Frame['FrameSignals']) == 0:
                dframe_ID.append(None)
                continue
            if verbose:
                print("Encoding Frame: '%s'" % LDF_Frame['Name'])
            # df = []
            # df = (dframe[dframe['ID']==LDF_Frame['ID']]).reset_index() # Create data frame filtering by ID
            df = (dframe[dframe['ID'] == LDF_Frame['ID']]).copy(deep=True)

            # ----------------------------------------------------------------------------------
            # convert data
            if (Type == 'Inth'):
                # TODO
                df['DATA'] = df['DATA'].apply(val2val64_Inth)
            else:
                # df['DATA'] = df['DATA'].apply(lambda x: DatatoData64(x))
                df['DATA'] = df['DATA'].apply(DatatoData64)
                # df['DATA64'] = [DatatoData64(val) for val in df['DATA']]

            # ----------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------
            for xx, frmsig in enumerate(LDF_Frame['FrameSignals']):
                if verbose:
                    print("Encoding Signal: '%s'" % frmsig['Signal'])
                sig_name = frmsig['Signal']
                sig_offset = frmsig['BitOffset']

                if sig_name in LDF_Signals_Names:
                    # print("Signal '%s' found" % sig_name)
                    sigsig = LDF_Signals[LDF_Signals_Names.index(sig_name)]
                    sig_bit_mask = ((2 ** sigsig['BitLen']) - 1);
                    sigval = [int(val // (2 ** sig_offset)) & int(sig_bit_mask) if not null else np.nan for val, null in
                              zip(df['DATA'], df['DATA'].isnull())]

                    # Revert Indian if sig_name ends with '_'
                    if sig_name[-1] == '_':
                        bitsh = ((sigsig['BitLen']) % 8)
                        sigval = [
                            val64asbig(val << bitsh) >> (64 + bitsh - sigsig['BitLen']) if not np.isnan(val) else np.nan
                            for
                            val in sigval]

                    df[sig_name + "(raw)"] = sigval
                    # ------------------------------------------------------------------------
                    # Search for encoder
                    encoder_name = ""
                    have_physical = False
                    for repr in LDF_SignalReprs:
                        if sig_name in repr["EncodedSignals"]:
                            encoder_name = repr["Encoder"]
                            break
                    if encoder_name == "":
                        # encoder not found
                        sigphval = sigval
                        ScalePhMaxValue = 2 ** (sigsig['BitLen'])
                        ScalePhMinValue = 0
                    else:
                        # print("Encoder '%s' found" % encoder_name)
                        if encoder_name in LDF_Encodings_Names:
                            LDF_Encoder = LDF_Encodings[LDF_Encodings_Names.index(encoder_name)]
                            # ---- Autoscale here
                            ScalePhMaxValue = -float('inf')
                            ScalePhMinValue = float('inf')
                            # ----
                            if len(LDF_Encoder["PhysicalValues"]) > 0:
                                # try to encode
                                # print("Encoder '%s' PhysicalValues found" % encoder_name)
                                np_sigval = np.array(sigval)
                                np_sigphval = np.array(sigval) * float('nan')
                                for PhysicalValue in LDF_Encoder["PhysicalValues"]:
                                    sel_idx = (np_sigval >= PhysicalValue["MinValue"]) & (
                                            np_sigval <= PhysicalValue["MaxValue"])
                                    np_sigphval[sel_idx] = np_sigval[sel_idx] * PhysicalValue["Scale"] + PhysicalValue[
                                        "Offset"]

                                    # ---
                                    # Autoscale here
                                    # ---

                                    PhMaxValue = PhysicalValue["MaxValue"] * PhysicalValue["Scale"] + PhysicalValue[
                                        "Offset"]
                                    PhMinValue = PhysicalValue["MinValue"] * PhysicalValue["Scale"] + PhysicalValue[
                                        "Offset"]
                                    if PhMaxValue > ScalePhMaxValue:
                                        ScalePhMaxValue = PhMaxValue
                                    if PhMinValue < ScalePhMinValue:
                                        ScalePhMinValue = PhMinValue

                                sigphval = np_sigphval.tolist()
                                have_physical = True

                            else:
                                # print("Encoder '%s' LogicalValues only" % encoder_name)
                                sigphval = sigval

                                # ---
                                # Autoscale here
                                # ---
                                PhMaxValue = sig_bit_mask
                                PhMinValue = 0
                                if PhMaxValue > ScalePhMaxValue:
                                    ScalePhMaxValue = PhMaxValue
                                if PhMinValue < ScalePhMinValue:
                                    ScalePhMinValue = PhMinValue

                                # print(sigphval)
                            # TO DO LOGICAL

                    # ---- Autoscale here
                    FS10 = 10 ** math.ceil(math.log10(ScalePhMaxValue - ScalePhMinValue))
                    sigsig['FS10'] = FS10
                    # ----
                    if encoder_name == "":
                        sigsig['encoded'] = False
                        sigsig['have_physical'] = False
                    else:
                        sigsig['encoded'] = True
                        sigsig['have_physical'] = have_physical

                    df[sig_name + "(ph)"] = sigphval

            dframe_ID.append(df)
        print("data start")
        print(type(dframe_ID))
        for x, LDF_Frame in enumerate(LDF_Frames):
            df = dframe_ID[x]
            df.to_csv(str(LDF_Frame['Name']) + str(".csv"), sep='\t', decimal=',')
        print("data end")
        # LDF_Encodings_Names = [entry['Encoder'] for entry in json_dict['LDF_Encodings']]
        LDF_Signals_FS10 = [entry['FS10'] for entry in LDF_Signals if 'FS10' in entry]
        # print(LDF_Signals_FS10)
        MaxFS10 = max(LDF_Signals_FS10)
        # print(MaxFS10)
        FS10s = list(set(LDF_Signals_FS10))
        # print(FS10s)
        print("Encoding Frames: (END)")
        elapsed_time_toc()

        # df.to_csv("temp3.csv", sep='\t', decimal=',')
        print(dframe_ID[0].head())
        print(dframe_ID[1].head())
        print(len(dframe_ID))

        # exit()
        # --------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------


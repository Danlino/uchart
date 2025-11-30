#!/usr/bin/env python3

from datetime import datetime
from glob import glob
import argparse
import signal
import sys
import os
import re

try:
    "⣾".encode(sys.stdout.encoding)
    USE_BRAILLE = len("⣾") == 1
except Exception:
    USE_BRAILLE = False

if not USE_BRAILLE:
    print("Warning: Braille patterns not supported.", file=sys.stderr)
    sys.exit(78)

def _handle_sigint(signum, frame):
    raise KeyboardInterrupt("Ctrl+C")

signal.signal(signal.SIGINT, _handle_sigint)

def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--height',
                        type=int, default=7, metavar='<NUMBER>',
                        help='Chart height in lines (default: %(default)s)')
    parser.add_argument('-x', '--width',
                        type=int, default=None, dest='width', metavar='<NUMBER>',
                        help='Maximum chart width in characters.')
    parser.add_argument('-m', '--multi',
                        action='store_true', dest='multi_value',
                        help='Plot all individual values instead of just the mean.')
    parser.add_argument('-c', '--column',
                        type=int, default=None, dest='column', metavar='<NUMBER>',
                        help='Specifies which field (column) in the input line to use.')
    parser.add_argument('-l', '--no-legend',
                        action='store_false', dest='show_legend', default=True,
                        help='Do not display the chart legend.')
    parser.add_argument('-n', '--no-stat',
                        action='store_false', dest='show_stat', default=True,
                        help='Do not display the chart stat.')
    parser.add_argument('-t', '--top-value',
                        type=float, default=None, dest='topv', metavar='<NUMBER>',
                        help='Maximum value in chart. (upper limit of Y-axis)')
    parser.add_argument('-b', '--bottom-value',
                        type=float, default=None, dest='bottomv', metavar='<NUMBER>',
                        help='Minimum value in chart. (lower limit of Y-axis)')
    parser.add_argument('-s', '--shift',
                        type=int, default=None, dest='shft', metavar='<NUMBER>',
                        help='Shift decimal point. (e.g. -6 = ÷1_000_000, 3 = ×1_000)')
    parser.add_argument('-a', '--add',
                        type=float, default=0, dest='addm', metavar='<NUMBER>',
                        help='The constant that will be added to each item. (default: %(default)s)')
    parser.add_argument('-f', '--format',
                        type=str, choices=[',', '.'], dest='separator', default=None, metavar='SEP',
                        help="If numbers contain thousands separator, specify it: ',' or '.' (e.g. -f ,)")
    parser.add_argument('file', nargs='*', default=None,
                        help='The input data file, if not specified, is read from stdin.')
    args = parser.parse_args()

    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help()
        sys.exit(0)
    return args

def get_shift(shft: int | None) -> float | int:
    if shft is None or shft == 0:
        return 1
    if not -15 <= shft <= 15:
        return 1
    return 10 ** shft

arg = get_arg()

SHOWLEGEND = arg.show_legend
SHOWSTATS  = arg.show_stat
YHEIGHT    = arg.height
XWIDTH     = arg.width
MULTIV     = arg.multi_value
COLUMN     = arg.column
TOPVAL     = arg.topv
DOWNV      = arg.bottomv
SHFT       = get_shift(arg.shft)
SEPA       = arg.separator
ADDM       = arg.addm

YHEIGHT = 2 if YHEIGHT is not None and YHEIGHT < 2 else YHEIGHT
XWIDTH  = None if XWIDTH is not None and XWIDTH < 1 else XWIDTH
COLUMN  = None if COLUMN is not None and COLUMN < 1 else COLUMN
if TOPVAL is not None and DOWNV is not None and TOPVAL <= DOWNV:
    TOPVAL = DOWNV = None

LEGEND = {'y': 'years >  ',
          'm': 'months > ',
          'd': 'days >   ',
          'H': 'hours >  ',
          'M': 'minutes >',
          'S': 'seconds >',}

ISO_PARTS = [(0,  4, "y"),
             (5,  7, "m"),
             (8, 10, "d"),
             (11,13, "H"),
             (14,16, "M"),
             (17,19, "S"),]

DATE_PARTS = [(0, 4,'y'),
              (5, 7,'m'),
              (8,10,'d'),]

TIME_PARTS = [(0,2,'H'),
              (3,5,'M'),
              (6,8,'S'),]

TS_RE = re.compile( r'^\d{4}-'                # y 0000-9999
                    r'(0[1-9]|1[0-2])-'       # m 01–12
                    r'(0[1-9]|[12]\d|3[01])'  # d 01–31
                    r'T'
                    r'(?:[01]\d|2[0-3])'      # H 00–23
                    r':[0-5]\d'               # M 00–59
                    r':[0-5]\d' )             # S 00–59

DT_RE = re.compile( r'^\d{4}-'                # y 0000-9999
                    r'(0[1-9]|1[0-2])-'       # m 01–12
                    r'(0[1-9]|[12]\d|3[01])') # d 01–31

TM_RE = re.compile( r'^(?:[01]\d|2[0-3])'     # H 01-12
                    r':[0-5]\d'               # M 00-59
                    r':[0-5]\d' )             # S 00-59

def get_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def is_valid(s: str, mode: str) -> bool:
    if   mode == 'timestamp': ftm = "%Y-%m-%dT%H:%M:%S"
    elif mode == 'date':      ftm = "%Y-%m-%d"
    elif mode == 'time':      ftm = "%H:%M:%S"
    else: return False

    try:
        datetime.strptime(s, ftm)
        return True
    except ValueError:
        return False

def create_braille_char(dots):
    base = 0x2800
    value = 0
    for i, dot in enumerate(dots):
        if dot:
            value |= (1 << i)
    return chr(base + value)

def get_dot_for_value(value, row, min_val, max_val, G_HEIGHT):
    if value is None:
        return None

    value_range = max_val - min_val
    if value_range == 0:
        normalized = 0.5
    else:
        normalized = (value - min_val) / value_range
    total_pixels = G_HEIGHT * 4
    pixel_pos = int(normalized * (total_pixels - 1))
    value_row = pixel_pos // 4
    value_row = G_HEIGHT - 1 - value_row

    if value_row != row:
        return None

    y_in_row = pixel_pos % 4
    return y_in_row

def average_values_in_groups(values_list, group_size):
    result = []
    for i in range(0, len(values_list), group_size):
        group = values_list[i:i+group_size]
        if group:
            result.append(sum(group) / len(group))
    return result

def group_values_for_multi(values_list, group_size):
    result = []
    for i in range(0, len(values_list), group_size):
        group = values_list[i:i+group_size]
        if group:
            result.append(group)
    return result

def axis_data(g: list[str], c: int, a: dict) -> None:

    if 1 <= c <= 11 and a['s'] is False:

        if c == 11:
            a['u'] = False
        else:
            amx = [i for i, item in enumerate(g) if is_valid( item[:19], "timestamp" )]
            if len(amx) == 1:
                a['x']['cl'] = amx[0]
                a['x']['fs'] = a['x']['ls'] = g[amx[0]][:19]
                a['s'] = True

            else:

                amd = [i for i, item in enumerate(g) if is_valid( item[:10], "date" )]
                if len(amd) == 1:
                    a['d']['cl'] = amd[0]
                    a['d']['fs'] = a['d']['ls'] = g[amd[0]][:10]
                    a['s'] = True

                amt = [i for i, item in enumerate(g) if is_valid( item[:8], "time" )]
                if len(amt) == 1:
                    a['t']['cl'] = amt[0]
                    a['t']['fs'] = a['t']['ls'] = g[amt[0]][:8]
                    a['s'] = True

    if a['x']['cl'] is not None:
        if g[a['x']['cl']][:19] != a['x']['ls']:
            toend = False
            for s1, s2, l in ISO_PARTS:
                if toend:
                    if a['i'][l]:
                        a['x'][l].append(c)
                else:
                    if a['x']['ls'][s1:s2] != g[a['x']['cl']][s1:s2]:
                        if a['i'][l]:
                            a['x'][l].append(c)
                        toend = True
            a['x']['ls'] = g[a['x']['cl']][:19] 

    else:
        if a['d']['ls'] is not None:
            if g[a['d']['cl']][:10] != a['d']['ls']:
                toend = False
                for s1, s2, l in DATE_PARTS:
                    if toend:
                        if a['i'][l]: a['d'][l].append(c)
                    else:
                        if g[a['d']['cl']][s1:s2] != a['d']['ls'][s1:s2]:
                            if a['i'][l]: a['d'][l].append(c)
                            toend = True
                a['d']['ls'] = g[a['d']['cl']][:10] 

        if a['t']['ls'] is not None:
            if g[a['t']['cl']][:8] != a['t']['ls']:
                toend = False
                for s1, s2, l in TIME_PARTS:
                    if toend:
                        if a['i'][l]: a['t'][l].append(c)
                    else:
                        if g[a['t']['cl']][s1:s2] != a['t']['ls'][s1:s2]:
                            if a['i'][l]: a['t'][l].append(c)
                            toend = True
                a['t']['ls'] = g[a['t']['cl']][:8] 

    if c%10 == 0:

        if a['x']['cl'] is not None:
            for i in ['y','m','d','H','M','S']:
                if len(a['x'][i]) > a['m']:
                    a['x'][i] = []
                    a['i'][i] = False
        else:

            if a['t']['cl'] is not None:
                for i in ['H','M','S']:
                    if len(a['t'][i]) > a['m']:
                        a['t'][i] = []
                        a['i'][i] = False

            if a['d']['cl'] is not None:
                for i in ['y','m','d']:
                    if len(a['d'][i]) > a['m']:
                        a['d'][i] = []
                        a['i'][i] = False

        if a['d']['cl'] is not None:
            if not DT_RE.match( g[a['d']['cl']][:10] ):
                a['e'] += 1

        if a['t']['cl'] is not None:
            if not TM_RE.match( g[a['t']['cl']][:8] ):
                a['e'] += 1

        if a['x']['cl'] is not None:
            if not TS_RE.match( g[a['x']['cl']][:19] ):
                a['e'] += 1

        if a['e'] > 2:
            a['u'] = False

            return None

        if c%100 == 0:

            if a['d']['cl'] is not None:
                if not any( a['i'][k] for k in "ymd" ):
                    a['d'] = { 'cl':None, 'fs': None, 'ls': None, 'y':[], 'm':[], 'd':[] }

            if a['t']['cl'] is not None:
                if not any( a['i'][k] for k in "HMS" ):
                    a['t'] = { 'cl':None, 'fs': None, 'ls': None, 'H':[], 'M':[], 'S':[] }

            if a['x']['cl'] is not None:
                if not any( a['i'][k] for k in "ymdHMS" ):
                    a['t'] = { 'cl':None, 'fs':None, 'ls':None, 'y':[], 'm':[], 'd':[], 'H':[], 'M':[], 'S':[] }

    return None

def print_x_legend(a: dict, l: int, b: int, c: int) -> None:

    if b < 10:
        print(f"{'':>{l}} └{'─' * b}")
        return None

    ml = int(b * 0.5)

    x = { k: a['d' if k in 'ymd' else 't'][k]
          for k in 'ymdHMS'
          if 0 < len(a['d' if k in 'ymd' else 't'][k]) < ml }

    if len(x) == 0:
        print(f"{'':>{l}} └{'─' * b}")
        return None

    if len(x) > 1:
        lkey = max(x, key=lambda k: len(x[k]))
        x = {lkey: x[lkey]}
    else:
        lkey = list(x.keys())[0]


    positions = x[lkey]
    total_braille_cols = 2 * b

    line = [' '] * b

    for pos in positions:
        col = pos // c
        if col >= total_braille_cols:
            continue

        term_col = col // 2
        is_right = col % 2

        bit = 1 << (0 if not is_right else 3)

        current = ord(line[term_col]) - 0x2800 if line[term_col] != ' ' else 0
        new_val = current | bit
        line[term_col] = chr(0x2800 + new_val)

    linex = ''.join(line)
    print(f"{LEGEND[lkey]}{'':>{l-9}} └{'─' * b}")
    print(f"{'':>{l+2}}{linex}")

def reducef(p: list[str], f: int) -> int:
    if len(p) < 2:
        return f

    max_needed = 0

    for i in range(len(p) - 1):
        s1, s2 = p[i], p[i+1]

        if s1.split('.')[0] != s2.split('.')[0]:
            continue

        frac1 = s1.split('.')[1] if '.' in s1 else ''
        frac2 = s2.split('.')[1] if '.' in s2 else ''

        for pos in range(max(len(frac1), len(frac2))):
            c1 = frac1[pos] if pos < len(frac1) else '0'
            c2 = frac2[pos] if pos < len(frac2) else '0'
            if c1 != c2:
                max_needed = max(max_needed, pos + 1)
                break
    return min(max_needed, f)

def am_digit(p: list[str]) -> int:
    return max((len(s.replace('-', '').split('.')[0]) for s in p), default=0)

def negat(p: list[str]) -> bool:
    return any(s.startswith('-0.') for s in p)

def draw_graph(values_for_plot, original_raw_values, compression_factor, long_numbers, long_floatpa, axisx, cl, cv):
    if not values_for_plot:
        return

    if not original_raw_values:
        min_val = min(val for group in values_for_plot for val in (group if isinstance(group, list) else [group]))
        max_val = max(val for group in values_for_plot for val in (group if isinstance(group, list) else [group]))
    else:
        min_val = min(original_raw_values)
        max_val = max(original_raw_values)

    max_val = TOPVAL if TOPVAL is not None else max_val
    min_val = DOWNV if DOWNV is not None else min_val
    value_range = max_val - min_val

    if SHOWSTATS:
        total_original_values = len(original_raw_values)
        num_plot_columns = len(values_for_plot)
        if MULTIV:
            print(f"\n[{total_original_values} values in {num_plot_columns} columns; {compression_factor} values in a column]")
        elif compression_factor == 1:
            print(f"\n[{total_original_values} values]")
        else:
            print(f"\n[{total_original_values} values; average of {compression_factor} values in a column]")

    legend_values = []

    if SHOWLEGEND:
        for i in range(YHEIGHT):
            normalized = 1 - (i / (YHEIGHT - 1))
            val = min_val + normalized * value_range
            legend_values.append(val)

        zend = None
        for row in range(YHEIGHT):
            lg = legend_values[row]
            lz = f"{lg:>{3+long_numbers+3}.{long_floatpa}f}"
            ze = len(lz) - len(lz.rstrip('0'))
            zend = ze if zend is None else zend
            zend = ze if ze < zend else zend

        zend = long_floatpa - zend
        vall = [f"{legend_values[row]:.{zend}f}" for row in range(YHEIGHT)]
        zend = reducef(vall, zend)
        zend = 1 if zend < 1 and am_digit(vall) < 4 else zend
        nega = 1 if negat(vall) and zend == 7 else 0

    for row in range(YHEIGHT):
        line = ""
        if SHOWLEGEND:
            lg = legend_values[row]
            if all( c in '0.-' for c in f"{lg:.{zend}f}" ):
                line += f"{'':{nega+long_numbers+2}}0 │"
            else:
                line += f"{lg:>{3+nega+long_numbers}.{zend}f} │"

        for i in range(0, len(values_for_plot), 2):
            dots = [False] * 8

            if i < len(values_for_plot):
                current_data_left = values_for_plot[i]
                values_to_process = current_data_left if isinstance(current_data_left, list) else [current_data_left]

                for val in values_to_process:
                    y_pos = get_dot_for_value(val, row, min_val, max_val, YHEIGHT)
                    if y_pos is not None:
                        dot_map = [6, 2, 1, 0]
                        dots[dot_map[y_pos]] = True

            if i + 1 < len(values_for_plot):
                current_data_right = values_for_plot[i + 1]
                values_to_process = current_data_right if isinstance(current_data_right, list) else [current_data_right]

                for val in values_to_process:
                    y_pos = get_dot_for_value(val, row, min_val, max_val, YHEIGHT)
                    if y_pos is not None:
                        dot_map = [7, 5, 4, 3]
                        dots[dot_map[y_pos]] = True
            line += create_braille_char(dots)
        print(line)

    if SHOWLEGEND:
        num_braille_chars = (len(values_for_plot) + 1) // 2

        if axisx['u']:
            print_x_legend(axisx, nega+long_numbers+3, num_braille_chars, compression_factor)
        else:
            print(f"{'':>{nega+long_numbers+3}} └{'─' * num_braille_chars}")


def main():
    args = get_arg()
    raw_values = []
    long_numbers = 0
    long_floatpa = 2
    counter_value = 1
    counter_line = 1
    axisx = { 'u':True, 
              's':False,
              'e': 0,
              'm': get_terminal_width() if XWIDTH is None else XWIDTH,
              'd':{ 'cl':None, 'fs':None, 'ls':None, 'y':[], 'm':[], 'd':[] },
              't':{ 'cl':None, 'fs':None, 'ls':None, 'H':[], 'M':[], 'S':[] },
              'x':{ 'cl':None, 'fs':None, 'ls':None, 'y':[], 'm':[], 'd':[], 'H':[], 'M':[], 'S':[] },
              'i':{ k: True for k in ['y', 'm', 'd', 'H', 'M', 'S']}, }

    # 1. pipe
    if not sys.stdin.isatty():
        datain = sys.stdin

    # 2. file or files
    else:
        file_list = []
        for pattern in args.file or []:
            matches = glob(pattern)
            file_list.extend(matches if matches else [pattern])

        if not file_list:
            datain = sys.stdin

        else:
            # more files – but as one stream
            def multi_file_stream(files):
                for f_path in files:
                    with open(f_path, 'r', encoding='utf-8') as f:
                        yield from f

            datain = multi_file_stream(file_list)

    try:
        for line in datain:
            if COLUMN:
                fields = line.split()
                if len(fields) < COLUMN: continue
                line = fields[COLUMN-1]
            if SEPA:
                line = line.replace(SEPA, '')
            line = line.strip().replace(',', '.')
            if line:
                counter_line += 1
                try:
                    value = ( float(line) + ADDM ) * SHFT
                    value = TOPVAL if TOPVAL is not None and value > TOPVAL else value
                    value = DOWNV if DOWNV is not None and value < DOWNV else value
                    if len(str(int(value))) > long_numbers:
                        long_numbers = len(str(int(value)))
                    raw_values.append(value)
                    if axisx['u'] and COLUMN:
                        axis_data(fields, counter_value, axisx)
                    counter_value += 1
                except ValueError:
                    continue

        if long_numbers < 6:
            long_floatpa = 8 - long_numbers
            long_numbers = 6

        if raw_values:
            if XWIDTH is not None and XWIDTH < get_terminal_width() - (long_numbers + 1 + long_floatpa + 2 + 2):
                term_width = XWIDTH
            else:
                term_width = get_terminal_width() - (long_numbers + 1 + long_floatpa + 2 + 2)

            available_braille_chars = term_width if SHOWLEGEND else get_terminal_width() - 2
            if available_braille_chars < 1:
                available_braille_chars = 1
            max_data_columns = available_braille_chars * 2
            compression_factor = 1

            if len(raw_values) > max_data_columns:
                compression_factor = (len(raw_values) + max_data_columns - 1) // max_data_columns
                if compression_factor == 0: compression_factor = 1

            val_for_plot = []
            if MULTIV:
                val_for_plot = group_values_for_multi(raw_values, compression_factor)
            else:
                val_for_plot = average_values_in_groups(raw_values, compression_factor)

            draw_graph(val_for_plot, raw_values, compression_factor, long_numbers, long_floatpa, axisx, counter_line, counter_value)

    except KeyboardInterrupt:
        print(f'\nAfter loading {len(raw_values)} values, it was interrupted by the user.', file=sys.stderr)
        sys.exit(130)

    finally:
        if hasattr(datain, 'close') and datain is not sys.stdin:
            try:
                datain.close()
            except:
                pass  # it is already closed

if __name__ == "__main__":
    main()

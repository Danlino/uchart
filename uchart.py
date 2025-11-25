#!/usr/bin/env python3

import argparse
import signal
import sys
import os

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
    parser.add_argument('file', nargs='?', default=None,
                        help='The input data file, if not specified, is read from stdin.')
    args = parser.parse_args()

    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help()
        sys.exit(0)
    return args

def get_shift_multiplier(shft: int | None) -> float:
    if shft is None or shft == 0:
        return 1.0
    if not -15 <= shft <= 15:
        return 1.0
    return 10.0 ** shft

arg = get_arg()

SHOWLEGEND = arg.show_legend
SHOWSTATS  = arg.show_stat
YHEIGHT    = arg.height
XWIDTH     = arg.width
MULTIV     = arg.multi_value
COLUMN     = arg.column
TOPVAL     = arg.topv
DOWNV      = arg.bottomv
SHFT       = get_shift_multiplier(arg.shft)
SEPA       = arg.separator
ADDM       = arg.addm

YHEIGHT = 2 if YHEIGHT is not None and YHEIGHT < 2 else YHEIGHT
XWIDTH  = None if XWIDTH is not None and XWIDTH < 1 else XWIDTH
COLUMN  = None if COLUMN is not None and COLUMN < 1 else COLUMN
if TOPVAL is not None and DOWNV is not None and TOPVAL <= DOWNV:
    TOPVAL = DOWNV = None

def get_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except:
        return 80

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

def draw_graph(values_for_plot, original_raw_values, compression_factor, long_numbers, long_floatpa):
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
        print(f"{'':>{nega+long_numbers+3}} └{'─' * num_braille_chars}")

def main():
    args = get_arg()
    raw_values = []
    long_numbers = 0
    long_floatpa = 2

    if not sys.stdin.isatty():
        datain = sys.stdin
    elif args.file and args.file != '-':
        try:
            datain = open(args.file, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f"Error: file '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: no permission to read file '{args.file}'.", file=sys.stderr)
            sys.exit(1)
    else:
        datain = sys.stdin

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
                try:
                    value = ( float(line) + ADDM ) * SHFT
                    value = TOPVAL if TOPVAL is not None and value > TOPVAL else value
                    value = DOWNV if DOWNV is not None and value < DOWNV else value
                    if len(str(int(value))) > long_numbers:
                        long_numbers = len(str(int(value)))
                    raw_values.append(value)
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

            processed_values_for_plot = []
            if MULTIV:
                processed_values_for_plot = group_values_for_multi(raw_values, compression_factor)
            else:
                processed_values_for_plot = average_values_in_groups(raw_values, compression_factor)

            draw_graph(processed_values_for_plot, raw_values, compression_factor, long_numbers, long_floatpa)

    except KeyboardInterrupt:
        print(f'\nAfter loading {len(raw_values)} values, it was interrupted by the user.', file=sys.stderr)
        sys.exit(130)

    finally:
        if datain is not sys.stdin:
            datain.close()

if __name__ == "__main__":
    main()

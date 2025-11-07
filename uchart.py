#!/usr/bin/env python3

import argparse
import sys
import os

def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--height',
                        type=int, default=7,
                        help='Chart height in lines (default: %(default)s)')
    parser.add_argument('-x', '--width',
                        type=int, default=0,
                        help='Maximum chart width in characters')
    parser.add_argument('-m', '--merge',
                        action='store_true',
                        help='Do not display average multiple values per column; show all points.')
    parser.add_argument('-l', '--no-legend',
                        action='store_false', dest='show_legend', default=True,
                        help='Do not display the chart legend.')
    parser.add_argument('-s', '--no-stat',
                        action='store_false', dest='show_stat', default=True,
                        help='Do not display the chart stat.')
    parser.add_argument('-t', '--top-value',
                        type=int, default=None, dest='topv',
                        help='Maximum value in chart.')
    parser.add_argument('-d', '--down-value',
                        type=int, default=None, dest='downv',
                        help='Minimum value in chart.')
    return parser.parse_args()

arg = get_arg()
YHEIGHT    = arg.height
XWIDTH     = arg.width
MERGEM     = arg.merge
SHOWLEGEND = arg.show_legend
SHOWSTATS  = arg.show_stat
TOPVAL     = arg.topv
DOWNV      = arg.downv

def get_terminal_width():
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

def group_values_for_merge(values_list, group_size):
    result = []
    for i in range(0, len(values_list), group_size):
        group = values_list[i:i+group_size]
        if group:
            result.append(group)
    return result

def draw_graph(values_for_plot, original_raw_values, compression_factor):
    if not values_for_plot:
        return

    if not original_raw_values:
        min_val = min(val for group in values_for_plot for val in (group if isinstance(group, list) else [group]))
        max_val = max(val for group in values_for_plot for val in (group if isinstance(group, list) else [group]))
    else:
        min_val = min(original_raw_values)
        max_val = max(original_raw_values)

    value_range = max_val - min_val

    if XWIDTH and XWIDTH > 0 and XWIDTH < get_terminal_width() - 17:
        term_width = XWIDTH + 17
    else:
        term_width = get_terminal_width()

    legend_width = 15 if SHOWLEGEND else 0
    available_graph_columns = len(values_for_plot)

    if SHOWSTATS:
        total_original_values = len(original_raw_values)
        num_plot_columns = len(values_for_plot)
        if MERGEM:
            print(f"[Bod = všetky hodnoty z {compression_factor} vstupov, celkovo {total_original_values} hodnôt v {num_plot_columns} stĺpcoch]\n")
        elif compression_factor == 1:
            print(f"[Bod = 1 hodnota, {total_original_values} hodnôt]\n")
        else:
            print(f"[Bod = priemer z {compression_factor} hodnôt, celkovo {total_original_values} hodnôt v {num_plot_columns} stĺpcoch]\n")


    legend_levels = YHEIGHT
    legend_values = []
    if SHOWLEGEND:
        for i in range(legend_levels):
            normalized = 1 - (i / (legend_levels - 1))
            val = min_val + normalized * value_range
            legend_values.append(val)

    for row in range(YHEIGHT):
        line = ""

        if SHOWLEGEND:
            lg = legend_values[row]
            if f"{lg:.2f}" == "-0.00" or f"{lg:.2f}" == "0.00":
                line += f"{'':8}0 │ "
            else:
                line += f"{lg:>9.2f} │ "

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
        print(f"{'':>9} └{'─' * num_braille_chars}")

def main():
    raw_values = []
    try:
        for line in sys.stdin:
            line = line.strip().replace(',', '.')
            if line:
                try:
                    value = float(line)
                    if TOPVAL and value > TOPVAL:
                        value = TOPVAL
                    if DOWNV and value < DOWNV:
                        value = DOWNV
                    raw_values.append(value)
                except ValueError:
                    continue

        if raw_values:
            if XWIDTH and XWIDTH > 0 and XWIDTH < get_terminal_width() - 17:
                term_width = XWIDTH + 17
            else:
                term_width = get_terminal_width()
            legend_width = 15 if SHOWLEGEND else 0
            
            available_braille_chars = term_width - legend_width - 2
            if available_braille_chars < 1:
                available_braille_chars = 1

            max_data_columns = available_braille_chars * 2

            compression_factor = 1

            if len(raw_values) > max_data_columns:
                compression_factor = (len(raw_values) + max_data_columns - 1) // max_data_columns
                if compression_factor == 0: compression_factor = 1

            processed_values_for_plot = []
            if MERGEM:
                processed_values_for_plot = group_values_for_merge(raw_values, compression_factor)
            else:
                processed_values_for_plot = average_values_in_groups(raw_values, compression_factor)

            draw_graph(processed_values_for_plot, raw_values, compression_factor)

    except KeyboardInterrupt:
        if raw_values:
            if XWIDTH and XWIDTH > 0 and XWIDTH < get_terminal_width() - 17:
                term_width = XWIDTH + 17
            else:
                term_width = get_terminal_width()
            legend_width = 15 if SHOWLEGEND else 0
            available_braille_chars = term_width - legend_width - 2
            if available_braille_chars < 1:
                available_braille_chars = 1

            max_data_columns = available_braille_chars * 2
            compression_factor = 1

            if len(raw_values) > max_data_columns:
                compression_factor = (len(raw_values) + max_data_columns - 1) // max_data_columns
                if compression_factor == 0: compression_factor = 1

            processed_values_for_plot = []
            if MERGEM:
                processed_values_for_plot = group_values_for_merge(raw_values, compression_factor)
            else:
                processed_values_for_plot = average_values_in_groups(raw_values, compression_factor)
            
            draw_graph(processed_values_for_plot, raw_values, compression_factor)

if __name__ == "__main__":
    main()

![logo](images/logo.png)
&emsp;&emsp;[install](#installation)&emsp;&emsp;[usage](#usage)

### What <u>uChart</u> is
- A handy helper for quick analysis of raw logs
- Tiny CLI tool for quick charts in the terminal  
- Zero dependencies, single Python script  


It reads data from **standard input (stdin)** or directly from **files** given as positional arguments.  

Terminal requirements: UTF-8 and Unicode support (standard in all modern terminals).

**Data format**
- By default it expects **one number per line**; non-numeric lines are silently ignored.
- When lines contain **multiple** whitespace- or tab-separated columns, use [`-c N`](#usage-column) / [`--column N`](#usage-column) (1-based index) to select which column to plot.


```
$ seq -20 40 | uchart

[61 values]
     40.0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠁
     30.0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠔⠒⠉⠀⠀⠀⠀
     20.0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀
     10.0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    -10.0 │ ⠀⠀⠀⠀⢀⣀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    -20.0 │ ⣀⡠⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          └──────────────────────────────────────
```
- By default, the `uchart` uses the full terminal width for rendering the chart. Using the [`-x`](#usage-width) option, you can set a custom exact width for the chart. This option is suitable for creating a series of charts with the same size.

```
$ seq 130 | awk '{print sin($1/10)}' | uchart -x40 -m

[130 values in 80 columns; 2 values in a column]
      1.0 │⠀⠀⢀⠔⠊⠲⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡰⠒⠒⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      0.7 │⠀⠠⠃⠀⠀⠀⠈⢢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      0.3 │⡠⠃⠀⠀⠀⠀⠀⠀⢃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠆⠀⠀⠀⠀⠀⠀⠨⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡨
        0 │⠂⠀⠀⠀⠀⠀⠀⠀⠀⢃⠀⠀⠀⠀⠀⠀⠀⠀⢀⠌⠀⠀⠀⠀⠀⠀⠀⠀⠡⡀⠀⠀⠀⠀⠀⠀⠀⠀⡨⠀
     -0.3 │⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢃⠀⠀⠀⠀⠀⠀⠀⡌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⠀⠀⠀⠀⡨⠀⠀
     -0.7 │⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢢⠀⠀⠀⠀⠀⡊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⡔⠁⠀⠀
     -1.0 │⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠣⣄⣀⡠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢄⣀⣠⠜⠀⠀⠀⠀
          └─────────────────────────────────────────────────
```
### All values [(-m)](#usage-multy) & Average value

- With [`-m`](#usage-multy):&emsp;all raw values from a column are plotted as separate points
- Without [`-m`](#usage-multy):&emsp;only the arithmetic mean of the column is shown (default)

```bash
awk '/^2025-10-02 15/{print $3}' eufr-2025-10.tsv | uchart -m
```
```
[3600 values in 110 columns; 33 values in a column]
    50.06 │ ⢀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢀⣼⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    50.03 │ ⠿⠿⡇⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⣸⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠋⡇⠿⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢸⡀⠀⢀⠀⠀⠀⠀⠀⠀⢀⢀⡷
    50.01 │ ⠀⠀⠛⣶⣿⠀⠀⠀⠀⢰⠀⠀⠀⢸⢿⠏⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⠀⠀⠻⣇⠀⠀⠀⠀⠀⠀⠀⠀⢸⠿⢷⣷⢿⡿⡄⠀⠀⣰⣰⢸⡾⠇
    49.99 │ ⠀⠀⠀⠿⠹⡇⣀⠀⣴⡾⣴⣶⣰⡞⠈⠀⠸⢦⣠⡀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⢻⡀⠀⠀⠀⢠⣦⢠⣸⠋⠀⠀⠁⠀⠀⣧⡇⣴⢿⡿⡏⠁⠀
    49.97 │ ⠀⠀⠀⠀⠀⠛⠛⣿⠇⠁⠿⠋⠛⠀⠀⠀⠀⠈⠛⢷⣼⣆⢠⢀⠀⢀⣾⠇⠀⠀⠀⠀⠈⢻⣾⣇⣇⡿⢹⡟⠋⠀⠀⠀⠀⠀⠀⠈⠹⠻⠘⠇⠀⠀⠀
    49.94 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠙⠿⣾⣼⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠈⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    49.92 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          └───────────────────────────────────────────────────────────────────
```
```bash
awk '/^2025-10-02 15/{print $3}' eufr-2025-10.tsv | uchart
```
```
[3600 values; average of 33 values in a column]
    50.06 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    50.03 │ ⠊⠉⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠊⠁⠑⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠔
    50.01 │ ⠀⠀⠐⠠⢄⠀⠀⠀⠀⢀⠀⠀⠀⢀⠡⠁⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠄⠡⠤⠢⠔⡀⠀⠀⠀⢀⠐⠌⠀
    49.99 │ ⠀⠀⠀⠁⠀⠄⠀⠀⠠⠄⣀⡠⢀⠄⠀⠀⠀⢄⢀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠄⢀⠠⠁⠀⠀⠀⠀⠀⢀⠄⢀⠊⠄⠄⠀⠀
    49.97 │ ⠀⠀⠀⠀⠀⠈⠉⠔⠁⠀⠀⠀⠁⠀⠀⠀⠀⠀⠁⠡⡠⠄⠀⠀⠀⠀⡠⠀⠀⠀⠀⠀⠀⠑⠔⢂⠂⠒⠠⠂⠁⠀⠀⠀⠀⠀⠀⠀⠐⠁⠀⠀⠀⠀⠀
    49.94 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠌⠤⠐⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    49.92 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          └────────────────────────────────────────────────────────────────────
```
### Decimal point shift & offset

uchart does not use SI prefixes (K, M, G, T) or scientific notation in axis legends.  
With very large or very small numbers, the Y-axis labels would otherwise become excessively wide.

The [`-s`](#usage-shift) / [`--shift`](#usage-shift) option lets you move the decimal point left or right across all values:

- Positive number → shift right (multiply by powers of 10)  
- Negative number → shift left (divide by powers of 10)  

The value itself specifies how many places to shift.

Additionally, the [`-a`](#usage-add) / [`--add`](#usage-add) option adds or subtracts a constant from every value.  
This is especially useful for moving a reference value (e.g. the nominal 50 Hz mains frequency) to zero so deviations are easier to read.

- uchart always performs the addition/subtraction first and only afterwards moves/shifts the decimal point.

##### Example: Display mains frequency deviation in millihertz (centered around 50 Hz)

```
uchart -y11 -c3 -m a-50 -s3 -b-150 -t150 eufr-2025-10.tsv
```

| Switch   | Meaning                             | Result after transformation |
|----------|-------------------------------------|-----------------------------|
| `-y11`   | Chart height in characters          | –                           |
| `-c3`    | Use 3rd column of the file          | e.g. 50.012 Hz              |
| `-m`     | show all points                     | –                           |
| `-a -50` | Subtract 50 from every value        | → 0.012 Hz                  |
| `-s 3`   | Multiply every value by 1000        | → 12 mHz                    |
| `-b -150`| Fixed bottom boundary of the chart  | -150 mHz                    |
| `-t 150` | Fixed top boundary of the chart     | +150 mHz                    |

Result: the chart is perfectly centered around the ideal 50 Hz (the middle line = 0 mHz) and shows frequency deviation in millihertz with a symmetric ±150 mHz range.

![ex1](images/frequency.png)

### X-axis labels
The [`-c`](#usage-column) option selects which column to plot. When enabled, uchart scans each line for a clear timestamp. If a valid and consistent timestamp is found within the first ten lines, it is used to draw time markers below the X-axis.

uchart automatically chooses the best interval that best fits the data, placing a dot at the start of each period. When enough horizontal space is available after a dot, the corresponding value is displayed next to it in subscript form.

---
### Live data preview example

uchart is not designed for real-time streaming, but live visualization can be easily achieved using the `watch` command.

For testing/demo purposes, the following one-liner creates a temporary file `/tmp/pingfile`, fills it with fresh ping latency values every second for one minute, and automatically deletes the file afterwards:
```bash
(for i in {1..60}; do ping -nc1 -W1 8.8.4.4 | grep -o 'time=[0-9.]*' | cut -d= -f2; sleep 1; done ) >> /tmp/pingfile && rm /tmp/pingfile &
```
To monitor the live data stream itself, simply run:
```bash
watch -n1 "tail -30 /tmp/pingfile | uchart"
```
---
### Unified Y-axis scale (multi-chart)
When displaying multiple charts side-by-side, use the same [`-t`](#usage-top) / [`--top`](#usage-top) and [`-b`](#usage-bottom) / [`--bottom`](#usage-bottom) values for all of them.  
This keeps a common Y-axis range and makes the charts visually comparable.

![multi-chart](images/multichart.png)

---
### Aggregated by time unit ( y,m,d,H,M,S )
If the input data contains valid timestamps, **uChart can automatically aggregate (sum) values in the selected column** by a chosen time interval.

All you need to tell uChart is the **time unit** to use for aggregation.  
Specify it right next to the column number after the [`-c`](#usage-column) switch.

**Examples:**
- `-c 1d` → sums all values from the same day
- `-c 1H` → sums all values from the same hour
- `-c 1m` → sums all values from the same month

In the example below, all values fall within a single day, so `-c 1d` aggregates everything into **one bar**.

The screenshot also demonstrates the **debug mode** [`-X`](#usage-debug).  
The two unprocessed lines at the top are simply the header of the input text file.

![sum-data](images/sum_data.png)

## Installation
Linux
```bash
curl -fsSL https://raw.githubusercontent.com/Danlino/uchart/main/install.sh | bash
```

---
### USAGE:
&emsp;uchart [[-h]](#usage-help) [[-v]](#usage-version) [[-y]](#usage-height) [[-x]](#usage-width) [[-m]](#usage-multy) [[-X]](#usage-debug) [[-c]](#usage-column) [[-l]](#usage-legend) [[-n]](#usage-stat) [[-t]](#usage-top) [[-b]](#usage-bottom) [[-s]](#usage-shift) [[-a]](#usage-add) [[-f]](#usage-sep) [file ...] [filters]

_**positional arguments:**_  
**file**  
&emsp;`Input is read from stdin if piped, otherwise from the given file.`
  
**filters**  
&emsp;`Time filters.`  

&emsp;`target=`&emsp;process only entries matching this exact timestamp (or period)  
&emsp;`from=`&emsp;start of the requested period (including this date/time)  
&emsp;`to=`&emsp;end of the requested period (including this date/time)  

&emsp;<ins>Supported formats:</ins>  
&emsp;yyyy&emsp;|&emsp;yyyy-mm&emsp;|&emsp;yyyy-mm-dd&emsp;|&emsp;yyyy-mm-ddThh  
&emsp;|&emsp;yyyy-mm-ddThh:mm&emsp;|&emsp;yyyy-mm-ddThh:mm:ss  

&emsp;<ins>Examples:</ins>  
&emsp;Process only entries in December 2025  
&emsp;`target=2025-12`  

&emsp;Process entries from the beginning of 2025 up to a specific date  
&emsp;`from=2025 to=2025-06-30`  

&emsp;Process only entries on a specific day and hour  
&emsp;`target=2025-12-14T13`  

&emsp;Process everything from December 5, 2025 onwards (until the end of available data)  
&emsp;`from=2025-12-05`  

_**options:**_  

##### -h, --help <a id="usage-help"></a>  
&emsp;`Show help message and exit.`

[^^](#usage)

---
##### -v, --version <a id="usage-version"></a>  
&emsp;`Show program's version number and exit.`

[^^](#usage)

---
##### -y <ins>NUMBER</ins>, --height <ins>NUMBER</ins> <a id="usage-height"></a>  
&emsp;`Chart height in lines. (default: 7)`

Minimum height of the chart is 2 terminal rows. Values less than 2 are forced to 2.

[^^](#usage)

---
##### -x <ins>NUMBER</ins>, --width <ins>NUMBER</ins> <a id="usage-width"></a>  
&emsp;`Maximum chart width in characters.`

Uchart automatically fits the terminal width by default.
Since the X-axis is linear and all columns have the same number of samples, the final width is rounded down. This means the chart may end up substantially narrower than the window.

Using the `-x` / `--width` option, you can set a custom **exact width** for the chart, expressed in the number of terminal characters. For example, with the value -x 20, exactly 40 Braille columns will be displayed. Uchart intelligently divides the input data into 40 groups and displays them.

[^^](#usage)

---
##### -m, --multi <a id="usage-multy"></a>  
&emsp;`Do not display average multiple values per column; show all points.`

By default, when a column contains multiple values, uchart plots only a single point representing the arithmetic mean of all values in that column. This can hide peak/outlier values.
The `-m` / `--multi` flag forces uchart to plot every individual value instead.

[^^](#usage)

---
##### -X, --debug-mode <a id="usage-debug"></a>  
&emsp;`Additional information about the processing of input data.`

[^^](#usage)

---
##### -c <ins>NUMBER[y|m|d|H|M|S]</ins>, --column <ins>NUMBER[y|m|d|H|M|S]</ins> <a id="usage-column"></a>  
&emsp;`Specifies which field (column) in the input line to use.`

By default (without `-c`), **uchart** expects **exactly one numeric value per line**.  
Lines containing multiple values or non-numeric content are silently skipped.

Use the `-c N` / `--column N` option to select a specific column from space- or tab-separated input:

- N is 1-based (first column = 1)
- If a line has fewer than `N` columns, it is skipped

Can now include time unit modifier [**y**]ear, [**m**]onth, [**d**]ay, [**H**]our, [**M**]inute, [**S**]econd. Values within the same time period are **summed** into one bar.

Example: '5**H**' or '**H**5' = total for that **hour** from timestamp data.
This function excels at aggregating and visualizing high volumes of discrete events over time periods. For example: counting errors, requests, or status changes per minute/hour/day in log files.

[^^](#usage)

---
##### -l, --no-legend <a id="usage-legend"></a>  
&emsp;`Do not display the chart legend.`

[^^](#usage)

---
##### -n <ins>TEXT</ins>, --note <ins>TEXT <a id="usage-stat"></a>
&emsp;`Custom chart title. (overrides default stats)`  

If you wish to only remove the line with statistics, enter an empty string `-n ""`  

Uchart can interpret the newline character `\n` and the tab character `\t` in text. It can also include emojis and expand the contents of Bash environment variables.  

```bash
# Let's get the amount of timeout for the last hour
timeout=$(tail -60 ping.txt | grep "timeout" | wc -l)
# We will display the chart
tail -60 ping.txt | uchart -c3 -n "\n 🏓 timeout = ${timeout}/60 values"
```
```
 🏓 timeout = 0/60 values
     39.4 │⠀⠀⠀⠀⠀⠀⠂⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     37.0 │⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     34.6 │⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀
     32.2 │⠀⠀⠀⠀⠀⠠⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⢀
     29.9 │⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠄⠀⠐⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀
     27.5 │⠐⠐⠐⠔⢀⠄⢀⠐⠀⠐⠀⢀⠄⠔⢀⠐⢀⢂⠀⡠⠔⠀⠤⢁⢀⢀⠀⠢⠀⠀
     25.1 │⠁⠂⠁⠀⠁⠀⠀⠀⠔⠀⠊⠄⠈⠀⠁⠀⠀⠀⠄⠀⠀⠐⠀⠀⠀⠁⠈⠀⢄⡀
          └─────────────────────────────────────
```

[^^](#usage)

---
##### -t <ins>NUMBER</ins>, --top-value <ins>NUMBER</ins> <a id="usage-top"></a> 
&emsp;`Maximum value in chart. (upper limit of Y-axis)`

Sets a hard ceiling for displayed values.  
Any value greater than the specified limit is **clipped** and drawn at the top of the chart.

##### -b <ins>NUMBER</ins>, --bottom-value <ins>NUMBER</ins> <a id="usage-bottom"></a>  
&emsp;`Minimum value in chart. (lower limit of Y-axis)`

Same functionality as `-t`, but for the lower boundary.

Useful for:
- preventing extreme spikes from distorting the scale
- focusing on the relevant range
- stabilizing the scale with noisy data

[^^](#usage)

---
##### -s <ins>NUMBER</ins>, --shift <ins>NUMBER</ins> <a id="usage-shift"></a>  
&emsp;`Shift the decimal point left or right. (default: 0)`

uchart does not use scientific notation or SI prefixes (K, M, G…) in the Y-axis legend.  
With very large numbers (e.g. raw byte counts), the legend labels would become excessively wide.

To keep labels short and readable, you can **shift the decimal point** across all data values using the `-s` / `--shift` option:

- The number specifies how many places to shift

**Examples:**
```bash
uchart -s 3  data.txt      # ×1000  (e.g. bytes → kilobytes)
uchart -s 6  data.txt      # ×1M    (bytes → megabytes)
uchart -s -3 data.txt      # ÷1000  (kilobytes → bytes)
```


| Value               | Effect     | Example:          |
|---------------------|------------|-------------------|
| `-s 3`              | ×1000      | 0.012 → 12        |
| `-s 2`              | ×100       | 0.001 → 0.1       |
| `-s 0` or `No Used` | no change  | -                 |
| `-s -1`             | ÷10        | 1000 → 100        |
| `-s -6`             | ÷1000000   | 1000000000 → 1000 |

Range: -15 to +15 (10⁻¹⁵ to 10¹⁵)

- If the entered value is outside this range, the option will be automatically disabled and will have no effect.

[^^](#usage)

---
##### -a <ins>NUMBER</ins>, --add <ins>NUMBER></ins> <a id="usage-add"></a>  
&emsp;`The constant that will be added to each item. (default: 0)`

Option adds or subtracts a constant from every value.

[^^](#usage)

---
##### -f <ins>SEP</ins>, --format <ins>SEP</ins> <a id="usage-sep"></a>  
&emsp;`If numbers contain thousands separator, specify it: ',' or '.' (e.g. -f ,)`

Number formatting varies across the world (e.g. 1,234.56 vs 1.234,56).  
Because of this, uchart cannot always reliably tell which character is the thousands separator and which is the decimal separator.

[^^](#usage)

---
Sample data structure in the examples.
```sh
$ head -3 eufr-2025-10.tsv; echo '...'; tail -3 eufr-2025-10.tsv
2025-10-01 00:00:00	50,04144
2025-10-01 00:00:01	50,035435
2025-10-01 00:00:02	50,02934
...
2025-10-31 23:59:57	50,01183
2025-10-31 23:59:58	50,01234
2025-10-31 23:59:59	50,010765
```


![logo](images/logo.png)

# <u>uchart</u>

**Uchart is** a single-file **terminal command** with no dependencies written in Python. It serves **for simple visualization of a chart** from data read from stdin directly in the terminal. For the proper rendering of the chart, UTF-8 character set support is required. Numeric values must be separated by newlines. One number per line expected; other lines skipped. When input lines contain multiple whitespace- or tab-separated values, the -c N / --column N option selects the N-th column (1-based) for plotting.


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
- By default, the `uchart` uses the full terminal width for rendering the chart. Use the `-x` flag to specify a smaller width.

```
$ seq 130 | awk '{print sin($1/10)}' | uchart -x40 -m

[130 values in 65 columns; 2 values in a column]
      1.0 │ ⠀⠀⡰⠚⠲⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⠒⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      0.7 │ ⠀⠜⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      0.3 │ ⡰⠁⠀⠀⠀⠀⠘⡀⠀⠀⠀⠀⠀⠀⠀⠀⡔⠀⠀⠀⠀⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⢀⠅
        0 │ ⠂⠀⠀⠀⠀⠀⠀⢑⠀⠀⠀⠀⠀⠀⠀⡨⠀⠀⠀⠀⠀⠀⠀⢅⠀⠀⠀⠀⠀⠀⠀⡌⠀
     -0.3 │ ⠀⠀⠀⠀⠀⠀⠀⠀⢃⠀⠀⠀⠀⠀⢠⠁⠀⠀⠀⠀⠀⠀⠀⠈⡄⠀⠀⠀⠀⠀⡨⠀⠀
     -0.7 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠈⢆⠀⠀⠀⢀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⡰⠁⠀⠀
     -1.0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⣀⡠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢄⣀⡴⠁⠀⠀⠀
          └─────────────────────────────────────────
```
### All values (-m) & Average value

- With `-m`: all raw values from a column are plotted as separate points/lines
- Without `-m` (default): only the arithmetic mean of the column is shown

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
### Data scaling & offset

Data can be multiplied by a constant or a constant can be added to (or subtracted from) them before plotting.
In the following example I am displaying the measured mains frequency in Hz. By subtracting 50 (`-a` -50) and then multiplying by 1000 (`-s` 1000), the chart will show the values in millihertz (mHz) while the centre line of the graph represents the ideal value of 50 Hz.

##### Example: Display mains frequency deviation in millihertz (centered around 50 Hz)

```
uchart -c3 -a -50 -s 1000 -b -150 -t 150 -m eufr-2025-10.tsv
```

| Switch   | Meaning                                                                 | Result after transformation |
|----------|--------------------------------------------------------------------------|----------------------------|
| `-c3`    | Use 3rd column of the file                                           | e.g. 50.012 Hz             |
| `-a -50` | Subtract 50 from every value                                             | → 0.012 Hz                 |
| `-s 1000`| Multiply every value by 1000                                              | → 12 mHz                   |
| `-b -150`| Fixed bottom boundary of the chart                                       | -150 mHz                   |
| `-t 150` | Fixed top boundary of the chart                                          | +150 mHz                   |
| `-m`     | show all points              | –                          |

Result: the chart is perfectly centered around the ideal 50 Hz (the middle line = 0 mHz) and shows frequency deviation in millihertz with a symmetric ±150 mHz range.

![ex1](images/frequency.png)


### Live data preview example

`uchart` is not designed for real-time streaming, but live visualization can be easily achieved using the `watch` command.

For testing/demo purposes, the following one-liner creates a temporary file `/tmp/pingfile`, fills it with fresh ping latency values every second for one minute, and automatically deletes the file afterwards:
```bash
(for i in {1..60}; do ping -n -c 1 -W 1 8.8.4.4 | grep -o 'time=[0-9.]*' | cut -d= -f2; sleep 1; done ) >> /tmp/pingfile && rm /tmp/pingfile &
```
To monitor the live data stream itself, simply run:
```bash
watch -n1 "tail -30 /tmp/pingfile | uchart -y5"
```

---
<u>**USAGE:**</u> &emsp;uchart [**-h**] [**-y** <NUMBER>] [**-x** <NUMBER>] [**-m**] [**-l**] [**-n**] [**-t** <NUMBER>] [**-b** <NUMBER>] [**-s** <NUMBER>] [**-a** <NUMBER>] [**-f** SEP] [file]

_**positional arguments:**_
**file**
&emsp;`Input is read from stdin if piped, otherwise from the given file.`

_**options:**_
**-h**, --help  
&emsp;`Show this help message and exit.`

**-y** <ins>NUMBER</ins>, --height <ins>NUMBER</ins>  
&emsp;`Chart height in lines. (default: 7)`

**-x** <ins>NUMBER</ins>, --width <ins>NUMBER</ins>  
&emsp;`Maximum chart width in characters.`

**-m**, --merge  
&emsp;`Do not display average multiple values per column; show all points.`

**-c** <ins>NUMBER</ins>, --column <ins>NUMBER</ins>  
&emsp;`Specifies which field (column) in the input line to use.`

**-l**, --no-legend  
&emsp;`Do not display the chart legend.`

**-n**, --no-stat  
&emsp;`Do not display the chart stat.`

**-t** <ins>NUMBER</ins>, --top-value <ins>NUMBER</ins>  
&emsp;`Maximum value in chart. (upper limit of Y-axis)`

**-b** <ins>NUMBER</ins>, --bottom-value <ins>NUMBER</ins>  
&emsp;`Minimum value in chart. (lower limit of Y-axis)`

**-s** <ins>NUMBER</ins>, --scale <ins>NUMBER</ins>  
&emsp;`Scale factor to multiply all data values by. (default: 1.0)`

**-a** <ins>NUMBER</ins>, --add <ins>NUMBER></ins>
&emsp;`The constant that will be added to each item. (default: 0)`

**-f** <ins>SEP</ins>, --format <ins>SEP</ins>  
&emsp;`If numbers contain thousands separator, specify it: ',' or '.' (e.g. -f ,)`

---
Sample data structure in the example.
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


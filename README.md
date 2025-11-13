# uchart

Uchart is a single-file application with  
no dependencies written in Python.  
It serves for simple visualization  
of a chart from data read from  
stdin directly in the terminal.  
For the proper rendering of  
the chart, UTF-8 character  
set support is required.


```
seq -20 40 | uchart

[61 values]
    40.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠁
    30.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠔⠒⠉⠀⠀⠀⠀
    20.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀
    10.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
   -10.00 │ ⠀⠀⠀⠀⢀⣀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
   -20.00 │ ⣀⡠⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          └───────────────────────────────────────
```

```
seq 0 0.1 13 | awk '{print sin($1)}' | uchart -x40 -m

[131 values in 66 columns; 2 values in a column]
     1.00 │ ⠀⠀⣠⠒⠓⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠒⠲⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     0.67 │ ⠀⠰⠁⠀⠀⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     0.33 │ ⢠⠃⠀⠀⠀⠀⠈⡂⠀⠀⠀⠀⠀⠀⠀⠀⡰⠀⠀⠀⠀⠀⠨⡀⠀⠀⠀⠀⠀⠀⠀⠀⡌
        0 │ ⠆⠀⠀⠀⠀⠀⠀⠘⡀⠀⠀⠀⠀⠀⠀⢠⠁⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⠀⠀⠀⠀⡨⠀
    -0.33 │ ⠀⠀⠀⠀⠀⠀⠀⠀⢑⠀⠀⠀⠀⠀⢀⠅⠀⠀⠀⠀⠀⠀⠀⠀⢅⠀⠀⠀⠀⠀⢠⠁⠀
    -0.67 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⡊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢆⠀⠀⠀⢠⠃⠀⠀
    -1.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠣⣀⣠⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⣀⡠⠃⠀⠀⠀
          └─────────────────────────────────────────
```
### All & Average
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
          └───────────────────────────────────────────────────────
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
          └───────────────────────────────────────────────────────
```
### Big data
```bash
awk '{print $3}' eufr-2025-10.tsv | uchart -m
```
```
[2678400 values in 110 columns; 24350 values in a column]
    50.11 │ ⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⡀⠀⠀⠀⠀⢀⠀⠀⠀
    50.07 │ ⣼⣧⣶⡆⣶⣧⣧⣸⣶⣆⣦⣶⣿⣾⣶⣶⣇⣇⣿⣆⣰⣀⡄⢰⣤⣧⣧⣦⣶⣠⣤⣠⣰⡇⣦⣦⣤⣤⣶⣄⣠⣿⣼⣾⣤⣶⣿⣄⣷⣇⣴⢸⣶⢀⣀
    50.03 │ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    49.98 │ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    49.94 │ ⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⡿⡿⣿⣿⢻⣿⣿⣿⣿⣿⡿⣿⡿⢿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿
    49.90 │ ⠀⠉⠛⠙⠸⡏⡿⢻⡿⡿⠏⠃⠈⠀⠘⠈⠈⠇⡟⠇⠈⠏⢸⠸⠛⠀⡇⠈⠙⠘⠘⠛⠋⡇⠇⠁⢹⠃⠘⢸⢸⠃⡇⡏⠉⢻⠈⠹⠁⠇⠇⠇⠁⠙⠈
    49.86 │ ⠀⠀⠀⠀⠀⠁⠃⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠁⠁⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀
          └───────────────────────────────────────────────────────
```
---
usage: uchart [**-h**] [**-y** HEIGHT] [**-x** WIDTH] [**-m**] [**-l**] [**-n**] [**-t** TOPV] [**-b** BOTTOMV] [**-s** SCALE] [**-f** SEP]


_**options:**_
**-h**, --help
&emsp;`show this help message and exit`

**-y** <ins>NUMBER</ins>, --height <ins>NUMBER</ins>
&emsp;`Chart height in lines (default: 7)`

**-x** <ins>NUMBER</ins>, --width <ins>NUMBER</ins>
&emsp;`Maximum chart width in characters`

**-m**, --merge
&emsp;`Do not display average multiple values per column; show all points`

**-l**, --no-legend
&emsp;`Do not display the chart legend`

**-n**, --no-stat
&emsp;`Do not display the chart stat`

**-t** <ins>NUMBER</ins>, --top-value <ins>NUMBER</ins>
&emsp;`Maximum value in chart (upper limit of Y-axis)`

**-b** <ins>NUMBER</ins>, --bottom-value <ins>NUMBER</ins>
&emsp;`Minimum value in chart (lower limit of Y-axis)`

**-s** <ins>NUMBER</ins>, --scale <ins>NUMBER</ins>
&emsp;`Scale factor to multiply all data values by (default: 1.0)`

**-f** <ins>SEP</ins>, --format <ins>SEP</ins>
&emsp;`If numbers contain thousands separator, specify it: ',' or '.' (e.g. -f ,)`

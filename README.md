# uchart

Uchart is a single-file application with 
no dependencies written in Python. 
It serves for simple visualization 
of a chart from data read from 
stdin directly in the terminal. 
For the proper rendering of 
the chart, UTF-8 character
set support is required.


```sh
seq -20 40 | uchart

[61 values]
    40.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠁
    30.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠔⠒⠉⠀⠀⠀⠀
    20.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀
    10.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        0 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
   -10.00 │ ⠀⠀⠀⠀⢀⣀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
   -20.00 │ ⣀⡠⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          └───────────────────────────────
```

```sh
seq 64 | awk '{print sin($1/10)}' | uchart -y5

[64 values]
     1.00 │ ⠀⠀⠀⢀⡠⠔⠒⠊⠒⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     0.50 │ ⠀⡠⠒⠁⠀⠀⠀⠀⠀⠀⠀⠈⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        0 │ ⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔
    -0.50 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⠁⠀
    -1.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⠤⣀⣀⣀⣀⡠⠔⠊⠀⠀⠀⠀
          └────────────────────────────────
```


```
usage: uchart [-h] [-y HEIGHT] [-x WIDTH] [-m] [-l] [-s] [-t TOPV] [-d DOWNV]

options:
  -h, --help            show this help message and exit
  -y HEIGHT, --height HEIGHT
                        Chart height in lines (default: 7)
  -x WIDTH, --width WIDTH
                        Maximum chart width in characters
  -m, --merge           Do not display average multiple values per column; show all points.
  -l, --no-legend       Do not display the chart legend.
  -s, --no-stat         Do not display the chart stat.
  -t TOPV, --top-value TOPV
                        Maximum value in chart.
  -d DOWNV, --down-value DOWNV
                        Minimum value in chart.
```

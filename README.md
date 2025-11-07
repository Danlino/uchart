# uchart
easy chart

```bash
seq 64 | uchart -s -y5
```
    64.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠤⠒⠊
    48.25 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠤⠔⠒⠉⠉⠀⠀⠀⠀⠀
    32.50 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠤⠤⠒⠊⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    16.75 │ ⠀⠀⠀⠀⠀⠀⠀⣀⡠⠤⠒⠒⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     1.00 │ ⣀⣀⠤⠔⠒⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          └────────────────────────────────────────


```bash
seq 64 | awk '{print sin($1/10)}' | uchart -y5 -s
```

     1.00 │ ⠀⠀⠀⢀⡠⠔⠒⠊⠒⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     0.50 │ ⠀⡠⠒⠁⠀⠀⠀⠀⠀⠀⠀⠈⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        0 │ ⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔
    -0.50 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⠁⠀
    -1.00 │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⠤⣀⣀⣀⣀⡠⠔⠊⠀⠀⠀⠀
          └────────────────────────────────────────

```bash
uchart -h
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

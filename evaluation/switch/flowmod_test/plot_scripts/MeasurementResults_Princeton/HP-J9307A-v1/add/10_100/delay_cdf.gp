set terminal postscript eps enhanced color 'Times-New-Roman,30';
set size ratio 0.625
set output "delay_cdf.eps"
#set ylabel "CDF";
set ylabel "CDF"
set xlabel "delay (ms)" font 'Times New Roman,30'

#set logscale x
set xrange [0:500];
set yrange [0:1];

set key right bottom
set xtics nomirror rotate by -45 font ",30"
#set xtics ("50" 50, "100" 100, "150" 150, "200" 200)

#set key top right
#set title "compute performance comparing"
plot "delay.cdf" using 1:2 title "(X-flow/sec)" with linespoints linetype 2 linecolor 3 linewidth 3 pointtype 1 pointsize 0

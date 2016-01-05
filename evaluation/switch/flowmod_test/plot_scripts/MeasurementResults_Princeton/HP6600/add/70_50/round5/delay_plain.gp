set terminal postscript eps enhanced color 'Times-New-Roman,30';
set size ratio 0.625
set output "delay_plain.eps"
#set ylabel "CDF";
set ylabel "delay (ms)"
set xlabel "modification" font 'Times New Roman,30'

#set logscale x
set xrange [0:1024];
set yrange [0:500];

set key right bottom
set xtics nomirror rotate by -45 font ",30"
#set xtics ("50" 50, "100" 100, "150" 150, "200" 200)

#set key top right
#set title "compute performance comparing"
plot "result.txt" using 1:2 title "(X-flow/sec)" with points  pointtype 1 pointsize 1

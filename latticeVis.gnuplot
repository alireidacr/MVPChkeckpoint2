
set palette grey
#set palette rgbformula 30,13,10
set cblabel "Alive/Dead"
unset cbtics
set xrange [0:99]
set yrange [0:99]
set cbrange[0:1]
set title "Visualisation of the Game of Life"
plot 'latticeState.txt' w image
while (1) {
    pause 0.1
    replot
}

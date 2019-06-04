plot 	"S-02-130mW.txt"  		u ($1):($2-1000*1) w l lw 3
rep 	"S-01-130mW.txt"		u ($1):($2-1000*2) w l lw 3
rep 	"S-03-100mW.txt"  		u ($1):($2-1000*3) w l lw 3
rep 	"S-04-90mW.txt"   		u ($1):($2-1000*4) w l lw 3
rep 	"S-05-60mW.txt"   		u ($1):($2-1000*5) w l lw 3
rep 	"S-06-34mW-10seg.txt"   u ($1):($2/10 -1000*5) w l
rep 	"S-07-129mW-1seg.txt"   u ($1):($2-1000*7) w l


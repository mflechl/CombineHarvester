import os

pcall='for i in hist*C; do echo $i; grep -v ",nan)" $i | sed s\'#exp+#exp#g\' | sed s\'#exp-#exp#g\' | sed s\'#Draw("")#Draw("colz")#g\' > c_$i; done'
os.system(pcall)

# 
# Write 0x44 to cd4/cd5 mmio offset 0x80-0x88
#
mm 0xfed80580 44 -w 1 -mmio -n
mm 0xfed80581 44 -w 1 -mmio -n
mm 0xfed80582 44 -w 1 -mmio -n
mm 0xfed80583 44 -w 1 -mmio -n
mm 0xfed80584 44 -w 1 -mmio -n
mm 0xfed80585 44 -w 1 -mmio -n
mm 0xfed80586 44 -w 1 -mmio -n
mm 0xfed80587 44 -w 1 -mmio -n
mm 0xfed80588 44 -w 1 -mmio -n

stall 1000000
reset

fdisk /dev/mmcblk0 <<EOF
n
p
3
t
3
c
w
EOF

mkfs -t vfat -n ROMS /dev/mmcblk0p3

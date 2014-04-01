fdisk /dev/mmcblk0 <<EOF
n
p
3


t
3
c
w
EOF
partprobe
mkfs -t vfat -n ROMS /dev/mmcblk0p3
mount -o rw,remount /
echo "/dev/mmcblk0p3 /roms vfat ro 0 0" >> /etc/fstab
mount -o ro,remount /

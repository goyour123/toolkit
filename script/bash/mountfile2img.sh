
img=$1
file=$2

mount_path=/mnt/test

sudo mkdir $mount_path
sudo mount $img $mount_path
sudo cp $file $mount_path
sudo umount $mount_path


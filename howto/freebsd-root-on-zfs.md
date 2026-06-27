
# FreeBSD Root-on-ZFS for Dual Boot with Linux

Based on: <https://forums.freebsd.org/threads/uefi-gpt-dual-boot-how-to-install-freebsd-with-zfs-alongside-another-os-sharing-the-same-disk.75734/>

## Manual Partitioning in Shell

```bash
gpart add -t freebsd-swap -a 4k -s 8G -l swap0 nda0
gpart add -t freebsd-zfs -a 4k -l zfs0 nda0

# gpart show
```

```bash
mount -t tmpfs tmpfs /mnt
```

```bash
kldload zfs

# kldstat
```

```bash
zpool create \
    -o altroot=/mnt -o ashift=12 -o autotrim=on \
    -O atime=off -O compression=lz4 -O mountpoint=none -O xattr=sa -O acltype=posixacl \
    zroot /dev/gpt/zfs0

zfs create -o mountpoint=none zroot/ROOT
zfs create -o mountpoint=/ zroot/ROOT/default

zfs create -o mountpoint=/usr -o canmount=off zroot/usr
zfs create zroot/usr/home
zfs create -o setuid=off zroot/usr/ports
zfs create zroot/usr/src

zfs create -o mountpoint=/var -o canmount=off zroot/var
zfs create -o exec=off -o setuid=off zroot/var/audit
zfs create -o exec=off -o setuid=off zroot/var/crash
zfs create -o exec=off -o setuid=off zroot/var/log
zfs create -o atime=on zroot/var/mail
zfs create -o setuid=off zroot/var/tmp

zpool set bootfs=zroot/ROOT/default zroot

# zpool list
# zpool status
# zfs list
```

```bash
ln -s /usr/home /mnt/home
chmod 1777 /mnt/var/tmp
```

```bash
printf 'zfs_enable="YES"\n' >> /tmp/bsdinstall_etc/rc.conf
printf "/dev/gpt/swap0.eli\tnone\tswap\tsw\t0\t0\n" >> /tmp/bsdinstall_etc/fstab
printf "tmpfs\t/tmp\ttmpfs\trw,mode=1777\t0\t0\n" >> /tmp/bsdinstall_etc/fstab
```

```bash
mount -t msdosfs /dev/nda0p1 /media
mkdir -p /media/EFI/freebsd
cp /boot/loader.efi /media/EFI/freebsd/loader.efi
umount /media
```

```bash
exit
```

## rEFInd Configuration

```bash
menuentry "FreeBSD" {
    loader /EFI/freebsd/loader.efi
    icon /EFI/refind/icons/os_freebsd.png
}
```

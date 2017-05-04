# motoflash2sh

This script converts Motorola's Android system images (containing a `flashfile.xml`) to a shell script.

## Install

Use Python 3 `pip` (usually named `pip3`):

```sh
$ pip3 install https://github.com/dlenski/motoflash2sh/archive/v0.1.zip     # tagged version
$ pip3 install https://github.com/dlenski/motoflash2sh/archive/master.zip   # latest commit
```

## Use

1. Unpack zip file containing Motorola system image
2. Run `motoflash2sh` to convert the `flashfile.xml` to `flashfile.sh`
3. Inspect and/or run the `flashfile.sh` to execute the equivalent fastboot commands.

```sh
$ unzip XT1607_HARPIA_RETUS_MPI24.241-2.35-1_cid50_subsidy-DEFAULT_regulatory-DEFAULT_CFC.xml.zip -d /tmp/unpacked
$ motoflash2sh /tmp/unpacked/flashfile.xml
Wrote shell script with 26 fastboot steps to /tmp/unpacked/flashfile.sh
```

## Example output

This is the output for the `flashfile.xml` in the
`XT1607_HARPIA_RETUS_MPI24.241-2.35-1_cid50_subsidy-DEFAULT_regulatory-DEFAULT_CFC.xml.zip` system image:

```sh
#!/bin/sh -x

cd "/tmp/unpacked"

# <header>
#     <phone_model model="harpia" />
#     <software_version version="harpia-user 6.0.1 MPI24.241-2.35-1 1 release-keysM8916_20250106.08.05.23R" />
#     <subsidy_lock_config MD5="00b1a7c46832ca619f9090d3fc80ecce" name="slcf_rev_b_default_v1.0.nvm" />
#     <regulatory_config SHA1="da39a3ee5e6b4b0d3255bfef95601890afd80709" name="regulatory_info_default.png" />
#     <sparsing enabled="true" max-sparse-size="268435456" />
#     <interfaces>
#       <interface name="AP" />
#     </interfaces>
#   </header>

md5sum --check <<EOF || exit 1
61863ba7dac0c512d610ffa6406a50f8 *gpt.bin
8bce118ce20d18f07b8074919a9c760c *bootloader.img
3b273bca1e1206c05d50fbb136168586 *logo.bin
89e6547bcfdca3ec4800d1fdc8220e17 *boot.img
4f73a316fb3ca64f1f6d40840ddcd86c *recovery.img
ecc4eab279c1b23c16a84715fcd986f0 *system.img_sparsechunk.0
50fc3cb4fe688dc1092c1073bc42c6b7 *system.img_sparsechunk.1
b411e841ff3ebf63b56026710121dbd4 *system.img_sparsechunk.2
92901d92792a43a4dcd6f3eeee316d21 *system.img_sparsechunk.3
cebd659e30514298a86d52d25fca6b02 *system.img_sparsechunk.4
4b8342159bd24dc4551509c8b650520c *system.img_sparsechunk.5
d9d2dca4e684b9a8360760751a117b23 *system.img_sparsechunk.6
12fcdd4d23d5ad9d32996ddc6cf984b6 *system.img_sparsechunk.7
c71717415dcce6012858af6af72b27b5 *oem.img
2bb0babde39a5a6df952793c7925daa9 *NON-HLOS.bin
d160f142b2985248f38a29dd77b5bd5a *fsg.mbn
EOF

fastboot getvar max-sparse-size || exit 1
fastboot oem fb_mode_set || exit 1
fastboot flash partition gpt.bin || exit 1
fastboot flash bootloader bootloader.img || exit 1
fastboot flash logo logo.bin || exit 1
fastboot flash boot boot.img || exit 1
fastboot flash recovery recovery.img || exit 1
fastboot flash system system.img_sparsechunk.0 || exit 1
fastboot flash system system.img_sparsechunk.1 || exit 1
fastboot flash system system.img_sparsechunk.2 || exit 1
fastboot flash system system.img_sparsechunk.3 || exit 1
fastboot flash system system.img_sparsechunk.4 || exit 1
fastboot flash system system.img_sparsechunk.5 || exit 1
fastboot flash system system.img_sparsechunk.6 || exit 1
fastboot flash system system.img_sparsechunk.7 || exit 1
fastboot flash oem oem.img || exit 1
fastboot flash modem NON-HLOS.bin || exit 1
fastboot erase modemst1 || exit 1
fastboot erase modemst2 || exit 1
fastboot flash fsg fsg.mbn || exit 1
fastboot erase cache || exit 1
fastboot erase userdata || exit 1
fastboot erase customize || exit 1
fastboot erase clogo || exit 1
fastboot erase DDR || exit 1
fastboot oem fb_mode_clear || exit 1
```

## License

GPLv3 or later

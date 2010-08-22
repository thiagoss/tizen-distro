DESCRIPTION = "utils for managing LZMA compressed files"
HOMEPAGE = "http://tukaani.org/xz/"
SECTION = "base"

LICENSE = "GPLv2+ & GPLv3+ & LGPLv2.1+"
LIC_FILES_CHKSUM = "file://COPYING;md5=c475b6c7dca236740ace4bba553e8e1c \
                    file://COPYING.GPLv2;md5=751419260aa954499f7abaabaa882bbe \
                    file://COPYING.GPLv3;md5=d32239bcb673463ab874e80d47fae504 \
                    file://COPYING.LGPLv2.1;md5=fbc093901857fcd118f065f900982c24 \
                    file://lib/getopt.c;endline=23;md5=2069b0ee710572c03bb3114e4532cd84 "

SRC_URI = "http://tukaani.org/xz/xz-${PV}.tar.gz"

DEPENDS = "gettext"

PR = "r0"

inherit autotools

BBCLASSEXTEND = "native"

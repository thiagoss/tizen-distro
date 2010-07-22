LICENSE = "unknown"
DESCRIPTION = "Tool to sign omap3 x-loader images"

inherit native
SRC_URI = "file://signGP.c"

do_compile() {
	${CC} ${WORKDIR}/signGP.c -o signGP
}

do_install() {
	install -d ${D}${bindir}/
	install -m 0755 signGP ${D}${bindir}/
}

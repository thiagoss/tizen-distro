require clutter-gst.inc

PV = "0.4.0+svnr${SRCREV}"

SRC_URI = "svn://svn.o-hand.com/repos/clutter/trunk;module=${PN};proto=http \
           file://autofoo.patch;patch=1"

S = "${WORKDIR}/${PN}"



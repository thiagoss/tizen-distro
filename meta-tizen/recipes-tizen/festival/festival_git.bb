require festival.inc

PRIORITY = "10"

LIC_FILES_CHKSUM ??= "file://${COMMON_LICENSE_DIR}/GPL-2.0;md5=801f80980d171dd6425610833a22dbe6"

SRC_URI += "git://review.tizen.org/profile/ivi/festival;tag=46c12f13085720f0758c2f205acf9768e22a3f47;nobranch=1"

BBCLASSEXTEND += " native "

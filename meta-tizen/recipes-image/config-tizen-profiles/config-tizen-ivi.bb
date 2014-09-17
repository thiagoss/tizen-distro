LICENSE = "GPL-2.0"
LIC_FILES_CHKSUM ??= "file://${COMMON_LICENSE_DIR}/GPL-2.0;md5=801f80980d171dd6425610833a22dbe6"

SRC_URI = ""
ALLOW_EMPTY_${PN} = "1"

inherit allarch useradd

USERADD_PACKAGES = "${PN}"

GROUPADD_PARAM_${PN} = "-g 100 users; -g 5000 app; -g 54 lock; -g 190 systemd-journal; --system -g 192 weston-launch "

USERADD_PARAM_${PN} += " -u 5000 -d /home/app -m -g users -G users,weston-launch -r -s /bin/sh app "
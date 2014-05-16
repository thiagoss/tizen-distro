DESCRIPTION = "Security server and utilities"
HOMEPAGE = "http://nohomepage.org"
SECTION = "Security/Service"
LICENSE = "Apache-2.0"

SRC_URI = ""

S = "${WORKDIR}/git"

inherit autotools-brokensep

BBCLASSEXTEND += ""
PROVIDES = ""

#PROVIDES by security-server-certs 


#PROVIDES by libsecurity-server-client 


#PROVIDES by security-server 


#PROVIDES by security-server-dev 


#PROVIDES by libsecurity-server-client-dev 


RDEPENDS = ""
#RDEPENDS of security-server-certs (${PN}-certs)
RDEPENDS_${PN}-certs += "security-server"

#RDEPENDS of libsecurity-server-client (lib${PN}-client)
RDEPENDS_lib${PN}-client += "eglibc"
RDEPENDS_lib${PN}-client += "security-server"

#RDEPENDS of libsecurity-server-client-dev (lib${PN}-client-dev)
RDEPENDS_lib${PN}-client-dev += "libprivilege-control-dev"
RDEPENDS_lib${PN}-client-dev += "libsecurity-server-client"

#RDEPENDS of security-server-dev (${PN}-dev)
RDEPENDS_${PN}-dev += "security-server"

#RDEPENDS of security-server (${PN})
RDEPENDS_${PN} += "systemd"


DEPENDS = ""
#DEPENDS of security-server 
DEPENDS += "systemd"
DEPENDS_append_class-native = " cmake-native"
DEPENDS_append_class-target = " cmake-native"
DEPENDS += "attr"
DEPENDS += "zip"
DEPENDS += "openssl"
DEPENDS += "dlog"
DEPENDS += "smack"
DEPENDS += "libcap"
DEPENDS += "libprivilege-control"

do_prep() {
 cd ${S}
 chmod -Rf a+rX,u+w,g-w,o-w ${S}
 #setup -q
 cp ${S}/packaging/security-server.manifest .
 cp ${S}/packaging/libsecurity-server-client.manifest .
 
 
}
do_patch_append() {
    bb.build.exec_func('do_prep', d)
}

do_configure() {
}

do_compile() {
 cd ${S}
 LANG=C
 export LANG
 unset DISPLAY
 CFLAGS="-O2 -g -m64 -fmessage-length=0 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables" ; export CFLAGS ; 
 CXXFLAGS="${CXXFLAGS:--O2 -g -m64 -fmessage-length=0 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables}" ; export CXXFLAGS ; 
 FFLAGS="${FFLAGS:--O2 -g -m64 -fmessage-length=0 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables -I%_fmoddir}" ; export FFLAGS ; 
 LD_AS_NEEDED=1; export LD_AS_NEEDED ; 
 
 
 export LDFLAGS+="-Wl,--rpath=${prefix}/lib"
 
 
   CFLAGS="${CFLAGS:--O2 -g -m64 -fmessage-length=0 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables}" ; export CFLAGS ; 
   CXXFLAGS="${CXXFLAGS:--O2 -g -m64 -fmessage-length=0 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables}" ; export CXXFLAGS ; 
   FFLAGS="${FFLAGS:--O2 -g -m64 -fmessage-length=0 -D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables}" ; export FFLAGS ; 
   cmake \
         -DCMAKE_VERBOSE_MAKEFILE=ON \
         -DCMAKE_INSTALL_PREFIX:PATH=${prefix} \
         -DCMAKE_INSTALL_LIBDIR:PATH=${prefix}/lib \
         -DINCLUDE_INSTALL_DIR:PATH=${prefix}/include \
         -DLIB_INSTALL_DIR:PATH=${prefix}/lib \
         -DSYSCONF_INSTALL_DIR:PATH=${sysconfdir} \
         -DSHARE_INSTALL_PREFIX:PATH=${prefix}/share \
         -DCMAKE_SKIP_RPATH:BOOL=ON \
         -DBUILD_SHARED_LIBS:BOOL=ON . -DVERSION=0.0.118 \
         -DCMAKE_BUILD_TYPE=RELEASE \
         -DCMAKE_VERBOSE_MAKEFILE=ON
 make -j16
 
 
 
}

do_install() {
 echo export RPM_BUILD_ROOT=${D}
 cd ${S}
 LANG=C
 export LANG
 unset DISPLAY
 rm -rf ${D} 
 mkdir -p ${D} 
 
 rm -rf ${D}
 mkdir -p ${D}/usr/share/license
 cp LICENSE ${D}/usr/share/license/security-server
 cp LICENSE ${D}/usr/share/license/libsecurity-server-client
 mkdir -p ${D}/etc/security/
 cp security-server-audit.conf ${D}/etc/security/
 
   oe_runmake \
         DESTDIR=${D} \
         INSTALL_ROOT=${D} \
         BINDIR=${prefix}/bin \
   install  
   rm -f ${D}${infodir}/dir 
   find ${D} -regex ".*\.la$" | xargs rm -f -- 
   find ${D} -regex ".*\.a$" | xargs rm -f --
 
 mkdir -p ${D}/usr/lib/systemd/system/multi-user.target.wants
 mkdir -p ${D}/usr/lib/systemd/system/sockets.target.wants
 ln -s ../security-server.service ${D}/usr/lib/systemd/system/multi-user.target.wants/security-server.service
 ln -s ../security-server-data-share.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-data-share.socket
 ln -s ../security-server-get-gid.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-get-gid.socket
 ln -s ../security-server-privilege-by-pid.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-privilege-by-pid.socket
 ln -s ../security-server-cookie-get.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-cookie-get.socket
 ln -s ../security-server-cookie-check.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-cookie-check.socket
 ln -s ../security-server-app-privilege-by-name.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-app-privilege-by-name.socket
 ln -s ../security-server-password-check.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-password-check.socket
 ln -s ../security-server-password-set.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-password-set.socket
 ln -s ../security-server-password-reset.socket ${D}/usr/lib/systemd/system/sockets.target.wants/security-server-password-reset.socket
 
 
}

PACKAGES += " libsecurity-server-client "
PACKAGES += " libsecurity-server-client-dev "

security-server_files = ""
security-server_files += "security-server.manifest"
security-server_files += "/usr/bin/security-server"
security-server_files += "${prefix}/lib/libsecurity-server-commons.so.*"
security-server_files += "/usr/lib/systemd/system/multi-user.target.wants/security-server.service"
security-server_files += "/usr/lib/systemd/system/security-server.service"
security-server_files += "/usr/lib/systemd/system/security-server.target"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-data-share.socket"
security-server_files += "/usr/lib/systemd/system/security-server-data-share.socket"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-get-gid.socket"
security-server_files += "/usr/lib/systemd/system/security-server-get-gid.socket"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-privilege-by-pid.socket"
security-server_files += "/usr/lib/systemd/system/security-server-privilege-by-pid.socket"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-cookie-get.socket"
security-server_files += "/usr/lib/systemd/system/security-server-cookie-get.socket"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-cookie-check.socket"
security-server_files += "/usr/lib/systemd/system/security-server-cookie-check.socket"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-app-privilege-by-name.socket"
security-server_files += "/usr/lib/systemd/system/security-server-app-privilege-by-name.socket"
security-server_files += "/etc/security/security-server-audit.conf"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-password-check.socket"
security-server_files += "/usr/lib/systemd/system/security-server-password-check.socket"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-password-set.socket"
security-server_files += "/usr/lib/systemd/system/security-server-password-set.socket"
security-server_files += "/usr/lib/systemd/system/sockets.target.wants/security-server-password-reset.socket"
security-server_files += "/usr/lib/systemd/system/security-server-password-reset.socket"
security-server_files += "${prefix}/share/license/security-server"

libsecurity-server-client_files = ""
libsecurity-server-client_files += "libsecurity-server-client.manifest"
libsecurity-server-client_files += "${prefix}/lib/libsecurity-server-client.so.*"
libsecurity-server-client_files += "${prefix}/share/license/libsecurity-server-client"

libsecurity-server-client-dev_files = ""
libsecurity-server-client-dev_files += "security-server.manifest"
libsecurity-server-client-dev_files += "${prefix}/lib/libsecurity-server-client.so"
libsecurity-server-client-dev_files += "${prefix}/lib/libsecurity-server-commons.so"
libsecurity-server-client-dev_files += "/usr/include/security-server/security-server.h"
libsecurity-server-client-dev_files += "${prefix}/lib/pkgconfig/*.pc"

FILES_${PN} = "${security-server_files}"
FILES_lib${PN}-client = "${libsecurity-server-client_files}"
FILES_lib${PN}-client-dev = "${libsecurity-server-client-dev_files}"

PKG_security-server= "security-server"
PKG_libsecurity-server-client= "libsecurity-server-client"
PKG_libsecurity-server-client-dev= "libsecurity-server-client-dev"

require security-server-extraconf.inc

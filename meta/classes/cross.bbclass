# Cross packages are built indirectly via dependency,
# no need for them to be a direct target of 'world'
EXCLUDE_FROM_WORLD = "1"

# Save PACKAGE_ARCH before changing HOST_ARCH
OLD_PACKAGE_ARCH := ${PACKAGE_ARCH}
PACKAGE_ARCH = ${OLD_PACKAGE_ARCH}

PACKAGES = ""

HOST_ARCH = "${BUILD_ARCH}"
HOST_VENDOR = "${BUILD_VENDOR}"
HOST_OS = "${BUILD_OS}"
HOST_PREFIX = "${BUILD_PREFIX}"
HOST_CC_ARCH = "${BUILD_CC_ARCH}"

CPPFLAGS = "${BUILD_CPPFLAGS}"
CFLAGS = "${BUILD_CFLAGS}"
CXXFLAGS = "${BUILD_CFLAGS}"
LDFLAGS = "${BUILD_LDFLAGS}"
LDFLAGS_build-darwin = "-L${STAGING_LIBDIR_NATIVE}"

# Set the compiler. It could have been set to something else
export CC = "${CCACHE}${HOST_PREFIX}gcc ${HOST_CC_ARCH}"
export CXX = "${CCACHE}${HOST_PREFIX}g++ ${HOST_CC_ARCH}"
export F77 = "${CCACHE}${HOST_PREFIX}g77 ${HOST_CC_ARCH}"
export CPP = "${HOST_PREFIX}gcc -E"
export LD = "${HOST_PREFIX}ld"
export CCLD = "${CC}"
export AR = "${HOST_PREFIX}ar"
export AS = "${HOST_PREFIX}as"
export RANLIB = "${HOST_PREFIX}ranlib"
export STRIP = "${HOST_PREFIX}strip"


# Overrides for paths

# Path prefixes
base_prefix = "${exec_prefix}"
prefix = "${CROSS_DIR}"
exec_prefix = "${prefix}"

# Base paths
base_bindir = "${base_prefix}/bin"
base_sbindir = "${base_prefix}/bin"
base_libdir = "${base_prefix}/lib"

# Architecture independent paths
datadir = "${prefix}/share"
sysconfdir = "${prefix}/etc"
sharedstatedir = "${prefix}/com"
localstatedir = "${prefix}/var"
infodir = "${datadir}/info"
mandir = "${datadir}/man"
docdir = "${datadir}/doc"
servicedir = "${prefix}/srv"

# Architecture dependent paths
bindir = "${exec_prefix}/bin"
sbindir = "${exec_prefix}/bin"
libexecdir = "${exec_prefix}/libexec"
libdir = "${exec_prefix}/lib"
includedir = "${exec_prefix}/include"
oldincludedir = "${exec_prefix}/include"

do_stage () {
	oe_runmake install
}

do_install () {
	:
}

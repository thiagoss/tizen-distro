SRC_URI += " file://0001-Update-autoconf-macros.patch "
SRC_URI += " file://0002-Do-not-set-gcrypt-thread-callback.patch "
SRC_URI += " file://0003-Remove-obsolete-function-gcry_md_start_debug.patch "

gpg2_files += "/usr/lib/gpg2keys_kdns"
gpg2_files += "/usr/lib/gpg-protect-tool"
gpg2_files += "/usr/lib/gpg-check-pattern"
gpg2_files += "/usr/lib/gpg2keys_finger"
gpg2_files += "/usr/lib/gnupg-pcsc-wrapper"
gpg2_files += "/usr/lib/gpg2keys_hkp"
gpg2_files += "/usr/lib/gpg2keys_curl"
gpg2_files += "/usr/lib/gpg-preset-passphrase"

EXTRA_OECONF += " --disable-doc"
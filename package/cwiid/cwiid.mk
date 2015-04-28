################################################################################
#
# cwiid
#
################################################################################

CWIID_VERSION = 0.6.00
CWIID_SOURCE = cwiid-$(CWIID_VERSION).tgz
CWIID_SITE = http://abstrakraft.org/cwiid/downloads
CWIID_LICENSE = GPLv2+
CWIID_LICENSE_FILES = COPYING

CWIID_AUTORECONF = YES
CWIID_INSTALL_STAGING = YES

CWIID_DEPENDENCIES = host-pkgconf host-bison host-flex bluez_utils python

CWIID_CONF_OPTS = --disable-ldconfig

CWIID_MAKE = $(MAKE1)

CWIID_MAKE_ENV = STAGING_DIR=$(STAGING_DIR) \
	HOST_DIR=$(HOST_DIR) \
	TARGET_CC=$(TARGET_CC)

ifeq ($(BR2_PACKAGE_CWIID_WMGUI),y)
CWIID_DEPENDENCIES += libgtk2 libglib2
CWIID_CONF_OPTS += --enable-wmgui
else
CWIID_CONF_OPTS += --disable-wmgui
endif

$(eval $(autotools-package))

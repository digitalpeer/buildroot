#############################################################
#
# rpio_pwm
#
#############################################################

RPIO_PWM_VERSION = 40398925117df6be77f9b433cdca7cfe5fb13552
RPIO_PWM_SITE = git@github.com:metachris/raspberrypi-pwm.git
RPIO_PWM_SITE_METHOD = git

define RPIO_PWM_BUILD_CMDS
	(cd $(@D); \
		$(TARGET_CC) rpio-pwm/rpio_pwm.c -o rpio_pwm; \
	)
endef

define RPIO_PWM_CLEAN_CMDS
	rm $(@D)/rpio-pwm/rpio_pwm
endef

define RPIO_PWM_INSTALL_TARGET_CMDS
	$(INSTALL) -D $(@D)/rpio_pwm $(TARGET_DIR)/usr/bin/rpio_pwm
endef

define RPIO_PWM_UNINSTALL_TARGET_CMDS
	rm -f $(TARGET_DIR)/usr/bin/rpio_pwm
endef

$(eval $(generic-package))

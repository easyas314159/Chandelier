SOURCE=$(shell pwd)

CONFIG=/etc/chandelier
INITD=/etc/init.d/chandelier
COMMON=/usr/share/chandelier
LOGS=/var/log/chandelier

.PHONY: all install

all:

install: $(CONFIG) $(COMMON) $(LOGS) $(INITD)

i2c:
	sed -i.bak '/^[^#].*i2c-bcm2708/s/^/#/' /etc/modprobe.d/raspi-blacklist.conf
	grep -q 'i2c-dev' /etc/modules || echo "i2c-dev" >> /etc/modules

$(CONFIG):
	cp default.config $(CONFIG)
	ln -fs $(CONFIG) config

$(INITD): i2c
	apt-get install python-daemon python-smbus i2c-tools
	ln -fs $(COMMON)/chandelier.sh $(INITD)
	update-rc.d chandelier defaults

$(COMMON):
	ln -fs $(SOURCE) $(COMMON)

$(LOGS):
	mkdir $(LOGS)

clean:
	rm -f *.pyc
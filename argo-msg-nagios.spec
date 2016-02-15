Summary: Bridge from Nagios to the MSG Messaging system
Name: argo-msg-nagios
Version: 1.0.1
Release: 1%{?dist}
License: APL2
Group: Network/Monitoring
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch
Requires: perl(GridMon) >= 1.0.70
Requires: msg-utils
Requires: perl(No::Worries)
Obsoletes: msg-nagios-bridge

%description

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install --directory ${RPM_BUILD_ROOT}/usr/libexec/%{name}
install --mode 755 ./handle_service_check  ${RPM_BUILD_ROOT}/usr/libexec/%{name}
install --mode 755 ./handle_service_change  ${RPM_BUILD_ROOT}/usr/libexec/%{name}
install --mode 755 ./send_to_msg  ${RPM_BUILD_ROOT}/usr/libexec/%{name}
install --mode 755 ./recv_from_queue  ${RPM_BUILD_ROOT}/usr/libexec/%{name}
install --mode 755 ./check_config  ${RPM_BUILD_ROOT}/usr/libexec/%{name}
install --directory ${RPM_BUILD_ROOT}/usr/sbin
install --mode 755 ./msg-clean-spool ${RPM_BUILD_ROOT}/usr/sbin
install --mode 755 ./msg-to-handler ${RPM_BUILD_ROOT}/usr/sbin
install --mode 755 ./msg-to-handler.chk ${RPM_BUILD_ROOT}/usr/sbin
install --mode 755 ./nagios-notifications ${RPM_BUILD_ROOT}/usr/sbin
install --mode 755 ./send-to-dashboard ${RPM_BUILD_ROOT}/usr/sbin
install --directory ${RPM_BUILD_ROOT}/etc/init.d
install --mode 755 ./init.d/msg-to-handler ${RPM_BUILD_ROOT}/etc/init.d
install --directory ${RPM_BUILD_ROOT}/etc/cron.hourly
install --mode 755 ./msg-to-handler.chk ${RPM_BUILD_ROOT}/etc/cron.hourly
install --directory ${RPM_BUILD_ROOT}/etc/sysconfig
install --mode 644 ./msg-to-handler.sysconfig ${RPM_BUILD_ROOT}/etc/sysconfig/msg-to-handler
install --directory ${RPM_BUILD_ROOT}/etc/msg-to-handler.d
install --mode 644 ./msg-to-handler.conf ${RPM_BUILD_ROOT}/etc
install --directory ${RPM_BUILD_ROOT}/var/cache/msg/config-cache
touch ${RPM_BUILD_ROOT}/var/cache/msg/config-cache/config.db
install --directory ${RPM_BUILD_ROOT}/var/run/msg-to-handler
install --directory ${RPM_BUILD_ROOT}/var/spool/%{name}/outgoing
install --directory ${RPM_BUILD_ROOT}/var/spool/%{name}/incoming
install --directory ${RPM_BUILD_ROOT}/var/spool/%{name}/outgoing_alarms
install --directory ${RPM_BUILD_ROOT}/var/spool/%{name}/undelivered-messages
install --directory ${RPM_BUILD_ROOT}/var/spool/%{name}/outgoing-messages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/libexec/%{name}/handle_service_check
/usr/libexec/%{name}/handle_service_change
/usr/libexec/%{name}/send_to_msg
/usr/libexec/%{name}/recv_from_queue
/usr/libexec/%{name}/check_config
/usr/sbin/msg-clean-spool
/usr/sbin/msg-to-handler
/usr/sbin/msg-to-handler.chk
/usr/sbin/nagios-notifications
/usr/sbin/send-to-dashboard
/etc/init.d/msg-to-handler
/etc/cron.hourly/msg-to-handler.chk
%config /etc/sysconfig/msg-to-handler
%config %attr(0644,nagios,nagios) /var/cache/msg/config-cache/config.db
%config %attr(0644,root,root) /etc/msg-to-handler.conf
%dir /etc/msg-to-handler.d
%dir %attr(0770,nagios,nagios) /var/cache/msg/config-cache
%dir %attr(0770,nagios,nagios) /var/run/msg-to-handler
%dir %attr(0770,nagios,nagios) /var/spool/%{name}/outgoing
%dir %attr(0770,nagios,nagios) /var/spool/%{name}/incoming
%dir %attr(0770,nagios,nagios) /var/spool/%{name}/outgoing_alarms
%dir %attr(0770,nagios,nagios) /var/spool/%{name}/undelivered-messages
%dir %attr(0770,nagios,nagios) /var/spool/%{name}/outgoing-messages

%pre
if ! /usr/bin/id nagios &>/dev/null; then
    /usr/sbin/useradd -r -m -d /var/log/nagios -s /bin/sh -c "nagios" nagios || \
        logger -t nagios/rpm "Unexpected error adding user \"nagios\". Aborting installation."
fi
if ! /usr/bin/getent group nagiocmd &>/dev/null; then
    /usr/sbin/groupadd nagiocmd &>/dev/null || \
        logger -t nagios/rpm "Unexpected error adding group \"nagiocmd\". Aborting installation."
fi

%post
/sbin/chkconfig --add msg-to-handler
[ -x /usr/sbin/msg-clean-spool ] && /usr/sbin/msg-clean-spool >/dev/null 2>&1
if [ $1 = "2" ]; then
   /sbin/service msg-to-handler condrestart
fi
:

%preun
if [ "$1" = 0 ]; then
   /sbin/service msg-to-handler stop
   /sbin/chkconfig --del msg-to-handler
fi
:

%changelog
* Mon Feb 15 2016 Emir Imamagic <eimamagi@srce.hr> - 1.0.1-1%{?dist}
- Removed MRS related bits
- Added tennant support
- Fixed default settings
* Mon Sep 21 2015 Emir Imamagic <eimamagi@srce.hr> - 1.0.0-1%{?dist}
- Initial version based on msg-nagios-bridge

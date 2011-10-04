Summary: Network monitoring tools including ping
Name: iputils
Version: 20101006
Release: 9
License: BSD
URL: http://www.skbuff.net/iputils
Group: System/Daemons

Source0: http://www.skbuff.net/iputils/%{name}-s%{version}.tar.bz2
Source1: ifenslave.tar.gz

Patch0: iputils-20020927-rh.patch
Patch1: iputils-20020124-countermeasures.patch
Patch2: iputils-20020927-addrcache.patch
Patch3: iputils-20020927-ping-subint.patch
Patch4: iputils-ping_cleanup.patch
Patch5: iputils-ifenslave.patch
Patch6: iputils-20070202-idn.patch
Patch7: iputils-20070202-traffic_class.patch
Patch8: iputils-20070202-ia64_align.patch
Patch9: iputils-20071127-warnings.patch
Patch10: iputils-20071127-corr_type.patch
Patch11: iputils-msg-format.patch
Patch12: iputils-20071127-infiniband.patch
Patch13: iputils-20100418-convtoint.patch
Patch14: iputils-20100418-flowlabel.patch
Patch15: iputils-20101006-drop_caps.patch
Patch16: iputils-20101006-unused.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libidn-devel
BuildRequires: openssl-devel
BuildRequires: libcap-devel
BuildRequires: xz-libs

%description
The iputils package contains basic utilities for monitoring a network,
including ping. The ping command sends a series of ICMP protocol
ECHO_REQUEST packets to a specified network host to discover whether
the target machine is alive and receiving network traffic.

%prep
%setup -q -a 1 -n %{name}-s%{version}

%patch0 -p1 -b .rh
%patch1 -p1 -b .countermeasures
%patch2 -p1 -b .addrcache
%patch3 -p1 -b .ping-subint
%patch4 -p1 -b .cleanup
%patch5 -p1 -b .addr
%patch6 -p1 -b .idn
%patch7 -p1 -b .traffic_class
%patch8 -p1 -b .ia64_align
%patch9 -p1 -b .warnings
%patch10 -p1 -b .corr_type
%patch11 -p1 -b .format
%patch12 -p1 -b .infiniband
%patch13 -p1 -b .convtoint
%patch14 -p1 -b .flowlabel
%patch15 -p1 -b .drop_caps
%patch16 -p1 -b .unused

%build
%ifarch s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIE -Werror"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -Werror"
%endif
export LDFLAGS="-pie"
make %{?_smp_mflags} arping clockdiff ping ping6 rdisc tracepath tracepath6
gcc -Wall $RPM_OPT_FLAGS ifenslave.c -o ifenslave

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}/{bin,sbin}
install -c clockdiff		${RPM_BUILD_ROOT}%{_sbindir}/
install -cp arping		${RPM_BUILD_ROOT}/sbin/
ln -s /sbin/arping		${RPM_BUILD_ROOT}%{_sbindir}/arping
install -cp ping		${RPM_BUILD_ROOT}/bin/
install -cp ifenslave		${RPM_BUILD_ROOT}/sbin/
install -cp rdisc		${RPM_BUILD_ROOT}/sbin/
install -cp ping6		${RPM_BUILD_ROOT}/bin/
install -cp tracepath		${RPM_BUILD_ROOT}/bin/
install -cp tracepath6		${RPM_BUILD_ROOT}/bin/

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
ln -sf /bin/ping6 ${RPM_BUILD_ROOT}%{_sbindir}
ln -sf /bin/tracepath ${RPM_BUILD_ROOT}%{_sbindir}
ln -sf /bin/tracepath6 ${RPM_BUILD_ROOT}%{_sbindir}

iconv -f ISO88591 -t UTF8 RELNOTES -o RELNOTES.tmp
touch -r RELNOTES RELNOTES.tmp
mv -f RELNOTES.tmp RELNOTES



%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc RELNOTES README.bonding
%{_sbindir}/clockdiff
/sbin/arping
%{_sbindir}/arping
%attr(4755,root,root) /bin/ping
/sbin/ifenslave
/sbin/rdisc
%attr(4755,root,root) /bin/ping6
/bin/tracepath
/bin/tracepath6
%{_sbindir}/ping6
%{_sbindir}/tracepath
%{_sbindir}/tracepath6


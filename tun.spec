#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
# TODO: UP/SMP
%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?_with_smp:-smp}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	Universal TUN/TAP device driver
Summary(pl):	Uniwersalny sterownik urz±dzeñ TUN/TAP
Name:		tun
Version:	1.1
Release:	1
License:	GPL
Group:		Base/Kernel
Source0:	http://vtun.sourceforge.net/tun/%{name}-%{version}.tar.gz
URL:		http://vtun.sourceforge.net/tun/
BuildRequires:	perl
%{!?_without_dist_kernel:BuildRequires:	kernel-headers < 2.3.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TUN/TAP provides packet reception and transmission for user space
programs. It can be viewed as a simple Point-to-Point or Ethernet
device, which instead of receiving packets from a physical media,
receives them from user space program and instead of sending packets
via physical media writes them to the user space program.

%description -l pl
TUN/TAP zapewnia przyjmowanie i transmisjê pakietów dla programów
user-space. Mo¿e byæ widziany jako zwyk³e urz±dzenie Point-to-Point
lub Ethernet, które zamiast otrzymywania pakietów z fizycznego medium
otrzymuje je od programu i zamiast wysy³ania pakietów przez fizyczne
medium wysy³a je do programu.

%package -n kernel%{smpstr}-net-tun
Summary:	Universal TUN/TAP device driver
Summary(pl):	Uniwersalny sterownik urz±dzeñ TUN/TAP
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}

%description -n kernel%{smpstr}-net-tun
TUN/TAP provides packet reception and transmission for user space
programs. It can be viewed as a simple Point-to-Point or Ethernet
device, which instead of receiving packets from a physical media,
receives them from user space program and instead of sending packets
via physical media writes them to the user space program.

%description -n kernel%{smpstr}-net-tun -l pl
TUN/TAP zapewnia przyjmowanie i transmisjê pakietów dla programów
user-space. Mo¿e byæ widziany jako zwyk³e urz±dzenie Point-to-Point
lub Ethernet, które zamiast otrzymywania pakietów z fizycznego medium
otrzymuje je od programu i zamiast wysy³ania pakietów przez fizyczne
medium wysy³a je do programu.

%prep
%setup -q

%build
%if %{smp}
CFLAGS="%{rpmcflags} -D__KERNEL_SMP=1"
%endif
%configure2_13 \
	--with-kernel=%{_kernelsrcdir}
touch .config
mkdir arch
touch arch/Makefile
%{__make} \
%if %{smp}
	CONFIG_SMP=y \
%endif
	KDIR=`pwd` \
	ARCH="" \
	HPATH=%{_kernelsrcdir}/include

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net

install linux/tun.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net

install -d $RPM_BUILD_ROOT/dev
perl -pi -e "s|/dev|$RPM_BUILD_ROOT/dev|g;" linux/create_dev
%{__make} -C linux dev

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{smpstr}-net-tun
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun	-n kernel%{smpstr}-net-tun
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%files -n kernel%{smpstr}-net-tun
%defattr(644,root,root,755)
%doc FAQ README ChangeLog
%attr(644,root,root) /lib/modules/%{_kernel_ver}/net/tun.o*
%attr(600,root,root) /dev/*

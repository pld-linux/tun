# TODO: UP/SMP
#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?with_smp:-smp}
%define		smp		%{?with_smp:1}%{!?with_smp:0}
Summary:	Universal TUN/TAP device driver
Summary(pl.UTF-8):   Uniwersalny sterownik urządzeń TUN/TAP
Name:		tun
Version:	1.1
Release:	1
License:	GPL
Group:		Base/Kernel
Source0:	http://vtun.sourceforge.net/tun/%{name}-%{version}.tar.gz
# Source0-md5:	b270be81ff9b743d9e9031b0b1a36ebe
URL:		http://vtun.sourceforge.net/tun/
%{?with_dist_kernel:BuildRequires:	kernel-headers < 2.3.0}
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TUN/TAP provides packet reception and transmission for user space
programs. It can be viewed as a simple Point-to-Point or Ethernet
device, which instead of receiving packets from a physical media,
receives them from user space program and instead of sending packets
via physical media writes them to the user space program.

%description -l pl.UTF-8
TUN/TAP zapewnia przyjmowanie i transmisję pakietów dla programów
user-space. Może być widziany jako zwykłe urządzenie Point-to-Point
lub Ethernet, które zamiast otrzymywania pakietów z fizycznego medium
otrzymuje je od programu i zamiast wysyłania pakietów przez fizyczne
medium wysyła je do programu.

%package -n kernel%{smpstr}-net-tun
Summary:	Universal TUN/TAP device driver
Summary(pl.UTF-8):   Uniwersalny sterownik urządzeń TUN/TAP
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Conflicts:	kernel < %{_kernel_ver}
Conflicts:	kernel > %{_kernel_ver}
Conflicts:	kernel-%{?with_smp:up}%{!?with_smp:smp}

%description -n kernel%{smpstr}-net-tun
TUN/TAP provides packet reception and transmission for user space
programs. It can be viewed as a simple Point-to-Point or Ethernet
device, which instead of receiving packets from a physical media,
receives them from user space program and instead of sending packets
via physical media writes them to the user space program.

%description -n kernel%{smpstr}-net-tun -l pl.UTF-8
TUN/TAP zapewnia przyjmowanie i transmisję pakietów dla programów
user-space. Może być widziany jako zwykłe urządzenie Point-to-Point
lub Ethernet, które zamiast otrzymywania pakietów z fizycznego medium
otrzymuje je od programu i zamiast wysyłania pakietów przez fizyczne
medium wysyła je do programu.

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
%{__perl} -pi -e "s|/dev|$RPM_BUILD_ROOT/dev|g;" linux/create_dev
%{__make} -C linux dev

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{smpstr}-net-tun
%depmod %{_kernel_ver}

%postun	-n kernel%{smpstr}-net-tun
%depmod %{_kernel_ver}

%files -n kernel%{smpstr}-net-tun
%defattr(644,root,root,755)
%doc FAQ README ChangeLog
/lib/modules/%{_kernel_ver}/net/tun.o*
%attr(600,root,root) /dev/*

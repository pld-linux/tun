%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		smpstr		%{?_with_smp:smp}%{!?_with_smp:up}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	Universal TUN/TAP device driver
Name:		tun
Version:	1.1
Release:	1@%{_kernel_ver}%{smpstr}
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Source0:	http://vtun.sourceforge.net/tun/%{name}-%{version}.tar.gz
URL:		http://vtun.sourceforge.net/tun/
BuildRequires:	perl
BuildRequires:	kernel-headers < 2.3.0
Prereq:		/sbin/depmod
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TUN/TAP provides packet reception and transmission for user space
programs. It can be viewed as a simple Point-to-Point or Ethernet
device, which instead of receiving packets from a physical media,
receives them from user space program and instead of sending packets
via physical media writes them to the user space program.

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

gzip -9nf FAQ README ChangeLog

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(644,root,root) /lib/modules/%{_kernel_ver}/net/tun.o
%attr(600,root,root) /dev/*

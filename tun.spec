Name:		tun
Version:	1.1
Release:	1
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Url:		http://vtun.sourceforge.net/tun/
Source0:	http://vtun.sourceforge.net/tun/%{name}-%{version}.tar.gz
Summary:	Universal TUN/TAP device driver.
Prereq:		/sbin/depmod
BuildRequires:	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_kernel_ver	%(grep UTS_RELEASE /usr/include/linux/version.h 2>/dev/null | cut -d'"' -f2)

%description
TUN/TAP provides packet reception and transmission for user space
programs. It can be viewed as a simple Point-to-Point or Ethernet
device, which instead of receiving packets from a physical media,
receives them from user space program and instead of sending packets
via physical media writes them to the user space program.

%prep
%setup -q 
./configure

%build
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net
install linux/tun.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net

install -d $RPM_BUILD_ROOT/dev
perl -pi -e "s|/dev|$RPM_BUILD_ROOT/dev|g;" linux/create_dev 
make -C linux dev

gzip -9nf FAQ README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
depmod -a

%postun
depmod -a

%files
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}/net/tun.o
%attr(600,root,root) /dev/*
%doc *.gz

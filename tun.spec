%define		_kernel_ver %(grep UTS_RELEASE /usr/src/linux/include/linux/version.h 2>/dev/null | cut -d'"' -f2)

Summary:	Universal TUN/TAP device driver
Name:		tun
Version:	1.1
Release:	1@%{_kernel_ver}
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Source0:	http://vtun.sourceforge.net/tun/%{name}-%{version}.tar.gz
URL:		http://vtun.sourceforge.net/tun/
BuildRequires:	perl
Prereq:		/sbin/depmod
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
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
%configure
%{__make} 

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

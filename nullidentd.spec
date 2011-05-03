%define	name	nullidentd
%define	version	1.0
%define	release 9

Summary:	Minimal identd server implementing the auth protocol (RFC 1413)
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
License:	GPL
Group:		System/Servers
Source0:	http://www.tildeslash.org/nullidentd/%{name}-%{version}.tar.bz2
Source1:	%{name}.xinetd.bz2
Patch0:		%{name}-makefile.patch.bz2
Patch1:		nullidentd-1.0-gcc4-fixes.patch.bz2
URL:		http://www.tildeslash.org/nullidentd.html
Provides:	identd
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(pre,postun):	rpm-helper

%description
nullidentd is intended to be a bare minimum identd server.

The program implements the auth protocol from RFC 1413.  This protocol is
used to identify active TCP connections.  It depends on the trustworthiness
of the server and as such is completely useless as a method of
identification.  Unfortunately some applications still require that an identd
server is available to query about incoming connections.  nullidentd
implements the absolute minimum server to allow these applications to
function.  It returns a fake response for any request.

%prep
%setup -q
%patch0 -p0
%patch1 -p1 -b .gcc4

%build
%make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/xinetd.d,%{_sbindir}}
%makeinstall
install -m755 %{name} $RPM_BUILD_ROOT%{_sbindir}
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/%{name}
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/true

%post
%_post_service xinetd

%preun
if [ -f /var/run/xinetd.pid ]; then
	echo "Restarting xinetd service"
	service xinetd restart
fi

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%doc README CHANGELOG
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%{_sbindir}/%{name}
%{_localstatedir}/lib/%{name}


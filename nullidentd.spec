%define	name	nullidentd
%define	version	1.0
%define release 10

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



%changelog
* Tue May 03 2011 Michael Scherer <misc@mandriva.org> 1.0-9mdv2011.0
+ Revision: 664792
- rebuild old pacakge

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.0-7mdv2010.0
+ Revision: 430188
- rebuild

* Mon Jun 02 2008 Pixel <pixel@mandriva.com> 1.0-6mdv2009.0
+ Revision: 214231
- adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 1.0-6mdv2008.1
+ Revision: 130757
- kill re-definition of %%buildroot on Pixel's request
- import nullidentd


* Fri Dec 23 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.0-6mdk
- get rid of compile warnings (P1)
- fix no-prereq-on rpm-helper
- fix summary-ended-with-dot
- %%mkrel
- convert changelog to utf-8

* Tue Nov 02 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.0-5mdk
- fix BuildRoot

* Wed Nov 26 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.0-4mdk
- updated url

* Wed Jul 02 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0-3mdk
- fix problem with xinetd being disabled after removal of rpm (fixes #4079)

* Tue Feb 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0-2mdk
- Corrected url

* Thu Nov 21 2002 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0-1mdk
- Initial release
- xinetd conf file from je_
- Fixed makefile

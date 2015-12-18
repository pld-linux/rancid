%include	/usr/lib/rpm/macros.perl
Summary:	Really Awesome New Cisco confIg Differ
Name:		rancid
Version:	3.2
Release:	0.1
License:	BSD with advertising
Group:		Applications/Networking
Source0:	ftp://ftp.shrubbery.net/pub/rancid/%{name}-%{version}.tar.gz
# Source0-md5:	b0bd8a9f98bc1077893425059a03b7ec
Source1:	%{name}.cron
Source2:	%{name}.logrotate
Patch0:		%{name}-conf.patch
Patch1:		%{name}-Makefile.patch
URL:		http://www.shrubbery.net/rancid/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cvs
BuildRequires:	expect >= 5.40
BuildRequires:	iputils
BuildRequires:	openssh-clients
BuildRequires:	perl
BuildRequires:	rpm-perlprov >= 4.1-13
#BuildRequires:	rsh
#BuildRequires:	sendmail
BuildRequires:	subversion
BuildRequires:	telnet
Requires:	expect >= 5.40
Requires:	findutils
Requires:	iputils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# should be provided by this package
%define		_noautoreq_perl rancid

%description
RANCID monitors a router's (or more generally a device's)
configuration, including software and hardware (cards, serial numbers,
etc) and uses CVS (Concurrent Version System) or Subversion to
maintain history of changes.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--sysconfdir=%{_sysconfdir}/%{name} \
	--bindir=%{_libexecdir}/%{name} \
	--libdir=%{perl_vendorlib} \
	--enable-conf-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_localstatedir}/{%{name},log/%{name}/old}
install -d $RPM_BUILD_ROOT{/etc/{cron.d,logrotate.d},%{_bindir}}

%{__sed} -e 's|RANCIDBINDIR|%{_libexecdir}/%{name}|g' %{SOURCE1} > $RPM_BUILD_ROOT/etc/cron.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

# symlink some bins
for base in \
	%{name} %{name}-cvs %{name}-fe %{name}-run
	do
	ln -sf %{_libexecdir}/%{name}/${base} \
	$RPM_BUILD_ROOT%{_bindir}/${base}
done

# duplicate with %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/{CHANGES,COPYING,FAQ,README*,UPGRADING}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
groupadd -r %{name}
useradd -r -g %{name} -d %{_localstatedir}/%{name} -s /bin/sh -k /etc/skel -m -c "RANCID" %{name}

%files
%defattr(644,root,root,755)
%doc CHANGES cloginrc.sample COPYING FAQ README README.lg Todo
%attr(750,rancid,rancid) %dir %{_sysconfdir}/%{name}
%attr(640,rancid,rancid) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/lg.conf
%attr(640,rancid,rancid) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/rancid.conf
%attr(640,rancid,rancid) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/rancid.types.base
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(755,root,root) %{_bindir}/rancid
%attr(755,root,root) %{_bindir}/rancid-cvs
%attr(755,root,root) %{_bindir}/rancid-fe
%attr(755,root,root) %{_bindir}/rancid-run
%{_mandir}/man1/*.1*
%{_mandir}/man3/rancid.3*
%{_mandir}/man5/*.5*

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_datadir}/%{name}
%{perl_vendorlib}/%{name}

%attr(750,rancid,rancid) %dir %{_localstatedir}/log/%{name}
%attr(750,rancid,rancid) %dir %{_localstatedir}/log/%{name}/old
%attr(750,rancid,rancid) %dir %{_localstatedir}/%{name}/

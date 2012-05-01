Name: compat-opensm-libs
Version: 3.3.5
Release: 3%{?dist}
Summary: Back compatability libraries for the IB management stack
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://openfabrics.org/
Source0: http://www.openfabrics.org/downloads/management/opensm-3.3.5.tar.gz
Source1: http://www.openfabrics.org/downloads/management/libibumad-1.3.4.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: libtool, bison, flex, byacc, libibmad
ExcludeArch: s390 s390x

%description
The libibumad and opensm packages provide libraries for use on the system.
As those libraries have changed version, this compat package provides the
older version of the libraries so that packages or user applications will
not need to be recompiled against the newer libraries unnecessarily.

%prep
%setup -q -n opensm-3.3.5 -a 1

%build
#libibumad first, then libibmad, then opensm
cd libibumad-1.3.4
%configure
make %{?_smp_mflags}
cd ..
%configure --with-opensm-conf-sub-dir=rdma CPPFLAGS="-I../libibumad-1.3.4/include/" LDFLAGS="-L../libibumad-1.3.4/" --disable-libcheck
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd libibumad-1.3.4
make DESTDIR=%{buildroot} install
cd ..
make DESTDIR=%{buildroot} install
# remove unpackaged files from the buildroot
rm -rf %{buildroot}/etc %{buildroot}/usr/include %{buildroot}/usr/sbin
rm -rf %{buildroot}/usr/share
rm -f %{buildroot}%{_libdir}/*.{la,so,a}
rm -f %{buildroot}%{_libdir}/libosm*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/lib*

%changelog
* Wed Aug 31 2011 Doug Ledford <dledford@redhat.com> - 3.3.5-3
- Change the file spec so we don't accidentally pick up the debug files in
  the base package on 32bit arches
- Resolves: bz732495

* Mon Aug 01 2011 Doug Ledford <dledford@redhat.com> - 3.3.5-2
- Drop libibmad as it didn't soname bump, and also remove the lower level
  opensm libs, libosm{comp,vendor} as they didn't soname bump either
- Related: bz725016

* Mon Jul 25 2011 Doug Ledford <dledford@redhat.com> - 3.3.5-1
- Initial creation of package
- Related: bz725106


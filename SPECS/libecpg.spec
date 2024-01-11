%global majorversion 13

Summary: ECPG - Embedded SQL in C
Name: libecpg
Version: %majorversion.5
Release: 1%{?dist}

License: PostgreSQL
Url: http://www.postgresql.org/

Source0: https://ftp.postgresql.org/pub/source/v%version/postgresql-%version.tar.bz2
Source1: https://ftp.postgresql.org/pub/source/v%version/postgresql-%version.tar.bz2.sha256


# Comments for these patches are in the patch files.
Patch1: libecpg-10.5-rpm-pgsql.patch
Patch2: libecpg-10.5-var-run-socket.patch
Patch3: libecpg-12.2-external-libpq.patch
Patch4: libecpg-10.5-no-compat-lib.patch
Patch5: libecpg-12.2-dependency-build.patch

BuildRequires: gcc
BuildRequires: glibc-devel bison flex gawk
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: krb5-devel
BuildRequires: openldap-devel
BuildRequires: libpq-devel
BuildRequires: gettext
BuildRequires: multilib-rpm-config
BuildRequires: make

Requires: libpgtypes = %{version}-%{release}

%description
An embedded SQL program consists of code written in an ordinary programming
language, in this case C, mixed with SQL commands in specially marked sections.
To build the program, the source code (*.pgc) is first passed through the
embedded SQL preprocessor, which converts it to an ordinary C program (*.c), and
afterwards it can be processed by a C compiler.


%package devel
Summary: Development files for ECPG - Embedded SQL in C
Requires: %name%{?_isa} = %version-%release
Requires: libpgtypes%{?_isa} = %version-%release

%description devel
ECPG development files.  You will need to install this package to build any
package or any clients that use the ECPG to connect to a PostgreSQL server.


%package -n libpgtypes
Summary: Map PostgreSQL database types to C equivalents

%description -n libpgtypes
The pgtypes library maps PostgreSQL database types to C equivalents that can be
used in C programs. It also offers functions to do basic calculations with those
types within C, i.e., without the help of the PostgreSQL server.


%prep
( cd "$(dirname "%SOURCE1")" ; sha256sum -c "%SOURCE1" )
%autosetup -n postgresql-%version -p1

# remove .gitignore files to ensure none get into the RPMs (bug #642210)
find . -type f -name .gitignore | xargs rm


%build
# We don't build server nor client (e.g. /bin/psql) binaries in this package, so
# we can disable some configure options.
%configure \
    --disable-rpath \
    --with-ldap \
    --with-openssl \
    --with-gssapi \
    --enable-nls \
    --without-readline \
    --datadir=%_datadir/pgsql

%make_build -C "src/interfaces/ecpg" -j1


%install
%make_install -C "src/interfaces/ecpg" -j1

# remove files not to be packaged
find $RPM_BUILD_ROOT -name '*.a' -delete

%multilib_fix_c_header --file "%{_includedir}/ecpg_config.h"

# function from postgresql.spec
find_lang_bins ()
{
    lstfile=$1 ; shift
    cp /dev/null "$lstfile"
    for binary; do
        %find_lang "$binary"-%majorversion
        cat "$binary"-%majorversion.lang >>"$lstfile"
    done
}

find_lang_bins %name.lst        ecpglib6
find_lang_bins %name-devel.lst  ecpg


%files -f %name.lst
%license COPYRIGHT
%_libdir/libecpg.so.6*


%files -n libpgtypes
%license COPYRIGHT
%_libdir/libpgtypes.so.3*


%files devel -f %name-devel.lst
%_bindir/ecpg
%_libdir/libecpg.so
%_libdir/libpgtypes.so
%_libdir/pkgconfig/libecpg.pc
%_libdir/pkgconfig/libpgtypes.pc
%_includedir/ecpg*.h
%_includedir/pgsql/informix
%_includedir/pgtypes*.h
%_includedir/sql3types.h
%_includedir/sqlca.h
%_includedir/sqlda*.h


%changelog
* Mon Nov 15 2021 Marek Kulik <mkulik@redhat.com> - 13.5-1
- Rebase to upstream release 13.5

* Fri Aug 20 2021 Filip Januš <fjanus@redhat.com> - 13.1-11
- Add -j1 also into build section
- Resolves: #1975438

* Thu Aug 05 2021 Filip Januš <fjanus@redhat.com> - 13.1-10
- Disable parallel build
- Resolves: #1975438

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 13.1-9
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jul 28 2021 Filip Januš <fjanus@redhat.com> - 13.1-8
- Fix gating.yaml and rebuild

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 13.1-7
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 13.1-6
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 13.1-5
- rebuild for libpq ABI fix rhbz#1908268

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 03 2020 Honza Horak <hhorak@redhat.com> - 13.1-3
- Add Requires: libpgtypes to avoid the need to test interoperability
  between the various combinations of old and new subpackages

* Wed Nov 18 2020 Honza Horak <hhorak@redhat.com> - 13.1-1
- Rebase to upstream release 13.0

* Fri Oct 23 2020 Honza Horak <hhorak@redhat.com> - 13.0-1
- Rebase to upstream release 13.0

* Tue Aug 25 2020 Patrik Novotný <panovotn@redhat.com> - 12.4-1
- Rebase to upstream release 12.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 18 2020 Patrik Novotný <panovotn@redhat.com> - 12.3-1
- Rebase to upstream release 12.3

* Mon Mar 2 2020 Filip Januš <fjanus@redhat.com> - 12.2-1
- Rebase onto: 12.2
- update of patch(libecpg-10.5-external-libpq.patch) was needed
- add upstream patch libecpg-12.2-dependency-build.patch
  https://www.postgresql.org/message-id/20200321221303.GA17979%40momjian.us 

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Pavel Raiskup <praiskup@redhat.com> - 11.2-1
- latest upstream release, per release notes:
  https://www.postgresql.org/docs/11/static/release-11-1.html
  https://www.postgresql.org/docs/11/static/release-11-2.html

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Pavel Raiskup <praiskup@redhat.com> - 11.0-1
- latest upstream release, per release notes:
  https://www.postgresql.org/docs/11/static/release-11.html

* Thu Aug 30 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-1
- slight simplification before review

* Thu Aug 16 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-0.1
- initial packaging

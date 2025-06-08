#
# Conditional build:
%bcond_with	tests		# test suite

%define		kf_ver		5.94.0
%define		qt_ver		6.5.0
%define		kaname		libkexiv2
Summary:	libkexiv2 - KDE Exiv2 wrapper
Summary(pl.UTF-8):	libexiv2 - obudowanie Exiv2 dla KDE
Name:		ka6-%{kaname}
Version:	25.04.2
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{version}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	2f08c8a352fc7ecd303eb3d8c3d4d45d
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	exiv2-devel >= 0.25
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	exiv2 >= 0.25
# don't obsolete until ka5 exists in PLD
#Obsoletes:	ka5-libkexiv2 < 24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libkexiv2 is a wrapper around Exiv2.

%description -l pl.UTF-8
Libkexiv2 jest wraperem wokół Exiv2.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qt_ver}
Requires:	Qt6Gui-devel >= %{qt_ver}
Requires:	libstdc++-devel >= 6:5
#Obsoletes:	ka5-libkexiv2-devel < 24

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_libdir}/libKExiv2Qt6.so.*.*
%ghost %{_libdir}/libKExiv2Qt6.so.0
%{_datadir}/qlogging-categories6/libkexiv2.categories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKExiv2Qt6.so
%{_includedir}/KExiv2Qt6
%{_libdir}/cmake/KExiv2Qt6

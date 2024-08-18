#
# Conditional build:
%bcond_with	tests		# build with tests

%define		kdeappsver	24.05.2
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		libkexiv2
Summary:	libkexiv2 - KDE Exiv2 wrapper
Summary(pl.UTF-8):	libexiv2 - obudowanie Exiv2 dla KDE
Name:		ka6-%{kaname}
Version:	24.05.2
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	4c870ca10078b89f7f8b6c183f9ab7d2
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	exiv2-devel >= 0.24
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
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
Obsoletes:	ka5-%{kaname}-devel < %{version}

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
%ghost %{_libdir}/libKExiv2Qt6.so.0
%{_libdir}/libKExiv2Qt6.so.*.*
%{_datadir}/qlogging-categories6/libkexiv2.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KExiv2Qt6
%{_libdir}/cmake/KExiv2Qt6
%{_libdir}/libKExiv2Qt6.so

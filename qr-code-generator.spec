%define clib %mklibname qrcodegen 1
%define clibd %mklibname -d qrcodegen
%define clibs %mklibname -s -d qrcodegen
%define cpplib %mklibname qrcodegencpp 1
%define cpplibd %mklibname -d qrcodegencpp

%global richname QR-Code-generator
%global commit0 67c62461d380352500fc39557fd9f046b7fe1d18
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20191014

Name: qr-code-generator
Version: 1.5.0
Release: 1.%{date}git%{shortcommit0}%{?dist}

License: MIT
Summary: High-quality QR Code generator library
URL: https://github.com/nayuki/%{richname}
Source0: %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# https://github.com/nayuki/QR-Code-generator/pull/72
Patch100: %{name}-build-fixes.patch

BuildRequires: python3-devel
BuildRequires: gcc-c++
BuildRequires: gcc

%description
This project aims to be the best, clearest QR Code generator library in
multiple languages.

The primary goals are flexible options and absolute correctness.
Secondary goals are compact implementation size and good documentation
comments.

%package -n %{clib}
Summary: QR Code generator library for C
Group: System/Libraries

%description -n %{clib}
QR Code generator library for C


%package -n %{clibd}
Summary: Development files for the QR Code generator C library
Group: Development/C
Requires: %{clib} = %{EVRD}
Provides: %{name}-devel = %{EVRD}

%description -n %{clibd}
Development files for the QR Code generator C library

%package -n %{cpplib}
Summary: QR Code generator library for C++
Group: System/Libraries

%description -n %{cpplib}
QR Code generator library for C++

%package -n %{cpplibd}
Summary: Development files for the QR Code generator C++ library
Group: Development/C
Requires: %{cpplib} = %{EVRD}
Provides: %{name}-c++-devel = %{EVRD}

%description -n %{cpplibd}
Development files for the QR Code generator C++ library

%package -n python-qrcodegen
Summary: High-quality QR Code generator library (Python version)
BuildArch: noarch
%{?python_provide:%python_provide python3-qrcodegen}

%description -n python-qrcodegen
This project aims to be the best, clearest QR Code generator library in
multiple languages.

The primary goals are flexible options and absolute correctness.
Secondary goals are compact implementation size and good documentation
comments.

%prep
%autosetup -n %{richname}-%{commit0} -p1

%build
# Exporting correct build flags...
%set_build_flags

# Building plain C version...
pushd c
%make_build
popd

# Building C++ version...
pushd cpp
%make_build
popd

# Building Python version...
pushd python
%py3_build
popd

%install
# Installing plain C version...
pushd c
%make_install LIBDIR=%{buildroot}%{_libdir} INCLUDEDIR=%{buildroot}%{_includedir}/qrcodegen
popd

# Installing C++ version...
pushd cpp
%make_install LIBDIR=%{buildroot}%{_libdir} INCLUDEDIR=%{buildroot}%{_includedir}/qrcodegencpp
popd

# Installing Python version...
pushd python
%py3_install
popd

%files -n %{clib}
%{_libdir}/libqrcodegen.so.1*

%files -n %{clibd}
%dir %{_includedir}/qrcodegen
%{_includedir}/qrcodegen/*.h
%{_libdir}/libqrcodegen.so

%files -n %{cpplib}
%{_libdir}/libqrcodegencpp.so.1*

%files -n %{cpplibd}
%dir %{_includedir}/qrcodegen
%{_includedir}/qrcodegencpp/*.hpp
%{_libdir}/libqrcodegencpp.so

%files -n python-qrcodegen
%{py_puresitedir}/qrcodegen.py
%{py_puresitedir}/__pycache__/*
%{py_puresitedir}/*.egg-info

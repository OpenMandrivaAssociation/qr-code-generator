%define clib %mklibname qrcodegen 1
%define clibd %mklibname -d qrcodegen
%define cpplib %mklibname qrcodegencpp 1
%define cpplibd %mklibname -d qrcodegencpp

%global richname QR-Code-generator
#global commit0 13a25580a3e2a29b2b6653802d58d39056f3eaf2
#global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global date 20200302

Name: qr-code-generator
Version: 1.8.0
Release: %{?date:%{date}git%{shortcommit0}.}1

License: MIT
Summary: High-quality QR Code generator library
URL: https://github.com/nayuki/%{richname}
%if 0%{?date}
Source0: %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
%else
Source0: https://github.com/nayuki/QR-Code-generator/archive/v%{version}/%{richname}-%{version}.tar.gz
%endif

# https://github.com/nayuki/QR-Code-generator/pull/72
Patch100: %{name}-build-fixes.patch

BuildRequires: jdk-current
BuildRequires: pkgconfig(python3) >= 3.11
BuildRequires: python%{pyver}dist(setuptools) >= 3.11

# FIXME package Javascript, Typescript and Rust modules once we have
# a proper unified packaging system for those languages

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

%package -n java-io.nayuki.qrcodegen
Summary: QR Code generator library for Java
Group: Development/Java

%description -n java-io.nayuki.qrcodegen
QR Code generator library for Java

%package -n javadoc-io.nayuki.qrcodegen
Summary: API documentation for the QR Code generator library for Java
Group: Development/Java

%description -n javadoc-io.nayuki.qrcodegen
API documentation for the QR Code generator library for Java

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
%autosetup -n %{richname}-%{!?date:%{version}}%{?date:%{commit0}} -p1

%build
# Exporting correct build flags...
%set_build_flags

# Building plain C version...
%make_build -C c CC=%{__cc} CFLAGS="%{optflags}"

# Building C++ version...
%make_build -C cpp CXX=%{__cxx} CXXFLAGS="%{optflags}"

# Building Java version...
cd java/src/main/java
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH
export LANG=en_US.utf-8
export LC_ALL=en_US.utf-8
cat >module-info.java <<EOF
module io.nayuki.qrcodegen {
	exports io.nayuki.qrcodegen;
	requires java.desktop;
}
EOF
find . -name "*.java" |xargs javac --add-modules java.desktop
find . -name "*.class" -o -name "*.properties" |xargs jar cf io.nayuki.qrcodegen-%{version}.jar
javadoc -d docs -sourcepath . --add-modules java.desktop io.nayuki.qrcodegen
cd -

# Building Python version...
pushd python
%py3_build
popd

%install
# Installing plain C version...
%make_install -C c LIBDIR=%{buildroot}%{_libdir} INCLUDEDIR=%{buildroot}%{_includedir}/qrcodegen

# Installing C++ version...
%make_install -C cpp LIBDIR=%{buildroot}%{_libdir} INCLUDEDIR=%{buildroot}%{_includedir}/qrcodegencpp

# The API has remained largely the same, but the header file name
# has changed since 1.5.0 -- so let's symlink it for compatibility
ln -s qrcodegen.hpp %{buildroot}%{_includedir}/qrcodegencpp/QrCode.hpp

# Installing Java version...
cd java
mkdir -p %{buildroot}%{_datadir}/java/modules %{buildroot}%{_datadir}/javadoc
mv src/main/java/*.jar %{buildroot}%{_datadir}/java/modules/
ln -s modules/io.nayuki.qrcodegen-%{version}.jar %{buildroot}%{_datadir}/java/
ln -s modules/io.nayuki.qrcodegen-%{version}.jar %{buildroot}%{_datadir}/java/io.nayuki.qrcodegen.jar
mv src/main/java/docs %{buildroot}%{_datadir}/javadoc/io.nayuki.qrcodegen
cd ..

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
%dir %{_includedir}/qrcodegencpp
%{_includedir}/qrcodegencpp/*.hpp
%{_libdir}/libqrcodegencpp.so

%files -n java-io.nayuki.qrcodegen
%{_datadir}/java/*.jar
%{_datadir}/java/modules/*

%files -n javadoc-io.nayuki.qrcodegen
%{_datadir}/javadoc/io.nayuki.qrcodegen

%files -n python-qrcodegen
%{py_puresitedir}/qrcodegen.py
%{py_puresitedir}/*.egg-info

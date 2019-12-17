%define clib %mklibname qrcodegen 1
%define clibd %mklibname -d qrcodegen
%define clibs %mklibname -s -d qrcodegen
%define cpplib %mklibname qrcodegencpp 1
%define cpplibd %mklibname -d qrcodegencpp
%define cpplibs %mklibname -s -d qrcodegencpp

Name: libqrcodegen
Version: 1.5.0
Release: 1
Source0: https://github.com/nayuki/QR-Code-generator/archive/v1.5.0/%{name}-%{version}.tar.gz
Patch0: https://sources.debian.org/data/main/q/qr-code-generator/1.4.0-1/debian/patches/batch-test.patch
Patch1: https://sources.debian.org/data/main/q/qr-code-generator/1.4.0-1/debian/patches/c-lib.patch
Patch2: https://sources.debian.org/data/main/q/qr-code-generator/1.4.0-1/debian/patches/cpp-lib.patch
Summary: QR Code generator library for multiple programming languages
URL: https://github.com/nayuki/QR-Code-generator
License: MIT
Group: System/Libraries
BuildRequires: jdk-current
BuildRequires: pkgconfig(python3)
# FIXME package Javascript, Typescript and Rust modules once we have
# a proper unified packaging system for those languages

%description
QR Code generator library for multiple programming languages

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

%package -n %{clibs}
Summary: Static library files for the QR Code generator C library
Group: Development/C
Requires: %{clibd} = %{EVRD}

%description -n %{clibs}
Static library files for the QR Code generator C library

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

%package -n %{cpplibs}
Summary: Static library files for the QR Code generator C++ library
Group: Development/C
Requires: %{cpplibd} = %{EVRD}

%description -n %{cpplibs}
Static library files for the QR Code generator C++ library

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
Summary: QR Code generator library for Python
Group: Development/Python

%description -n python-qrcodegen
QR Code generator library for Python

%prep
%autosetup -p1 -n QR-Code-generator-%{version}

%build
# We disable LTO because we're building static libraries
%make_build -C c CC=%{__cc} CFLAGS="%{optflags} -fno-lto"
%make_build -C cpp CXX=%{__cxx} CXXFLAGS="%{optflags} -fno-lto"

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

cd python
python setup.py build

%install
%make_install -C c LIBDIR=%{buildroot}%{_libdir} QRCODEGEN_VERSION=%{version}
%make_install -C cpp LIBDIR=%{buildroot}%{_libdir} QRCODEGEN_VERSION=%{version}
cd java
mkdir -p %{buildroot}%{_datadir}/java/modules %{buildroot}%{_datadir}/javadoc
mv src/main/java/*.jar %{buildroot}%{_datadir}/java/modules/
ln -s modules/io.nayuki.qrcodegen-%{version}.jar %{buildroot}%{_datadir}/java/
ln -s modules/io.nayuki.qrcodegen-%{version}.jar %{buildroot}%{_datadir}/java/io.nayuki.qrcodegen.jar
mv src/main/java/docs %{buildroot}%{_datadir}/javadoc/io.nayuki.qrcodegen
cd ..
cd python
python setup.py install --root=%{buildroot}

%files -n %{clib}
%{_libdir}/libqrcodegen.so.1*

%files -n %{clibd}
%dir %{_includedir}/qrcodegen
%{_includedir}/qrcodegen/*.h
%{_libdir}/libqrcodegen.so

%files -n %{clibs}
%{_libdir}/libqrcodegen.a

%files -n %{cpplib}
%{_libdir}/libqrcodegencpp.so.1*

%files -n %{cpplibd}
%dir %{_includedir}/qrcodegen
%{_includedir}/qrcodegen/*.hpp
%{_libdir}/libqrcodegencpp.so

%files -n %{cpplibs}
%{_libdir}/libqrcodegencpp.a

%files -n java-io.nayuki.qrcodegen
%{_datadir}/java/*.jar
%{_datadir}/java/modules/*

%files -n javadoc-io.nayuki.qrcodegen
%{_datadir}/javadoc/io.nayuki.qrcodegen

%files -n python-qrcodegen
%{py_puresitedir}/qrcodegen.py
%{py_puresitedir}/__pycache__/*
%{py_puresitedir}/*.egg-info

#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	C++ library for value-oriented design using the unidirectional data-flow architecture
Summary(pl.UTF-8):	Biblioteka C++ do projektowania zorientowanego na wartości przy użyciu architektury jednokierunkowego przepływu danych
Name:		lager
Version:	0.1.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/arximboldi/lager/tags
Source0:	https://github.com/arximboldi/lager/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c3ce2ef0230b26a272c0910b5e21f0ad
%define	theme_gitref	b5adfa2a6def8aa55d95dedc4e1bfde214a5e36c
Source1:	https://github.com/arximboldi/sinusoidal-sphinx-theme/archive/%{theme_gitref}/sinusoidal-sphinx-theme-%{theme_gitref}.tar.gz
# Source1-md5:	8873555af1d9f75d42a440fb1c60bd07
URL:		https://sinusoid.es/lager/
# disabled BRs for tests or examples
#BuildRequires:	boost-devel >= 1.56
BuildRequires:	cmake >= 3.8
#BuildRequires:	immer-devel
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_apidocs:BuildRequires:	sphinx-pdg-3 >= 1.3}
#BuildRequires:	zug-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# header-only library, but cmake files location is arch-dependent
%define		_enable_debug_packages	0

%description
Lager is a C++ library to assist value-oriented design by implementing
the unidirectional data-flow architecture. It is heavily inspired by
Elm and Redux, and enables composable designs by promoting the use of
simple value types and testable application logic via pure functions.

%description -l pl.UTF-8
Lager to biblioteka C++ pomagająca w projektowaniu zorientowanym na
wartości poprzez zaimplementowanie architektury jednokierunkowego
przepływu danych. Jest w dużym stopniu inspirowana bibliotekami Elm i
Redux. Pozwala na łączenie projektów poprzez promowanie używania
prostych typów wartości oraz testowalną logikę aplikacji poprzez
czyste funkcje.

%package devel
Summary:	C++ library for value-oriented design using the unidirectional data-flow architecture
Summary(pl.UTF-8):	Biblioteka C++ do projektowania zorientowanego na wartości przy użyciu architektury jednokierunkowego przepływu danych
Group:		Development/Libraries
Requires:	libstdc++-devel >= 6:8

%description devel
Lager is a C++ library to assist value-oriented design by implementing
the unidirectional data-flow architecture. It is heavily inspired by
Elm and Redux, and enables composable designs by promoting the use of
simple value types and testable application logic via pure functions.

%description devel -l pl.UTF-8
Lager to biblioteka C++ pomagająca w projektowaniu zorientowanym na
wartości poprzez zaimplementowanie architektury jednokierunkowego
przepływu danych. Jest w dużym stopniu inspirowana bibliotekami Elm i
Redux. Pozwala na łączenie projektów poprzez promowanie używania
prostych typów wartości oraz testowalną logikę aplikacji poprzez
czyste funkcje.

%package apidocs
Summary:	API documentation for Lager library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Lager
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Lager library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Lager.

%prep
%setup -q

tar xf %{SOURCE1} -C tools/sinusoidal-sphinx-theme --strip-components=1

%build
install -d build
cd build
%cmake .. \
	-Dlager_BUILD_EXAMPLES=OFF \
	-Dlager_BUILD_TESTS=OFF

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{_includedir}/lager
%{_libdir}/cmake/Lager

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,*.html,*.js}
%endif

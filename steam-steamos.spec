# Create an option to build locally without fetchting own repo
# for sourcing and patching
%bcond local 0

# Source repo
%global author pvermeer
%global source steam-steamos
%global sourcerepo https://github.com/PVermeer/steam-steamos
%global tag v0.0.3

Name: steam-steamos
Version: 0.0.3
Release: 0%{?dist}
License: GPL-3.0 license
Summary: Launch steam as it would on steamOS on desktop or as nested gamescope-session.
Url: %{sourcerepo}

BuildRequires: git

Requires: steam
Requires: gamescope
Requires: mangohud
Requires: (gamescope-session-steam or gamescope-session-ogui-steam or gamescope-session-opengamepadui or gamescope-session)
Requires: /usr/bin/gdctl

%description
A launcher and desktop files to launch steam in steamOS mode.
Gnome only and requires a proper gamescope-session installed (Terra).

%define workdir %{_builddir}/%{name}
%define sourcedir %{workdir}/%{source}

%prep
# To apply working changes handle sources / patches locally
# COPR should clone the commited changes
%if %{with local}
  # Get sources - local build
  mkdir -p %{sourcedir}
  cp -r %{_topdir}/SOURCES/* %{sourcedir}
%else
  # Get sources - COPR build
  git clone %{sourcerepo} %{sourcedir}
  cd %{sourcedir}
  git reset --hard %{tag}
  cd %{workdir}
%endif

# Do src stuff
cd %{sourcedir}
rm -rf .git
cd %{workdir}

%define license_dir %{_licensedir}/%{name}

%install
mkdir -p %{buildroot}/%{license_dir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/applications/

install -m 0644 %{sourcedir}/LICENSE %{buildroot}/%{license_dir}/LICENSE

install -D -m 0755 %{sourcedir}/src/steam-steamos %{buildroot}/%{_bindir}
install -D -m 0644 %{sourcedir}/assets/steam-steamos.desktop %{buildroot}/%{_datadir}/applications
install -D -m 0644 %{sourcedir}/assets/steam-steamos-gamescope.desktop %{buildroot}/%{_datadir}/applications

%files
%license %{license_dir}/LICENSE
%{_bindir}/steam-steamos
%{_datadir}/applications/steam-steamos.desktop
%{_datadir}/applications/steam-steamos-gamescope.desktop

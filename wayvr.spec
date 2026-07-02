%global commit 6563bbd
%global shortcommit 6563bbd
%global __requires_exclude ^libopenvr_api\\.so

Name:           wayvr-git
Version:        26.2.1
Release:        0.36.%{shortcommit}%{?dist}
Summary:        Your way to enjoy VR on Linux! Access your Wayland/X11 desktop from SteamVR/Monado/WiVRn

License:        GPLv3+
URL:            https://github.com/wayvr-org/wayvr
Source0:        https://github.com/wayvr-org/wayvr/%{commit}/%{name}-%{commit}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  git
BuildRequires:  python3
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  libshaderc-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  dbus-devel
BuildRequires:  pipewire-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  libdav1d-devel
BuildRequires:  openxr-devel
BuildRequires:  openvr-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig

Requires:       fontconfig%{?_isa}
Requires:       freetype%{?_isa}
Requires:       alsa-lib%{?_isa}
Requires:       dbus-libs%{?_isa}
Requires:       pipewire-libs%{?_isa}
Requires:       libxkbcommon%{?_isa}
Requires:       libxkbcommon-x11%{?_isa}
Requires:       openxr%{?_isa}
Requires:       openvr-api
Requires:       libshaderc%{?_isa}

Provides:       wayvr = %{version}-%{release}
Conflicts:      wayvr

%description
WayVR is a VR overlay that lets you access your Wayland and X11 desktop
from SteamVR or Monado. It supports both OpenVR and OpenXR.

%prep
%autosetup -n wayvr-main

pushd wayvr
cargo fetch --locked --target $(rustc -vV | sed -n 's/host: //p')
popd

pushd wayvrctl
cargo fetch --locked --target $(rustc -vV | sed -n 's/host: //p')
popd

%build
export CARGO_PROFILE_RELEASE_DEBUG=2
export CMAKE_POLICY_VERSION_MINIMUM=3.5
export SHADERC_LIB_DIR=%{_libdir}

pushd wayvr
cargo build --frozen --release --all-features
popd

pushd wayvrctl
cargo build --frozen --release --all-features
popd

%install
install -Dm0755 target/release/wayvr           %{buildroot}%{_bindir}/wayvr
install -Dm0755 target/release/wayvrctl        %{buildroot}%{_bindir}/wayvrctl
install -Dm0644 wayvr/wayvr.desktop            %{buildroot}%{_datadir}/applications/wayvr.desktop
install -Dm0644 wayvr/wayvr.png                %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/wayvr.png
install -Dm0644 wayvr/wayvr.svg                %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wayvr.svg

%post
if [ ! -L %{_libdir}/libopenvr_api.so ] && [ -f %{_libdir}/libopenvr_api.so.2.0.0 ]; then
    ln -s libopenvr_api.so.2.0.0 %{_libdir}/libopenvr_api.so
fi

%preun
if [ $1 -eq 0 ]; then
    if [ "$(readlink %{_libdir}/libopenvr_api.so)" = "libopenvr_api.so.2.0.0" ]; then
        rm -f %{_libdir}/libopenvr_api.so
    fi
fi

%files
%license LICENSE
%{_bindir}/wayvr
%{_bindir}/wayvrctl
%{_datadir}/applications/wayvr.desktop
%{_datadir}/icons/hicolor/128x128/apps/wayvr.png
%{_datadir}/icons/hicolor/scalable/apps/wayvr.svg

%changelog
* Thu Jul 02 2026 Galister <galister@example.com> - 26.2.1-0.36.
- Initial package based on the aur pkgbuild using wayvr git commit 6563bbd

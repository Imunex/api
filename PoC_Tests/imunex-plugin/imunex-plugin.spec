Name:           imunex-plugin
Version:        1.0
Release:        1%{?dist}
Summary:        Imunex AI tshark custom module

Group:          Network
License:        Proprietary
URL:            https://imunex.ai
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc, make, libpcap-devel, glibc-devel
Requires:       glib2, libpcap, lua, libsmi, pcre, pcre2, glibc

%description
Tshark network protocol analyzer with included Imunex AI Plugin with prebuild static libraries for CentOS 7/8.

%prep
%setup -q -n imunex-plugin

%build

%install
#mkdir -p %{buildroot}/usr/local/lib
mkdir -p %{buildroot}/usr/local/imunex/bin
mkdir -p %{buildroot}/usr/local/lib
mkdir -p %{buildroot}/usr/local/lib64
#cp /usr/local/bin/tshark %{buildroot}/usr/local/imunex/bin
#cp /usr/local/bin/dumpcap %{buildroot}/usr/local/imunex/bin
install -D -m755 /usr/local/bin/tshark %{buildroot}/usr/local/imunex/bin/tshark
install -D -m755 /usr/local/bin/dumpcap %{buildroot}/usr/local/imunex/bin/dumpcap
cp /usr/local/lib64/libwiretap.so.14.1.5 %{buildroot}/usr/local/lib64
cp /usr/local/lib64/libwireshark.so.17.0.5 %{buildroot}/usr/local/lib64
cp /usr/local/lib64/libwsutil.so.15.0.0 %{buildroot}/usr/local/lib64
cp /usr/local/lib/libcares.so.2.2.0 %{buildroot}/usr/local/lib
cp /usr/local/lib/libgcrypt.so.20.2.0 %{buildroot}/usr/local/lib
cp /usr/local/lib/libgpg-error.so.0.22.0 %{buildroot}/usr/local/lib


# Create necessary directories
mkdir -p %{buildroot}/etc/ld.so.conf.d

echo "/usr/local/lib" > %{buildroot}/etc/ld.so.conf.d/imunex-lib.conf
echo "/usr/local/lib64" >> %{buildroot}/etc/ld.so.conf.d/imunex-lib.conf

%post
echo "Please run \"ldconfig\" to update the cache libraries"
echo "Imunex AI Plugin installed successfully"

%postun
echo "Imunex AI Plugin uninstalled"

%files
/usr/local/imunex/bin/tshark
/usr/local/imunex/bin/dumpcap
/usr/local/lib64/*
/usr/local/lib/*
/etc/ld.so.conf.d/imunex-lib.conf


%changelog
* Mon May 27 2024 Tiago Flores <tiago@imunex.ai> - 1.0-1
- RPM release of Imunex AI tshark custom Plugin

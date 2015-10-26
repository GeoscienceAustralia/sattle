%define name sattle 
%define version 1.0.0
%define release 1
%define prefix /opt/django
  
%define debug_package %{nil}
 
 
Summary: TLE data Django Restful system 
Name: %{name}
Version: %{version}
Release: %{release}
License: Geoscience Australia 
Prefix:  %{prefix}
Group: Applications/Engineering
Source: sattle.tar.gz 
BuildRoot: %{_topdir}/BUILD/%{name}-%{version}-buildroot
AutoReq: 0
BuildArch: noarch
Vendor: Fei Zhang <fei.zhang@ga.gov.au>
#Requires:  python27 fetch neocommon tleserv

%description
Install Django project into /opt/django
 
%prep
%setup -q -c %{name}
 

%build
 
%install
echo $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{prefix}
mv ./* $RPM_BUILD_ROOT/%{prefix}
 
%clean
rm -rf $RPM_BUILD_ROOT
 
%files 
%attr(-,rms_usr,rms_grp) %{prefix}/
 
%pre
#bash commands
#/etc/init.d/fetchtled stop

%post
#mkdir -p /data/fetch/lock
#chown -R rms_usr:rms_grp /data/fetch
#mkdir -p /data/ephemeris/source
#chown -R rms_usr:rms_grp  /data/ephemeris

/etc/init.d/fetchtled start

%postun
rm -rf %{prefix}/*

 
%changelog

#* 2015-07-27: Fei Zhang initiated this spec file 

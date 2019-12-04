%include SPECS/.upsilon-pycommon.rpmmacro

Name:		upsilon-pycommon
Version:	%{version_formatted_short}
Release:	%{timestamp}.%{?dist}
Summary:	Monitoring Software
BuildArch:	noarch

Group:		Applications/System
License:	GPLv2
URL:		http://upsilon-project.co.uk
Source0:	upsilon-pycommon.zip

BuildRequires:	python

%if 0%{?fedora} >= 28
Requires:	python2 python2-pyyaml python2-mysql python2-prettytable python2-pika
%else
Requires:	python2 python2-pyyaml python-mysql python2-prettytable python2-pika
%endif

%description
Monitoring software

%prep
rm -rf $RPM_BUILD_DIR/*
%setup -q -n upsilon-pycommon-%{tag}


%build
mkdir -p %{buildroot}/usr/lib/python2.7/site-packages/upsilon
cp src/* %{buildroot}/usr/lib/python2.7/site-packages/upsilon

%files
/usr/lib/python2.7/site-packages/upsilon/*

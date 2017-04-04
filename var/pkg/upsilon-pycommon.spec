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
Requires:	python PyYAML MySQL-python python-prettytable

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

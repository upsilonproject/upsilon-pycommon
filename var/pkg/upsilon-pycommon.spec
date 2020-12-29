%include SPECS/.upsilon-pycommon.rpmmacro

Name:		upsilon-pycommon
Version:	%{version_formatted_short}
Release:	%{timestamp}%{?dist}
Summary:	Monitoring Software
BuildArch:	noarch

Group:		Applications/System
License:	GPLv2
URL:		http://upsilon-project.co.uk
Source0:	upsilon-pycommon.zip

BuildRequires:	python

%if 0%{?el7}
Requires:	python3 python3-pyyaml MySQL-python python-prettytable python3-pika
%endif

%if 0%{?fedora} >= 28
Requires:	python3 python3-pyyaml python3-mysql python3-prettytable python3-pika python3-google-api-client
%endif

%description
Monitoring software

%prep
rm -rf $RPM_BUILD_DIR/*
%setup -q -n upsilon-pycommon-%{tag}


%build
mkdir -p %{buildroot}/%{python_sitelib}/upsilon
cp src/*.py %{buildroot}/%{python_sitelib}/upsilon

%files
%{python_sitelib}/upsilon/*

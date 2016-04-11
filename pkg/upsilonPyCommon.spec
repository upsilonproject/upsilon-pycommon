Name:		upsilonPyCommon
Version: 	%{buildid_version}
Release:	%{buildid_timestamp}%{dist}
Summary:	A set of common upsilon libs.

Group:		Applications/System
License:	GPLv3
URL:		http://upsilon-project.co.uk
Source0:	upsilon-pycommmon-%{buildid_tag}.zip

BuildRequires:	python
Requires:	python python-pika

%description
A set of common upsilon libs.

%prep
%setup -q -n upsilon-web-%{buildid_tag}


%build
mkdir -p %{buildroot}/usr/lib/python2.7/site-packages/upsilonCommon
cp -r src/*.py %{buildroot}/usr/lib/python2.7/site-packages/upsilonCommon

%files
/usr/lib/python2.7/site-packages/upsilonCommon/*

%changelog
* Mon Apr 11 2016 James Read <contact@jwread.com> 1.0.0
	First version.


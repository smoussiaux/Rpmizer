%define __prelink_undo_cmd %{nil}
%define name %{portal}
%define installdir %{home}/%{user}/%{name}
%define python /usr/bin/python2.6
%define portbase 13080

Name: %{name}
Version: %{version}
Release: 1
Summary: %{name} website
URL: http://cirb.irisnet.be
License: GPL
Vendor: CIRB-CIBG
Packager: bsuttor <bsuttor@cirb.irisnet.be>
Group: Applications/Database
Buildroot: %{_tmppath}/%{name}-buildroot
Source: %{name}-%{version}.tar.gz
BuildRequires:  subversion, git, zlib-devel, freetype-devel, libjpeg-devel, gcc
BuildRequires:  python >= 2.6.6, libxslt-devel
AutoReqProv: no

%description
%{summary}

%package    core
Summary:    %{summary} - core without any clients
Group: Applications/Database
Requires:   python >= 2.6.6
Requires:   openssl-devel
Requires:   python-devel
Requires:   zlib freetype
AutoReqProv: no
%description core
%{summary}

%package    zeoserver
Summary:    %{summary} - core
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description zeoserver
%{summary}

%package    client1
Summary:    %{summary} - client1
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client1
%{summary}

%package    client2
Summary:    %{summary} - client2
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client2
%{summary}

%prep
%setup

%build
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{installdir}
mkdir -p $RPM_BUILD_ROOT%{installdir}/downloads
%{python} bootstrap.py -c rpm.cfg
bin/buildout -N -c rpm.cfg buildout:directory=$RPM_BUILD_ROOT%{installdir} buildout:rpm-directory=%{installdir}

%install
for file in `ls $RPM_BUILD_ROOT%{installdir}/bin/`
do
    sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/bin/$file
    sed -i s/${RPM_BUILD_DIR//\//\\/}\\/%{name}-%{version}\\/eggs/\\%{home}\\/%{user}\\/%{name}\\/eggs/g $RPM_BUILD_ROOT%{installdir}/bin/$file
done
cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/zc.buildout* $RPM_BUILD_ROOT%{installdir}/eggs
cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/setuptools* $RPM_BUILD_ROOT%{installdir}/eggs
cd $RPM_BUILD_ROOT%{installdir}/
rm  $RPM_BUILD_ROOT%{installdir}/.installed.cfg
rm -fr $RPM_BUILD_ROOT%{installdir}/downloads
rm -fr $RPM_BUILD_ROOT%{installdir}/parts/docs
rm -fr $RPM_BUILD_ROOT%{installdir}/.git
rm $RPM_BUILD_ROOT%{installdir}/bin/instance
rm $RPM_BUILD_ROOT%{installdir}/bin/copy_ckeditor_code
rm -rf $RPM_BUILD_ROOT%{installdir}/parts/instance
rm -rf $RPM_BUILD_ROOT%{installdir}/parts/lxml
find $RPM_BUILD_ROOT%{installdir} -name "*.pyc" -delete;
find $RPM_BUILD_ROOT%{installdir} -name "*.pyo" -delete;
for file in `ls $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/bin/`
do
    sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/bin/$file
done
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/etc/zeo.conf
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client1/etc/zope.conf
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client2/etc/zope.conf


%files core
%defattr(-, %{user}, %{user}, 0755)
%{installdir}/develop-eggs
%{installdir}/eggs
%{installdir}/var/log
%dir %{installdir}/bin
%dir %{installdir}/parts
%dir %{installdir}/var

%pre core
exit 0


%post core
/sbin/ldconfig

%preun core
find %{installdir} -name "*.pyc" -delete;
find %{installdir} -name "*.pyo" -delete;
find %{installdir} -name "*.mo" -delete;

%postun core
/sbin/ldconfig

%files zeoserver
%defattr(-, %{user}, %{user} , 0755)
%config(noreplace) %{installdir}/parts/zeoserver/etc/zeo.conf
#%{installdir}/bin/zodbpack
%{installdir}/bin/backup
%{installdir}/bin/repozo
%{installdir}/bin/restore
%{installdir}/bin/snapshotbackup
%{installdir}/bin/snapshotrestore
%{installdir}/bin/zeopack
%{installdir}/bin/zeoserver
%{installdir}/parts/zeoserver
%{installdir}/var/zeoserver
%{installdir}/var/filestorage
%{installdir}/var/blobstorage

%files client1
%defattr(-, %{user}, %{user}, 0755)
%config(noreplace) %{installdir}/parts/client1/etc/zope.conf
%{installdir}/bin/client1
%{installdir}/parts/client1
%{installdir}/var/client1

%files client2
%defattr(-, %{user}, %{user}, 0755)
%config(noreplace) %{installdir}/parts/client2/etc/zope.conf
%{installdir}/bin/client2
%{installdir}/parts/client2
%{installdir}/var/client2


%clean
rm -rf $RPM_BUILD_ROOT%{installdir} $RPM_BUILD_ROOT/etc

%changelog
* Wed Jul 25 2012 -  Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1.1
- Add client2 construction
- Clean path into zope.conf file and zeo.conf file
* Tue Jul 10 2012 - Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1
- initial build

# version_acronym is either sl or slf
# lower case please!
%define version_acronym el

%define base_release_version 6
%define minor_release_version 10

# increment this to get the stuff after the - higher
#  helps for making the rolling one go obsolete
%define release_count 1 

# set ROLLING true for the rolling tree
#  once set it will do the rest for you automatically
#  the only valid values are true and anything else
%define ROLLING false

# #

%define product_family EuroLinux

# setup pretty name
%if %(echo %{version_acronym} | grep -c 'slf')
    %define release_name Prague
    %define variant_titlecase Prague
    %define variant_lowercase prague
    %define beta_directory el10
%else
    %define release_name Prague
    %define beta_directory 6
%endif

%define debug_package %{nil}
%define full_release_version %{base_release_version}.%{minor_release_version}

# if we are building for the rolling tree, define beta
%if %(echo %{ROLLING} |grep -c 'true')
    %define beta rolling
%endif

#########################################################

# so we don't discover that the scripts hiding in doc require bash
%global _use_internal_dependency_generator 0
%global __requires_exclude_from ^%{_libexecdir}/firstboot.sh
%global __requires_exclude ^/bin/sh$
%global __find_requires /bin/true

# this doesn't work.....
# %%global __requires_exclude ^%{_libexecdir}.*

Name:           %{version_acronym}-release
Version:        %{full_release_version}
Release:        %{release_count}%{dist}
Summary:        %{product_family}%{?variant_titlecase: %{variant_titlecase}} release file
Group:          System Environment/Base
License:        GPLv2
Obsoletes:      rawhide-release redhat-release-as redhat-release-es redhat-release-ws redhat-release-de comps rpmdb-redhat fedora-release
Provides:       redhat-release system-release sl-release
Source0:        %{version_acronym}-release%{?variant_lowercase:-%{variant_lowercase}}-%{base_release_version}.tar.gz
BuildRequires:	coreutils bash sed
AutoReq: 0
AutoProv: 1

%description
%{product_family}%{?variant_titlecase: %{variant_titlecase}} release files

%prep
%setup -q -n %{version_acronym}-release%{?variant_lowercase:-%{variant_lowercase}}-%{base_release_version}

%build

# if this is for a 'beta' version of SL
%if 0%{?beta:1}
    echo "Customizing for beta version of %{product_family}%{?variant_titlecase: %{variant_titlecase}} for %{beta_directory}"
    #sed -e "s/\$releasever/%{beta_directory}/g" %{version_acronym}.repo > %{version_acronym}.repo.tmp
    #mv -f %{version_acronym}.repo.tmp %{version_acronym}.repo
%endif
echo OK

%install
rm -rf $RPM_BUILD_ROOT

# create /etc
mkdir -p $RPM_BUILD_ROOT/etc

# create /etc/system-release and /etc/redhat/release
echo "%{product_family}%{?variant_titlecase: %{variant_titlecase}} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > $RPM_BUILD_ROOT/etc/redhat-release
ln -s redhat-release $RPM_BUILD_ROOT/etc/system-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:redhat:enterprise_linux:%{version}:%{?beta:beta}%{!?beta:GA}%{?variant_lowercase::%{variant_lowercase}}" | tr [A-Z] [a-z] > $RPM_BUILD_ROOT/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
cp $RPM_BUILD_ROOT/etc/redhat-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m" >> $RPM_BUILD_ROOT/etc/issue
cp $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue

# copy yum repos to /etc/yum.repos.d
#mkdir -p $RPM_BUILD_ROOT/etc/yum.repos.d
#for file in *.repo; do
#    install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
#done

# Combine GPG keys
cat RPM-GPG-KEY-redhat-release-2 RPM-GPG-KEY-redhat-auxiliary > RPM-GPG-KEY-redhat-release
rm RPM-GPG-KEY-redhat-release-2 RPM-GPG-KEY-redhat-auxiliary
cat RPM-GPG-KEY-redhat-beta-2 RPM-GPG-KEY-redhat-legacy-beta > RPM-GPG-KEY-redhat-beta
rm RPM-GPG-KEY-redhat-beta-2 RPM-GPG-KEY-redhat-legacy-beta

# copy GPG keys
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file $RPM_BUILD_ROOT/etc/pki/rpm-gpg
done
#TODO NEW
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/
(cd $RPM_BUILD_ROOT/usr/share/doc/ ; ln -s %{name}-%{version} redhat-release)

# set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%rhel %{base_release_version}
%%dist .el%{base_release_version}
%%el%{base_release_version} 1
EOF

##### Fix for auto-requires
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
touch %{buildroot}/%{_libexecdir}/%{name}/fixfirstboot.sh
chmod 700 %{buildroot}/%{_libexecdir}/%{name}/fixfirstboot.sh

cat >>%{buildroot}/%{_libexecdir}/%{name}/fixfirstboot.sh << EOS
#!/bin/bash
########################################################################
SELFCOPIES=\${1:-0}
TRIGGERCOPIES=\${2:-0}
########################################################################
if [ -f /usr/share/firstboot/modules/additional_cds.py ] ; then
  rm -f /usr/share/firstboot/modules/additional_cds.py*
fi

if [ -f /usr/share/firstboot/modules/eula.py ] ; then
  rm -f /usr/share/firstboot/modules/eula.py*
fi

if [ -f /usr/share/firstboot/modules/rhn_register.py ] ; then
  rm -f /usr/share/firstboot/modules/rhn_register.py*
fi

EOS


%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -p %{_libexecdir}/%{name}/fixfirstboot.sh -- firstboot
%triggerin -p %{_libexecdir}/%{name}/fixfirstboot.sh -- rhn-setup-gnome


%files
%defattr(-,root,root)
%doc EULA GPL autorun-template
%doc /usr/share/doc/redhat-release
%attr(0644,root,root) /etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,root) /etc/issue
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,root) /etc/issue.net
#%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,root) /etc/yum.repos.d/*
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*
/etc/rpm/macros.dist
%{_libexecdir}/%{name}/

%changelog
* Mon Jul 23 2018 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 6.10-1
- New release

* Mon Apr 23 2018 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 6.9-2
- Add sl-release to provided packages for customer convenience
- Name contains now dist macro 

* Fri Apr 21 2017 Aleksander Baranowski <aleksander.baranowski@euro-linux.com>  6.9-1
- Change for EuroLinux 6.9

* Sun Aug 07 2016 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 6.8-1
- Modified for EuroLinux 6.8

* Wed Sep 16 2015 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 6.7-1
-Change to 6.7
- Backporting SL changes to our package
--> Dumping trigger code into external shell scripts so /bin/bash isn't a dep
--> switched yum repos to %config(noreplace) per request

* Fri Aug 21 2015 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> - 6.4-3
- SL and cern keys removed
- EULA fixed

* Thu Apr 17 2014 Tomasz Klosinski <t.m.klosinski@gmail.com> - 6.4-2
- Modified for EuroLinux

* Fri Mar 15 2013 Pat Riehecky <riehecky@fnal.gov> - 6.4-1
- updated for 6.4 RC1
* Fri Jun 29 2012 Pat Riehecky <riehecky@fnal.gov> - 6.3-0.rolling
- updated for 6.3 in 6rolling

* Fri Jan 6 2012 Pat Riehecky <riehecky@fnal.gov> - 6.2-0.1.rolling
- Added EULA licence file
- Removed Troy's key from the repos
- Added CERN's key for if they start building packages for us
- Added more abstraction to make making new release rpms easier

* Thu Dec 8 2011 Connie Sieh <csieh@fnal.gov> - 6.2-0.rolling
- Changed everything from 6.1 to 6rolling

* Wed Jul 27 2011 Troy Dawson <dawson@fnal.gov> - 6.1-2
- Didn't quite convert everything from 6rolling to %releasever, fixed it.

* Mon Jul 11 2011 Troy Dawson <dawson@fnal.gov> - 6.1-1
- Changed everything from 6rolling to $releasever

* Wed May 25 2011 Troy Dawson <dawson@fnal.gov> - 6.1-0.1.rolling
- Changed everything from 6.0 to 6rolling
- Separated fastbugs and testing to yum-conf-other

* Fri Feb 18 2011 Troy Dawson <dawson@fnal.gov> - 6.0-6.0.1
- Final release.  Got rid of the many extra numbers in release.

* Fri Feb 18 2011 Troy Dawson <dawson@fnal.gov> - 6.0-6.0.0.37.sl6.1
- Changed everything from 6 to 6.0

* Wed Feb 16 2011 Troy Dawson <dawson@fnal.gov> - 6-6.0.0.37.sl6.1
- Changed everything to it's final setting.

* Tue Nov 16 2010 Troy Dawson <dawson@fnal.gov> - 6-6.0.0.37.sl6
- Changed it to sl-release

* Fri Sep  3 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.37
- Update EULA
- Resolves: rhbz#591512

* Tue Aug 31 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.36
- Remove beta text
- Update EULA
- Resolves: rhbz#622251, rhbz#591512

* Mon Aug 16 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.35
- Bump for GA
- Resolves: rhbz#622251

* Mon Jul 26 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.91-6.0.0.34
- Update yum repos for GA

* Tue Jun 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.91-6.0.0.33
- Update GPL to match standard text

* Tue Jun 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.91-6.0.0.32
- Bump version for post-Beta2

* Wed Jun 16 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.32
- Fix logic for AddOn repos

* Tue Jun 15 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.31
- Only include the AddOn repos in the appropriate arches/variants
- Update the Beta GPG key locations
- Resolves: rhbz#603701, rhbz600288

* Tue Jun  8 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.29
- Combine GPG keys
- Resolves: rhbz#600287, rhbz#600288

* Fri May 28 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.28
- Use a different version value so as to not conflict with GA

* Fri May 28 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.28
- Include the variant in the version field (needed for RHN)
- Update repos for Beta 2
- Resolves: rhbz#594504

* Mon Apr 26 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.27
- Make 'Beta' lowercase in the cpe
- Provide system-release
- Resolves: rhbz#577167 rhbz#578199

* Wed Mar 31 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.25
- Temporarily disable beta repos
- Reverts: rhbz#572308

* Mon Mar 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.24
- Add beta debuginfo repos
- Resolves: rhbz#572308

* Mon Mar 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.23
- Enable yum repo for Beta

* Wed Mar 10 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.21
- Update yum repos for Beta 1

* Fri Feb  5 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.20
- Use the %{?dist} macro
- Related: rhbz#561120

* Wed Feb  3 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.19
- Mark the yum repos as configuration files
- Resolves: rhbz#561277

* Tue Feb  2 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.18
- Use %setup -q to keeep rpmlint happy
- Resolves: rhbz#561120

* Thu Jan 28 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.17
- Bump for Beta
- Related: rhbz#559610

* Tue Nov 17 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.16
- Fix newline issue in RPM-GPG-KEY-redhat-beta-2
- spec file cleanup
- Resolves: rhbz#532992

* Thu Oct  22 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.15
- Spec cleanup (dmach@redhat.com)
- Add the beta-2 and release-2 keys
- Rename the older keys
- Comment out eula.py code until it gets cleaned up
- Resolves: rhbz#530347
- Related: rhbz#526951

* Mon Sep 21 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.14
- Fix typo in cpe name
- Resolves: rhbz#404371

* Fri Sep 18 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.13
- Fix the cpe name
- Resolves: rhbz#404371

* Thu Sep 17 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.12
- Update the release name

* Thu Sep 17 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.11
- Add system-release-cpe
- Resolves: rhbz#404371

* Tue Sep 15 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.10
- Add the 'el6' macro
- Resolves: rhbz#513075

* Tue Sep  1 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.9
- Bump for rebuild

* Tue Aug 11 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.8
- Indicate Alpha instead of Beta
- Resolves: rhbz#513290

* Wed Jun 24 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.7
- Updated eula.py
- Resolves: rhbz#507426

* Tue Jun 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.6
- Add eula.py back
- Resolves: rhbz#507426

* Mon Jun 15 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.5
- add /etc/system-release
- some minor cleanup

* Fri Jun  5 2009 Dennis Gregorovic <dgregor@redhat.com> - 6Server-6.0.0.4
- bump for rebuild

* Fri Jun  5 2009 Dennis Gregorovic <dgregor@redhat.com> - 6Server-6.0.0.3
- Drop firstboot files as they conflict with the firstboot package

* Wed Jun  3 2009 Mike McLean <mikem@redhat.com> - 6Server-6.0.0.1
- initial build for version 6

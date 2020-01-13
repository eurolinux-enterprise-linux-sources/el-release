#
# version_acronym lower case please!
%define version_acronym el

# increment this to get the stuff after the - higher
#  helps for making the rolling one go obsolete
%define release_count 1

# Ok so we are 7.minor_release_version, what should
# that value be?
# NOTE: Becareful here
%define minor_release_version 7

# set ROLLING true for the rolling tree
#  once set it will do the rest for you automatically
#  the only valid values are true and anything else
%define ROLLING false

# setup pretty name
%define beta_directory 7rolling
%define beta_version 7rolling

# #

%define debug_package %{nil}
%define product_family EuroLinux


%define release_name Vatican
%define base_release_version 7
%define full_release_version %{base_release_version}.%{minor_release_version}
%define dist_release_version %{base_release_version}

%define dist .%{version_acronym}%{dist_release_version}


# if we are building for the rolling tree, define beta
%if %(echo %{ROLLING} |grep -c 'true')
    %define beta rolling
%endif

#########################################################

# so we don't discover that the scripts hiding in doc require bash
%global __requires_exclude_from %{_libexecdir}

# this doesn't work.....
# %%global __requires_exclude ^%{_libexecdir}.*

Name:		el-release%{?variant_lowercase:-%{variant_lowercase}}
Version:	%{full_release_version}
Release:        %{release_count}%{?dist}%{?beta:.%{beta}}
Summary:        %{product_family}%{?variant_titlecase: %{variant_titlecase}} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       redhat-release = %{version}-%{release}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{base_release_version}%{?variant_titlecase}
Provides:       system-release(releasever) = %{full_release_version}
Provides:       sl-release = %{version}-%{release}
Provides:       redhat-release = %{version}-%{release}
Provides:       centos-release = %{version}-%{release}
Provides:       oraclelinux-release = %{version}-%{release}
Source0:        %{name}-%{base_release_version}.tar.bz2
Source1:        85-display-manager.preset
Source2:        90-default.preset
%if %(echo %{ROLLING} |grep -c 'true')
Provides:	config(elreleasever) = %{beta_version}
%else
Provides:	config(elreleasever) = %{full_release_version}
%endif

# SL change from TUV:  This has some BuildRequires
BuildRequires:	coreutils systemd

%description
%{product_family}%{?variant_titlecase: %{variant_titlecase}} release files

##########################

# SL change from TUV: Make yum-conf-7x
#%package -n yum-conf-%{version_acronym}%{base_release_version}x
#Provides:	yum-conf-%{base_release_version}x
#Summary:	Utilize %{version_acronym}%{base_release_version}x repos
#Group:          System Environment/Base
#BuildArch:	noarch
#%if %(echo %{ROLLING} |grep -c 'true')
#Provides:	config(elreleasever) = %{beta_version}
#%else
#Provides:	config(slreleasever) = 7x
#%endif

# SL change from TUV: for this package to make any sense
#Requires:	sl-release%{?variant_lowercase:-%{variant_lowercase}}
#Requires:	yum

# SL change from TUV: for our %%preun script
#Requires(preun):	bash
#Requires(preun):	basesystem
#Requires(preun):	coreutils

# SL change from TUV: for our %%postun script
#Requires(postun):	bash
#Requires(postun):	basesystem
#Requires(postun):	coreutils

#%description -n yum-conf-%{version_acronym}%{base_release_version}x
#Configure the default yum repos to utilize the %{product_family}%{?variant_titlecase: %{variant_titlecase}} %{base_release_version}
#latest release.

###############################################################################
%prep
%setup -q -n %{name}-%{base_release_version}
#cp %{_prefix}/lib/yum-plugins/fastestmirror.py .
#patch -p0 < fastestmirror.patch

%build
echo OK

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc

# create /etc/system-release and /etc/redhat-release
echo "%{product_family}%{?variant_titlecase: %{variant_titlecase}} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > %{buildroot}/etc/redhat-release
ln -s redhat-release %{buildroot}/etc/system-release
cat %{buildroot}/etc/redhat-release

# SL change from TUV: /etc/el-release file exists
ln -s redhat-release %{buildroot}/etc/el-release

# create /etc/os-release
# SL change from TUV: HOME_URL
# SL change from TUV: BUG_REPORT_URL
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}%{?variant_titlecase: %{variant_titlecase}}"
VERSION="%{full_release_version} (%{release_name})"
ID="eurolinux"
ID_LIKE="rhel scientific centos fedora"
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family}%{?variant_titlecase: %{variant_titlecase}} %{full_release_version}%{?beta: %{beta}} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:eurolinux:eurolinux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}%{?variant_lowercase::%{variant_lowercase}}"
HOME_URL="http://www.euro-linux.com/"
BUG_REPORT_URL="mailto:euro@euro-linux.com"

REDHAT_BUGZILLA_PRODUCT="%{product_family} %{base_release_version}"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{full_release_version}
REDHAT_SUPPORT_PRODUCT="%{product_family}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{full_release_version}%{?beta: %{beta}}"
EOF
cat %{buildroot}/etc/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:eurolinux:eurolinux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}%{?variant_lowercase::%{variant_lowercase}}" | tr [A-Z] [a-z] > %{buildroot}/etc/system-release-cpe
cat %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# combine GPG keys
cat RPM-GPG-KEY-redhat-release-2 RPM-GPG-KEY-redhat-auxiliary > RPM-GPG-KEY-redhat-release
rm RPM-GPG-KEY-redhat-release-2 RPM-GPG-KEY-redhat-auxiliary
cat RPM-GPG-KEY-redhat-beta-2 RPM-GPG-KEY-redhat-legacy-beta > RPM-GPG-KEY-redhat-beta
rm RPM-GPG-KEY-redhat-beta-2 RPM-GPG-KEY-redhat-legacy-beta
cat RPM-GPG-KEY-redhat-legacy-former RPM-GPG-KEY-redhat-legacy-release RPM-GPG-KEY-redhat-legacy-rhx  > RPM-GPG-KEY-redhat-legacy-other
rm RPM-GPG-KEY-redhat-legacy-former RPM-GPG-KEY-redhat-legacy-release RPM-GPG-KEY-redhat-legacy-rhx

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
done

# Copy Productids
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/product-default

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%rhel %{base_release_version}
%%dist .el7
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/redhat-release
install -m 644 EULA %{buildroot}/%{_datadir}/redhat-release

# SL change from TUV: populate %{_datadir}/%{name}
(cd $RPM_BUILD_ROOT/%{_datadir} ; ln -s redhat-release %{name})

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/redhat-release
install -m 644 GPL %{buildroot}/%{_docdir}/redhat-release

# SL change from TUV: populate %{_docdir}/%{name}
(cd $RPM_BUILD_ROOT/%{_docdir} ; ln -s redhat-release %{name})

# copy systemd presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system-preset/

# SL change from TUV: populate /etc/pki/secure-boot
mkdir -p -m 755 %{buildroot}/etc/pki/secure-boot
install -m 644 SECURE-BOOT-KEY-fnal-sl7-exp-2017-07-26 %{buildroot}/etc/pki/secure-boot
install -m 644 SECURE-BOOT-KEY-fnal-sl7-exp-2020-08-26 %{buildroot}/etc/pki/secure-boot

# SL change from TUV: populate default repos
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d/

#for yumrepo in *.repo; do
#    install -m 644  $yumrepo %{buildroot}%{_sysconfdir}/yum.repos.d/
#done

########################################################################
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
# SL change from TUV: make script for all our triggers later
cat << EOF >>%{buildroot}/%{_libexecdir}/%{name}/set-elrelease.sh
#!/bin/bash
########################################################################
# If not defined, we've yum issues.
# If no file, set to 'point release'
#    for beta this file is packaged within sl-release so this never executes
# If yum-conf-7x is installed and we are not in beta, the file already exists
#    so there is nothing to do
########################################################################
SELFCOPIES=\${1:-0}
TRIGGERCOPIES=\${2:-0}
########################################################################
if [[ ! -f %{_sysconfdir}/yum/vars/elreleasever ]]; then
    if [[ ! -d %{_sysconfdir}/yum/vars/ ]]; then
        %{__mkdir_p} %{_sysconfdir}/yum/vars/
        %{__chmod} 755 %{_sysconfdir}/yum/vars/
    fi
%if 0%{?beta:1}
    echo %{beta_version} > %{_sysconfdir}/yum/vars/elreleasever
%else
    echo %{full_release_version} > %{_sysconfdir}/yum/vars/elreleasever
%endif
    %{__chmod} 644 %{_sysconfdir}/yum/vars/elreleasever
fi

# Make sure metadata looks like we expect, so we should expire
# any existing repomd.xml files but not necessarily the primary.sqlite
THISFILE=\$(mktemp)
echo  '#!/bin/bash' > \${THISFILE}
echo  "yum clean expire-cache" >> \${THISFILE}
echo  "rm -rf /tmp/nohup.out" >> \${THISFILE}
echo  "rm -rf \${THISFILE}" >> \${THISFILE}
%{__chmod} 755 \${THISFILE}
(cd /tmp
 nohup \${THISFILE} &
) >/dev/null 2>&1

EOF

# SL change from TUV: set releasever to a predictable number, 7 - ie %{base_release_version}
mkdir -p %{buildroot}%{_sysconfdir}/yum/vars

# for yum-conf-7x, your $releasever is 7
# I'd say this is the 'expected' behavior for end users
echo %{base_release_version} > %{buildroot}%{_sysconfdir}/yum/vars/releasever

# SL change from TUV: if this is for a 'beta' version, act differently
%if 0%{?beta:1}
    echo "---"
    echo "Customizing for beta version of %{product_family}%{?variant_titlecase: %{variant_titlecase}} for %{beta_directory}"
    echo "---"

    # This one goes into sl-release rather than yum-conf-7 so that our repos point automatically at rolling
    # it is a bit weird that ownership of this file changes between beta and released, but this keeps our
    # repo definitions much cleaner.... I think
    echo %{beta_version} > %{buildroot}%{_sysconfdir}/yum/vars/elreleasever

    echo "---"
%else
    echo "---"
    echo "Building GA repos for %{product_family}%{?variant_titlecase: %{variant_titlecase}}"
    echo "---"
    # for yum-conf-7x, your $elreleasever is 7x
    # I'd say this is the 'expected' behavior for end users
    echo %{base_release_version}x > %{buildroot}%{_sysconfdir}/yum/vars/elreleasever
%endif

# SL change from TUV: Deploy %{_libexecdir}/%{name}/ scripts
#install -m 0750 anaconda-make-service-sl-repos.sh %{buildroot}/%{_libexecdir}/%{name}/anaconda-make-service-sl-repos.sh
install -m 0750 anaconda-make-service-el-scap-xml.sh %{buildroot}/%{_libexecdir}/%{name}/anaconda-make-service-el-scap-xml.sh
#install -m 0750 anaconda-make-service-sl-fastestmirror.sh %{buildroot}/%{_libexecdir}/%{name}/anaconda-make-service-sl-fastestmirror.sh
install -m 0750 anaconda-make-services.sh %{buildroot}/%{_libexecdir}/%{name}/anaconda-make-services.sh
#install -m 0750 anaconda-sl-repos.sh %{buildroot}/%{_libexecdir}/%{name}/anaconda-sl-repos.sh
install -m 0750 anaconda-el-scap-xml.sh %{buildroot}/%{_libexecdir}/%{name}/anaconda-el-scap-xml.sh
#install -m 0750 anaconda-sl-fastestmirror.sh %{buildroot}/%{_libexecdir}/%{name}/anaconda-sl-fastestmirror.sh
#install -m 0644 fastestmirror.py %{buildroot}/%{_libexecdir}/%{name}/fastestmirror.py

##################################################################
##################################################################

%clean
rm -rf %{buildroot}

##################################################################
# SL change from TUV: Post and Triggers
##################################################################

#%postun -p %{_libexecdir}/%{name}/set-elrelease.sh -n yum-conf-%{version_acronym}%{base_release_version}x
##################################################################
# for yum-conf-7x
#    postun runs after all triggerin/un but not triggerpostun
##################################################################

#%preun -p /bin/bash -n yum-conf-%{version_acronym}%{base_release_version}x
##################################################################
# for yum-conf-7x
#    preun runs before everything else
##################################################################
#%if 0%{?beta:1}
#echo "do nothing in beta period" > /dev/null
#%else
#%{__rm} -f %{_sysconfdir}/yum/vars/elreleasever
#%endif



##################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
              # End of yum-conf-7x scripts/triggers #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##################################################################



%triggerin -p %{_libexecdir}/%{name}/set-elrelease.sh -- yum
##################################################################
# for sl-release
#  this trigger lets us define our yum vars without requiring
#  coreutils, this unloops a rather frustrating deploop
#
#  NOTE: this was once a post script, but we had to undo that to
#        make this trigger.
#        See: RITM0137163 or
#             SCIENTIFIC-LINUX-DEVEL@LISTSERV.FNAL.GOV 1 Dec 2014 09:43:35 -0700
##################################################################

%triggerpostun -p %{_libexecdir}/%{name}/set-elrelease.sh -- yum-conf-%{version_acronym}%{base_release_version}x
##################################################################
# for sl-release, runs after postun of yum-conf-7x
##################################################################

%triggerpost -p %{_libexecdir}/%{name}/set-elrelease.sh -- yum-conf-%{version_acronym}%{base_release_version}x
##################################################################
# for sl-release, runs after post of yum-conf-7x, this /should/ always be a noop
##################################################################


%triggerin -p %{_libexecdir}/%{name}/anaconda-make-services.sh -- anaconda
##################################################################
# for sl-release
# anaconda looks for a custom yum root, setup tmpfiles.d to cope

##################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
              # End of sl-release scripts/triggers #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##################################################################

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/%{name}
/etc/system-release
%config /etc/system-release-cpe
%config(noreplace) /etc/os-release
%verify(not md5 size mtime) %config(noreplace) /etc/issue
%verify(not md5 size mtime) %config(noreplace) /etc/issue.net
#%config(noreplace) %{_sysconfdir}/yum.repos.d/*
/etc/pki/rpm-gpg/
/etc/rpm/macros.dist
%{_sysconfdir}/pki/secure-boot/
%{_docdir}/redhat-release/*
%{_docdir}/%{name}
%{_datadir}/redhat-release/*
%{_datadir}/%{name}
%{_prefix}/lib/systemd/system-preset/*
/etc/pki/product-default

# SL change from TUV: stuff for our repos
#%attr(644, root, root)%{_libexecdir}/%{name}/*.py
#%exclude %{_libexecdir}/%{name}/*.pyo
#%exclude %{_libexecdir}/%{name}/*.pyc
%attr(755, root, root)%{_libexecdir}/%{name}/*.sh
# This should only include slreleasever if beta is defined
%if 0%{?beta:1}
%{_sysconfdir}/yum/vars/elreleasever
%else
%ghost %{_sysconfdir}/yum/vars/elreleasever
%endif

# This should only include sl/releasever if beta is not defined
#%files -n yum-conf-%{version_acronym}%{base_release_version}x
%defattr(0644,root,root,0755)
%{_sysconfdir}/yum/vars/releasever
%if 0%{?beta:1}
%ghost %{_sysconfdir}/yum/vars/elreleasever
%else
%{_sysconfdir}/yum/vars/elreleasever
%endif

##################################################################

%changelog
* Fri Aug 30 2019 Cezary Drak <cd@euro-linux.com> 7.7-2
- EuroLinux 7.7 (Vatican)

* Thu Dec 13 2018 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.6
- Bump for EuroLinux 7.6 prod

* Mon May 28 2018 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.5-1
- Version up for initscripts

* Tue May 15 2018 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.5-0
- Pull from upstream for new version


* Thu Oct  5 2017 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.4-0
- Pull from upstream.
- First version for EuroLinux 7.4 (Paris)
 
* Fri Apr 21 2017 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.3-1
- Huge pull from upstream, because of firstboot problem.

* Wed Apr  5 2017 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.3-0
- New release Lisbon

* Mon Mar 21 2016 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.2-0
- Changed version of EL with new codename

* Fri Aug 21 2015 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> 7.1-3
- Old EULA bug fixed 
- SL keys removed
- Removed Trigger for yum-conf-7x, we don't use that packaged - Sun Oct 25 2015
  |- sl-version 7.1-3

* Thu Jul  9 2015 Alex Baranowski <aleksander.baranowski> 7.1-2
- Codename changed

* Thu Jul  9 2015 Alex Baranowski <aleksander.baranowski> 7.1-1
-change set-elrelease.sh to set-slrelease.sh

* Mon Jul 06 2015 Tomasz Cholewa <slashroot@slashroot.eu> - 7.1-0
- Build for EuroLinux 7.1 

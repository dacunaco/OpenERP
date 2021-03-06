# Redhat, crippled, static version of the spec file

Name:           openerp-client
Version:        6.0.3
Release:        0%{?dist}
License:        AGPLv3
Group:          Applications/Databases
Summary:        OpenERP Client
URL:            http://www.openerp.com
Source0:        http://www.openerp.com/download/stable/source/%{name}-%{version}.tar.gz
#                   All non-official patches are contained in:
#                   http://git.hellug.gr/?p=xrg/openerp  and referred submodules
#                   look for the ./redhat folder there, where this .spec file is held, also.
# BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}

# ==== patches.client ====

BuildArch:      noarch
BuildRequires:  python
BuildRequires:  gettext
BuildRequires:  desktop-file-utils, python-setuptools
BuildRequires:  pygtk2-devel, libxslt-python
BuildRequires:  python2-devel
BuildRequires:  jpackage-utils
# Required for /usr/bin/msgfmt.py
BuildRequires:  python-tools

Requires:       pygtk2
Requires:       pygobject2, pygtk2-libglade, pydot, python-lxml
# Requires:     python-matplotlib
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:       hippo-canvas-python
Requires:       python-spiffgtkwidgets
Requires:       python-dateutil
Requires:       mx

%description
Gtk client for Open ERP.

OpenERP is a free Enterprise Resource Planning and Customer Relationship 
Management software. It is mainly developed to meet changing needs.

This package only contains the thin, native client for the ERP application.
After installing this, you will be able to connect to any OpenERP server
running in your local network or the Internet.

%prep
%setup -q
# ==== patches-prep.client ====

sed -i 's/\r//' doc/License.rtf
# Remove the bundled script:
rm -f msgfmt.py

# Remove the bundled lib:
rm -rf bin/SpiffGtkWidgets

%build

PYTHONPATH=%{_bindir} python ./setup.py build --quiet

%install
PYTHONPATH=%{_bindir} python ./setup.py install --root=%{buildroot} --quiet
install -D bin/pixmaps/openerp-icon.png %{buildroot}%{_iconsdir}/openerp-icon.png

# the Python installer plants the RPM_BUILD_ROOT inside the launch scripts, fix that:
pushd %{buildroot}%{_bindir}/
        sed -i "s|%{buildroot}||" %{name}
popd

# When setup.py copies files, it removes the executable bit, so we have to
# restore it here for some scripts:

pushd %{buildroot}%{python_sitelib}/%{name}/
    chmod a+x openerp-client.py
popd


pushd %{buildroot}%{_datadir}/locale
# Adjusting localization names for Albania, Ukraine
        mv al sq
        rm -rf ua # there is already an "uk" file for Ukraine, ua seems old.
popd

%find_lang %{name}

mv %{buildroot}%{_datadir}/openerp-client/* %{buildroot}%{python_sitelib}/%{name}
rm -rf %{buildroot}%{_datadir}/openerp-client

mkdir %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Version=1.0
Name=Open ERP
GenericName=GTK ERP Client
Comment=A gtk client for the open source ERP
Exec=%{_bindir}/%{name}
Icon=openerp-icon
Terminal=false
Type=Application
StartupNotify=true
Categories=Office;GNOME;GTK;
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/*
%{_bindir}/%{name}
%{_iconsdir}/openerp-icon.png
%{python_sitelib}/%{name}/
%{_mandir}/man1/openerp-client.*
%{_datadir}/pixmaps/openerp-client/
%{_datadir}/applications/%{name}.desktop
%{python_sitelib}/openerp_client-%{version}-py%{python_version}.egg-info

%post
%{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null || :
touch --no-create %{_iconsdir} &>/dev/null || :

%postun
if [ -x %{_bindir}/update-desktop-database ]; then %{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null || : ; fi
if [ $1 -eq 0 ] ; then
    touch --no-create %{_iconsdir} &>/dev/null
    gtk-update-icon-cache %{_iconsdir} &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_iconsdir} &>/dev/null || :

%changelog
* Tue Sep 13 2011 P. Christeas <xrg@linux.gr> 6.0.3-0
  + fedora: scripts to generate old-compatible sources/specs from git
  + redhat: consistency and permission fixes in server.spec
  + redhat: consistency fixes in client.spec
  + redhat: expand tabs to spaces, in both spec files

* Mon Sep 12 2011 P. Christeas <xrg@linux.gr> f27e337
  + upstream-commits: mark the hashes of 6.0.3
  + redhat: merge with the rpm-building branches
  + Update all submodules to v6.0.3

* Tue Jun 14 2011 P. Christeas <xrg@linux.gr> 5072656
  + redhat: unbundle SpiffGtkWidgets, bump rel. number

* Fri Jun 10 2011 P. Christeas <xrg@linux.gr> 4c09b47
  + Update submodules addons, server, client to latest 6.0

* Tue May 10 2011 P. Christeas <p_christ@hol.gr> bd6e22f
  + Redhat: spelling fixes for server description
  + Redhat: client: require gettext, unbundle msgfmt.py
  + Redhat: remove web-addon of 'wiki'

* Mon May 9 2011 P. Christeas <p_christ@hol.gr> 0201fa4
  + Redhat: tolerate failures of update-desktop-database
  + Redhat: use _initddir instead of _initrddir

* Thu May 5 2011 P. Christeas <p_christ@hol.gr> 8eee9fd
  + Update submodules server, client, addons
  + Redhat: more description in spec files
  + Redhat: update gtk icons cache, after install

* Thu Apr 28 2011 P. Christeas <p_christ@hol.gr> 30190fb
  + Redhat: cleanup License.rtf at client
  + Redhat: scripts to generate the specs+patches
  + Redhat: update licenses (multiple) for the server
  + Redhat: prepare for patch-based build.
  + Redhat: the %clean section can remain
  + Redhat: refactor the removal of buildroot from /usr/bin scripts
  + Redhat: buildrequire jpackage-utils for %{_iconsdir}
  + Redhat: mark the upstream commits, of 6.0.2
  + Redhat: a helper script to generate patches
  + Redhat: move and rename spec files into redhat/openerp-<sub>.spec
  + Merge remote-tracking branch 'origin/xrg-60' into HEAD

* Fri Apr 22 2011 P. Christeas <p_christ@hol.gr> eec43a2
  + Updated submodules addons, buildbot, client-kde, client-web, extra-addons, libcli, server

* Thu Apr 21 2011 P. Christeas <p_christ@hol.gr> 6.0.2-5
  + Redhat: split the spec into server and client ones
  + Redhat: a few more fixes, to reduce lint errors
  + Merge branch 'official' into xrg-60
  + scripts: generate archives2, like the upstream tarballs
  + server: update for RPM builds
  + Merge remote-tracking branch 'origin/xrg-60' into HEAD
  + Updated addons, client, client-web and server, to latest official-6.0

* Tue Apr 12 2011 P. Christeas <p_christ@hol.gr> 39d1e18
  + mandriva: pull changes from redhat spec, consider mageia

* Mon Apr 11 2011 P. Christeas <p_christ@hol.gr> 4d83114
  + Updated submodules addons, client, server
  + Redhat: remove double-listed requires
  + Redhat: remove embedded pychart, use upstream one

* Sun Apr 10 2011 P. Christeas <p_christ@hol.gr> e3c96ef
  + Redhat: cleanup the %doc files
  + Redhat: remove support for intermediate builds
  + Redhat: remove web-client support
  + Redhat: a few improvements, try to build the web-client

* Sat Apr 9 2011 P. Christeas <p_christ@hol.gr> 0037772
  + Redhat: more cleanup, offer default docs
  + Redhat: remove the kde client
  + Redhat: remove the serverinit sub-package
  + Redhat: cleanup macros, requires
  + Redhat: python build --quiet

* Fri Apr 8 2011 P. Christeas <p_christ@hol.gr> e7eab62
  + Radhat: 6.0.2-2 fix groups, cert script, changelog
  + Mandriva: a few changes in .spec file

* Mon Apr 4 2011 P. Christeas <p_christ@hol.gr> b4c22fc
  + redhat: update to 6.0.2
  + redhat: a couple of fixes for rpmlint
  + redhat: improvements at .spec to comply with Guidelines

* Sun Apr 3 2011 P. Christeas <p_christ@hol.gr> 45596e1
  + redhat: bring the server-check.sh and a patch for init.d
  + RedHat: cleanup the .spec file, fix dependencies

* Sat Apr 2 2011 P. Christeas <p_christ@hol.gr> 3a88941
  + mandriva: demote the class, again, to public

* Fri Apr 1 2011 P. Christeas <p_christ@hol.gr> 7d8252a
  + Mandriva: add some dependencies to .spec file
  + Update to 6.0.2+
  + Redhat spec: strip much of the mandriva logic, make it static
  + RPM: copy spec file from Mandriva/Mageia to RedHat

* Thu Mar 24 2011 P. Christeas <p_christ@hol.gr> b9154b0
  + Initialize submodule for 'libcli', the client library

* Mon Mar 21 2011 P. Christeas <p_christ@hol.gr> 469aa48
  + Remove tests/ , they are in the sandbox now.

* Sun Mar 20 2011 P. Christeas <p_christ@hol.gr> 067bf38
  + Add README about this repository

* Thu Mar 17 2011 P. Christeas <p_christ@hol.gr> 968601a
  + Rewrite last gtk-client patch for SpiffGtkWidgets setup
  + mandriva: require python-lxml for gtk client
  + Updated submodules addons, buildbot, client, client-kde, server
  + tests: one for mails, one to dump the doc nodes cache
  + git: Fix submodule URL of buildbot

* Wed Mar 9 2011 P. Christeas <p_christ@hol.gr> fed8f66
  + Updated submodules addons, client, client-kde, extra-addons, server

* Wed Feb 23 2011 P. Christeas <p_christ@hol.gr> 9beefb7
  + Updated submodules addons, client, client-kde, extra-addons, server

* Sat Feb 19 2011 P. Christeas <p_christ@hol.gr> 23f26ca
  + Updated submodules addons, buildbot, client, client-kde, client-web, extra-addons, server

* Fri Jan 21 2011 P. Christeas <p_christ@hol.gr> a1e11b1
  + Merge branch 'official' into xrg-60
  + RPM spec: adapt to official release, dirs have the right names now.

* Thu Jan 20 2011 P. Christeas <xrg@openerp.com> 939c332
  + Official Release 6.0.1 + debian changelogs

* Thu Jan 20 2011 P. Christeas <p_christ@hol.gr> 536461f
  + Merge release 6.0.1

* Wed Jan 19 2011 P. Christeas <p_christ@hol.gr> 4635463
  + Merge commit 'v6.0.0' into xrg-60
  + Merge 6.0.0 into xrg-60
  + Updated submodules addons, client, server
  + Release 6.0.0
  + RPM spec: have all-modules list, skip bad addons, skip server-check.sh
  + RPM: allow modulize.py to skip bad modules.
  + Reset submodules addons, client*, addons, server to official
  + Mandriva: let spec go closer to other RPM distros
  + Updated submodules addons, client, client-kde, client-web, extra-addons, server

* Sat Jan 15 2011 P. Christeas <p_christ@hol.gr> 7486fe9
  + Updated submodules addons, client, client-kde, client-web, server

* Thu Jan 13 2011 P. Christeas <p_christ@hol.gr> a9b50da
  + Updated submodule client, using improved installer

* Mon Jan 3 2011 P. Christeas <p_christ@hol.gr> bd6aa12
  + Version 6.0.0-rc2 with addons, client, client-web, server

* Sun Jan 2 2011 P. Christeas <p_christ@hol.gr> 7266984
  + Further attempt for a correct client-web installation.
  + client-web: fix installation, under "site-packages/openobject/"


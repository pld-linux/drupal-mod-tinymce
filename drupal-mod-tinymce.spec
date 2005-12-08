%define		modname tinymce
Summary:	Drupal TinyMCE WYSIWYG Editor Module
Summary(pl):	Modu³ edytora WYSIWYG TinyMCE dla Drupala
Name:		drupal-mod-%{modname}
Version:	4.6.0
Release:	0.26
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{modname}-%{version}.tar.gz
# Source0-md5:	050b885a5437c492f2e9d49181db9326
Source1:	%{name}.conf
URL:		http://drupal.org/project/tinymce
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	sed >= 4.0
Requires:	webapps >= 0.2
Requires:	drupal >= 4.6.0
Requires:	tinymce >= 1.44
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		drupal/%{modname}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_drupaldir	%{_datadir}/drupal
%define		_moddir		%{_drupaldir}/modules
%define		_htdocs		%{_drupaldir}/htdocs
%define		_htmlmoddir	%{_htdocs}/modules/%{modname}
%define		_tinymceplugindir	%{_datadir}/tinymce/plugins

%description
Use the TinyMCE WYSIWYG editor for editing site content. A
collaborative project by richardb, mathias and jjeff.

Features include:
- Drupal image upload integration
- Dynamically turn off/on TinyMCE per textarea field
- Assign different tinymce profiles per role

%description -l pl
Ten modu³ pozwala u¿ywaæ edytora WYSIWYG TinyMCE do modyfikowania
tre¶ci stron. Jest to wspólny projekt, który stworzyli richardb,
mathias i jjeff.

Mo¿liwo¶ci obejmuj±:
- integracjê umieszczania obrazków w Drupalu
- dynamiczne wy³±czanie/w³±czanie TinyMCE dla pól textarea
- przypisywanie ró¿nych profili tinymce dla ról

%prep
%setup -q -n %{modname}
rm -f LICENSE.txt # pure GPL

# undos the source
find '(' -name '*.txt' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_moddir}}
install -d $RPM_BUILD_ROOT%{_tinymceplugindir}

install *.module $RPM_BUILD_ROOT%{_moddir}
cp -a plugins/* $RPM_BUILD_ROOT%{_tinymceplugindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

install -d $RPM_BUILD_ROOT%{_moddir}/tinymce/jscripts
ln -s %{_datadir}/tinymce $RPM_BUILD_ROOT%{_moddir}/tinymce/jscripts/tiny_mce

# need symlink for drupal to think the file is there, we also do
# apache alias as the symlinks aren't usually allowed in htdocs
install -d $RPM_BUILD_ROOT%{_htmlmoddir}/jscripts
ln -s %{_datadir}/tinymce $RPM_BUILD_ROOT%{_htmlmoddir}/jscripts/tiny_mce

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
If this your first install of %{modname} module, load the database definition file:
zcat %{_docdir}/%{name}-%{version}/tinymce.mysql.gz | mysql drupal

EOF
fi

%triggerin -- apache1
# TODO install it only if this apache instance has drupal configured
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
# TODO install it only if this apache instance has drupal configured
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 4.6.0-0.25
# migrate from apache-config macros
if [ -f /etc/drupal/apache-tinymce.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/drupal/apache-tinymce.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/drupal/apache-tinymce.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/drupal/apache-tinymce.conf.rpmsave
fi

# place new config location, as trigger puts config only on first install, do it here.
if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
	rm -f /etc/apache/conf.d/99_%{name}.conf
	/usr/sbin/webapp register apache %{_webapp}
	apache_reload=1
fi
if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi
if [ "$apache_reload" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache reload 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.txt tinymce.{mysql,pgsql}
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%{_moddir}/*.module
%{_moddir}/tinymce
%{_tinymceplugindir}/*
%{_htmlmoddir}

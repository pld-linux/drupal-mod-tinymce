%define		modname tinymce
Summary:	Drupal TinyMCE WYSIWYG Editor Module
Summary(pl):	Modu³ edytora WYSIWYG TinyMCE dla Drupala
Name:		drupal-mod-%{modname}
Version:	4.6.0
Release:	0.16
Epoch:		0
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{modname}-%{version}.tar.gz
# Source0-md5:	dd7630860baf1f7f470d71c272d275eb
Source1:	%{name}.conf
URL:		http://drupal.org/project/tinymce
BuildRequires:	rpmbuild(macros) >= 1.194
BuildRequires:	sed >= 4.0
Requires:	drupal >= 4.6.0
Requires:	tinymce >= 1.44
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/drupal
%define		_moddir		%{_datadir}/drupal/modules
%define		_htmlmoddir	%{_datadir}/drupal/htdocs/modules
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
find '(' -name '*.txt' ')' -print0 | xargs -0 sed -i -e 's,
$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_moddir},%{_htmlmoddir}}
install -d $RPM_BUILD_ROOT%{_tinymceplugindir}

install *.module $RPM_BUILD_ROOT%{_moddir}
cp -a plugins/* $RPM_BUILD_ROOT%{_tinymceplugindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{modname}.conf

install -d $RPM_BUILD_ROOT%{_htmlmoddir}/tinymce/jscripts
ln -s %{_datadir}/tinymce $RPM_BUILD_ROOT%{_htmlmoddir}/tinymce/jscripts/tiny_mce
ln -s ../htdocs/modules/tinymce $RPM_BUILD_ROOT%{_moddir}/tinymce

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
If this your first install of %{modname} module, load the database definition file:
zcat %{_docdir}/%{name}-%{version}/tinymce.mysql.gz | mysql drupal

EOF
fi

%files
%defattr(644,root,root,755)
%doc *.txt tinymce.{mysql,pgsql}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%{_moddir}/*.module
%{_moddir}/tinymce
%{_htmlmoddir}/tinymce
%{_tinymceplugindir}/*

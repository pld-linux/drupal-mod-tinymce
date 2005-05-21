%define		modname tinymce
Summary:	Drupal TinyMCE WYSIWYG Editor Module
Summary(pl):	Modu³ edytora WYSIWYG TinyMCE dla Drupala
Name:		drupal-mod-%{modname}
Version:	4.6.0
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/WWW
Source0:	http://drupal.org/files/projects/%{modname}-%{version}.tar.gz
# Source0-md5:	dd7630860baf1f7f470d71c272d275eb
URL:		http://drupal.org/project/tinymce
Requires:	drupal >= 4.6.0
Requires:	tinymce
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_moddir		%{_datadir}/drupal/modules

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_moddir}

install *.module $RPM_BUILD_ROOT%{_moddir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt
%{_moddir}/*.module

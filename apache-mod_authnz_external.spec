%define	mod_name	authnz_external
%define apxs		/usr/sbin/apxs
Summary:	Basic authentication for the Apache Web server using arbitrary shell commands
Summary(cs):	Základní autentizace pro WWW server Apache pomocí shellových pøíkazù
Summary(da):	En autenticeringsmodul for webtjeneren Apache hvor man kan bruge vilkårlige skal-kommandoer
Summary(de):	Authentifizierung für den Apache Web-Server, der arbiträre Shell-Befehle verwendet
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant des commandes shell arbitraires
Summary(it):	Autenticazione di base per il server Web Apache mediante comandi arbitrari della shell
Summary(nb):	En autentiseringsmodul for webtjeneren Apache der en kan bruke skall-kommandoer
Summary(pl):	Podstawowy modu³ uwierzytelnienia dla Apache, u¿ywaj±cy poleceñ pow³oki
Summary(pt):	Um módulo de autenticação de LDAP para o servidor Web Apache
Summary(sl):	Osnovna avtentikacija za spletni stre¾nik Apache, z uporabo poljubnih lupinskih ukazov
Summary(sv):	Grundläggande autentisering för webbservern Apache med valfria skalkommandon
Name:		apache-mod_%{mod_name}
Version:	3.1.0
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://unixpapa.com/software/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	5051bffe6a3992336f4a9f84430a58d2
URL:		http://unixpapa.com/mod_auth_external.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This module allows you to use any command line program to authenticate
a user.

%description -l cs
Balíèek mod_auth_external slou¾í pro omezení pøístupu k dokumentùm,
které poskytuje WWW server Apache. Jména a hesla jsou kontrolována
pomocí jakéhokoliv pøíkazu (jeho návratovým kódem).

%description -l de
Mod_auth_external kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschränken, indem es den Rückcode
eines gegebenen arbiträren Befehls prüft.

%description -l es
Mod_auth_external puede usarse para limitar el acceso a documentos
servidos desde un servidor web verificando el código de retorno de un
comando arbitrario especificado.

%description -l fr
Mod_auth_external peut être utilisé pour limiter l'accès à des
documents servis par un serveur Web en vérifiant le code de retour
d'une commande spécifiée arbitraire.

%description -l it
Mod_auth_external può essere utilizzato per limitare l'accesso ai
documenti serviti da un server Web controllando il codice di ritorno
di un dato comando arbitrario.

%description -l ja
Mod_auth_external
¤ÏÇ¤°Õ¤Ë»ØÄê¤µ¤ì¤¿¥³¥Þ¥ó¥É¤ÎÌá¤ê¥³¡¼¥É¤ò¥Á¥§¥Ã¥¯¤¹¤ë¤³¤È ¤Ë¤è¤Ã¤Æ¡¢Web
¥µ¡¼¥Ð¡¼¤¬Äó¶¡¤¹¤ë¥É¥­¥å¥á¥ó¥È¤Ø¤Î¥¢¥¯¥»¥¹¤òÀ©¸Â¤¹¤ë¤³¤È ¤¬¤Ç¤­¤Þ¤¹¡£

%description -l pl
Ten modu³ pozwala na u¿ycie dowolnego programu dzia³aj±cego z linii
poleceñ do uwierzytelniania u¿ytkownika.

%description -l sv
Mod_auth_external kan användas för att begränsa åtkomsten till
dokument servade av en webbserver genom att kontrollera returkoden
från ett godtyckligt angivet kommando.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf/}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc TODO AUTHENTICATORS CHANGES README INSTALL test mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so

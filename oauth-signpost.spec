Name:		oauth-signpost
Version:	2.1.1
Release:	1
Summary:	OAuth 1.0a signing for Java HTTP requests
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/mttkay/signpost
# Tag oauth-signpost-2.1.1. signpost-core is plain Java. The httpclient
# modules are not built. DefaultOAuthConsumer signs HttpURLConnection.
Source0:	oauth-signpost-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-21-openjdk-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem

%description
oauth.signpost:signpost-core %{version}.
DefaultOAuthConsumer signs an HttpURLConnection with an OAuth 1.0a
Authorization header and can also sign a URL query string.

%prep
%autosetup -n oauth-signpost-%{version}
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE
test -s signpost-core/src/main/java/oauth/signpost/basic/DefaultOAuthConsumer.java
test -s compile.sh
test -s check.sh

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./compile.sh %{version}

%install
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
mkdir -p %{buildroot}
sysjar install --buildroot %{buildroot} \
	--artifact build/signpost-core.pom:build/signpost-core.jar \
	--file-name signpost-core \
	--filelist files.list
test -s %{buildroot}%{_javadir}/signpost-core.jar

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./check.sh %{buildroot}%{_javadir}/signpost-core.jar

%files -f files.list
%license LICENSE

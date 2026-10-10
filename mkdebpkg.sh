#!/bin/sh

PKGNAME=`tomlq -r '.tool.poetry.name' pyproject.toml`
PKGVER=`tomlq -r '.tool.poetry.version' pyproject.toml`
SCRIPT_ENTRY=`tomlq -r '.tool.poetry.scripts.opncli' pyproject.toml`

ARCH=all
OUTPUTDIR=.

WHLPKGNAME=`echo $PKGNAME | tr '-' '_'`

package_whl="dist/${WHLPKGNAME}-${PKGVER}-py3-none-any.whl"

extract()
{
  rm -rf work/dest/
  DESTDIR="work/dest/${PKGNAME}-${PKGVER}"
  dist_packages="$DESTDIR/usr/lib/python3/dist-packages"
  mkdir -p $dist_packages

  unzip $package_whl -d $dist_packages/
}

package()
{
  echo -n "create package ... "
  echo ""
  maintainer=`git config --get user.name`
  email=`git config --get user.email`

  mkdir -p $DESTDIR/DEBIAN
  cat << EOS > $DESTDIR/DEBIAN/control
Package: $PKGNAME
Maintainer: $maintainer <$email>
Architecture: $ARCH
Version: $PKGVER
Depends: python3, python3-dotenv, python3-requests, python3-yaml
Description: $PKGNAME
EOS

   mkdir -p $DESTDIR/usr/bin/
   cp -f opncli $DESTDIR/usr/bin/
#  cp -f postinst $DESTDIR/DEBIAN/
#  cp -f postrm   $DESTDIR/DEBIAN/
#  cp -f prerm    $DESTDIR/DEBIAN/
  fakeroot dpkg-deb --build $DESTDIR $OUTPUTDIR
  echo "done"
}

extract
package


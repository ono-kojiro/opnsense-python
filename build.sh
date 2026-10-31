#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

PKGNAME=`tomlq -r '.project.name' pyproject.toml`
PKGVER=`tomlq -r '.project.version' pyproject.toml`
SCRIPT_ENTRY=`tomlq -r '.project.scripts.opncli' pyproject.toml`

ARCH=all
OUTPUTDIR=.
WHLPKGNAME=`echo $PKGNAME | tr '-' '_'`
package_whl="dist/${WHLPKGNAME}-${PKGVER}-py3-none-any.whl"
package_deb="${PKGNAME}_${PKGVER}_${ARCH}.deb"

flags=""

help()
{
  usage
}

usage()
{
  cat << EOS
usage : $0 [options] target1 target2 ...

  target:
    build
    pytest
EOS

}

all()
{
  :
}

prepare()
{
  python3 -m pip install -e .
  python3 -m pip install .[dev]
}

wheel()
{
  python3 -m build
}

build()
{
  wheel 
  deb
}

pytest()
{
  command pytest ${flags}
}

install()
{
  cp -f ${package_deb} /tmp/
  sudo apt -y install /tmp/${package_deb}
  rm -f /tmp/${package_deb}
}

uninstall()
{
  sudo apt -y remove --purge ${PKGNAME}
}

reinst()
{
  uninstall
  install
}

test()
{
  command pytest -s
}

extract_whl()
{
  rm -rf work/dest/
  DESTDIR="work/dest/${PKGNAME}-${PKGVER}"
  dist_packages="$DESTDIR/usr/lib/python3/dist-packages"
  mkdir -p $dist_packages

  unzip $package_whl -d $dist_packages/
}

control()
{
  set -a
  export maintainer=`git config --get user.name`
  export email=`git config --get user.email`

  export PKGNAME=${PKGNAME}
  export PKGVER=${PKGVER}
  cat control.in \
      | envsubst '${PKGNAME} ${maintainer} ${email} ${PKGVER}' \
      > debian/control
  set +a
}

package()
{
  dpkg-buildpackage -us -uc
}

deb()
{
  extract_whl

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
  fakeroot dpkg-deb --build $DESTDIR $OUTPUTDIR
  echo "done"
}

args=""
while [ "$#" -ne 0 ]; do
  case $1 in
    -h )
      usage
      exit 1
      ;;
    -v )
      verbose=1
      ;;
    -* )
      flags="$flags $1"
      ;;
    * )
      args="$args $1"
      ;;
  esac
  
  shift
done

if [ -z "$args" ]; then
  help
  exit 1
fi

for target in $args; do
  target=`echo $target | tr '-' '_'`
  num=`LANG=C type $target 2>&1 | grep 'function' | wc -l`
  if [ "$num" -ne 0 ]; then
    $target
  else
    #echo "ERROR : $target is not shell function"
    #exit 1
    default $target
  fi
done


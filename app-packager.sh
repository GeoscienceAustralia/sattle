#! /bin/bash
# build a rpm package for django project (sattle) 
# Usage:   ./app-packager.sh ../sattle
# input:     ../sattle 
# output:    /tmp/$USER/RPMS/noarch/*.rpm

topdir=/tmp/$USER
scriptdir=$PWD
bsname=`basename $scriptdir`

if [ $# -lt 1 ]; then
    echo "USAGE: $0 path2django_projdir"
    exit 1
fi

mkdir -p $topdir/{RPMS,SOURCES,SPECS,SRPMS}
tar --exclude=.git -zcvf $topdir/SOURCES/$bsname.tar.gz $1 


cd $topdir

#rpmbuild -bb --define "_topdir $PWD" ../fetch_tle_config.spec
rpmbuild -ba --define "_topdir $PWD" $scriptdir/app-rpm.spec

echo "listing the new rpm package content by rpm -qlp ------------------------------ "
#rpm -qlp RPMS/noarch/noarch.rpm
echo "test extracting the script from the new rpm package ------------------------------ "
#rpm -qp --scripts RPMS/noarch/noarch.rpm > scripts_from_rpm

echo todo: how to avoid .pyo, .pyc files in the rpm package?
echo todo: post-rpm-install setup.sh run as rms_usr


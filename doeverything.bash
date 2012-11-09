#!/bin/bash
prepare_old_database ()
{
  pushd systems/scripts
  python createOldData.python
  popd
}

prepare_old_keplerdatabase ()
{
  pushd systems/kepler/scripts
  python createOldData.python
  popd
}

prepare_old_iphone ()
{
  pushd data_iphone/scripts
  python createIPhoneData.python
  popd
}

prepare_iphone ()
{
  pushd systems/iphone
  python createIPhoneData.python
  popd
}

commit (){
  git add *
  git commit -a -m "$1"
}


prepare_old_database
commit "automatic update: prepare_old_database"
prepare_old_keplerdatabase
commit "automatic update: prepare_old_keplerdatabase"
prepare_old_iphone
commit "automatic update: prepare_old_iphone"
prepare_iphone
commit "automatic update: prepare_iphone"

#git push

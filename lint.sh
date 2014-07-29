#!/bin/bash
# Copyright (c) 2014, Hung Nguyen Viet
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: Hung Nguyen Viet <hvnsweeting@gmail.com>
# Maintainer: Hung Nguyen Viet <hvnsweeting@gmail.com>
#
# A simple salt formula style checker

dir=${1:-.}

function check_result_print() {

  if [ "$?" -eq 0 ]; then
    echo '**************'
    echo -e "$1"
    echo '**************'
    echo
    echo
  fi
}

function check_pip_installed() {
  grep -Rin '^  pip:' -A1 $dir | grep -B1 '\- installed'
  check_result_print  "Manages requirements.txt file and uses module pip.install instead to avoid pip rerun every time"
}

function check_bad_state_style {
  find $dir -name '*.sls' -type f -exec grep -e '^  \w*\.\w*:' {} \;  -exec echo found in {} \;
  check_result_print "Use \nstate:\n  - function\nstyle instead"
}

function check_number_of_last_order {
  grep -Rc '\- order: last' $dir | egrep -v ':0|:1'
  check_result_print "Only one '- order: last' takes effect, use only one of that and replace other with specific requisite (maybe you want require sls: sls_file)"
}

function check_SLS_include_salt_minion {
  grep -Rin '^  \- salt.minion$' -B1 $dir | grep -v ' if '
  check_result_print "In CI, salt.minion must not be included by ANY SLS. To allow CI test for SLS included it, wrap if condition to only allow them when not in CI test"
}

function check_bad_pillar_usage {
  find $dir -name '*.sls' -or -name '*.jinja2' -print0 | xargs -0 grep -E "pillar\.get'\]\([^,]+\)"
  check_result_print "Use pillar['key1']['key2'] if 'key2' is a mandatory key. Using salt['pillar.get'] must provide an optional value"
}

function check_pillar_get_usage {
  find $dir -name '*.sls' -or -name '*.jinja2' -print0 | xargs -0 grep -Rin pillar.get\(
  check_result_print "pillar.get is buggy, uses salt['pillar.get']"
}

check_pip_installed
check_bad_state_style
check_number_of_last_order
check_SLS_include_salt_minion
check_bad_pillar_usage

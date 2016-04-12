#!/bin/bash

glidein_config=$1

#if [ "${GLIDEIN_Site}" = "T3_US_HEPCloud" ];
if [ 1 = 1 ];
then
    scramdir=$(mktemp -d)

    condor_vars_file=`grep -i "^CONDOR_VARS_FILE " $glidein_config | awk '{print $2}'` 
    add_config_line_source=`grep '^ADD_CONFIG_LINE_SOURCE ' $glidein_config | awk '{print $2}'`
    source $add_config_line_source 
    add_condor_vars_line GLIDEIN_SCRAM_PATH "S" "-" "+" "Y" "Y" "@"
    add_config_line GLIDEIN_SCRAM_PATH "$scramdir"

    GLIDEIN_CURL_PATH=`grep '^GLIDEIN_CURL_PATH ' $glidein_config | awk '{print $2}'`

    cat <<'EOF' > ${scramdir}/scramv1

#!/bin/bash

scram "$@"

if [ x$1 == "xruntime" ]; then
    if [ x$2 == "x-csh" ]; then
	echo setenv PATH ${GLIDEIN_CURL_PATH}:\$\{PATH\}
    fi
    if [ x$2 == "x-sh" ]; then
	echo export PATH=${GLIDEIN_CURL_PATH}:\$\{PATH\}
    fi

fi

EOF

chmod +x ${scramdir}/scramv1

fi

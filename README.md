# glidein-scripts

These represent a few scripts needed to enable CMS on AWS.

   * check-preempt-wrap.sh: A script which generates check-preemption.sh, which wakes up every 20 seconds and sends SIGQUIT (fast shutdown) to the condor_master process if the node is being preempted
   * curl.py: A wrapper script which adds AWS authentication headers using STS or environment variables
      * make-curl-wrap.sh: A script to create the curl-wrap.sh generator script
   * scram-wrap.sh: A generator script that creates scramv1, a wrapper that calls scram and then prepends the path for the curl wrapper
   * cmsset_local.sh: A bootstrap script that should be included in the image in /etc/cvmfs


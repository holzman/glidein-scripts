#!/usr/bin/python

import hashlib
import urlparse
import time
import hmac
import os
import sys

aws_id = os.getenv('S3_ACCESS_KEY', 'AKIAIOSFODNN7EXAMPLE')
key = os.getenv('S3_SECRET_KEY', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')
session_token = os.getenv('S3_SESSION_TOKEN')

url = "https://s3-us-west-2.amazonaws.com/hepcloud-cms/burt_test/hsimple.root"

def parse_url(url):
    # only parsing non-vhost style:
    # https://s3-us-west-2.amazonaws.com/hepcloud-cms/burt_test/hsimple.root

    regions = ['us-east-1', 'us-west-1', 'us-west-2', 'eu-west-1', 'eu-central-1',
               'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ap-northeast-2',
               'sa-east-1']
    parsed_url = urlparse.urlparse(url)
    netlocList = parsed_url.netloc.split(".", 1)
    region = None

    for r in regions:
        if r in netlocList[0]:
            region = r
            break

    if not region:
        print "NO REGION"
        sys.exit(1)

    return (parsed_url.netloc, parsed_url.path, region)

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(("AWS4" + key).encode("utf-8"), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = hmac.new(kService, "aws4_request".encode("utf-8"), hashlib.sha256).digest()
    return kSigning

now = time.gmtime()

datestamp = time.strftime("%Y%m%d", now)
timestamp = time.strftime("%Y%m%dT%H%M%SZ", now)

empty_hash = hashlib.sha256('').hexdigest()

host, path, region = parse_url(url)

request = "GET\n%s\n\n" % path
request += "host:%s\n" % host
request += "x-amz-content-sha256:%s\n" % empty_hash
request += "x-amz-date:%s\n" % timestamp
request += "x-amz-security-token:%s\n\n" % session_token
request += "host;x-amz-content-sha256;x-amz-date;x-amz-security-token\n"
request += empty_hash

scope = datestamp + "/%s/s3/aws4_request" % region

stringToSign = 'AWS4-HMAC-SHA256\n%s\n%s\n%s' % (timestamp, scope,
                                                   hashlib.sha256(request).hexdigest())

signKey = getSignatureKey(key, datestamp, region, 's3')
signature = hmac.new(signKey, (stringToSign).encode('utf-8'), hashlib.sha256).hexdigest()

auth_header = 'Authorization: AWS4-HMAC-SHA256 Credential=%s/%s, SignedHeaders=host;x-amz-content-sha256;x-amz-date;x-amz-security-token,' \
    'Signature=%s' % (aws_id, scope, signature)

cmd = 'curl -v %s ' % url + \
    '-H "%s" ' % auth_header + \
    '-H "x-amz-content-sha256: %s" ' % empty_hash + \
    '-H "x-amz-security-token: %s" ' % session_token + \
    '-H "x-amz-date: %s" ' % timestamp

print cmd

cmd=$(curl 'https://mlp.stable.caila-x-sls.test-ai.net/api/mlpgate/account/1023067/model/1183740/external'   -H 'cookie: CC-SESSION-ID=F67BZbA5-Gud_Tbhx2LnSTSfJlOCGyaLcLhoGTRkzJM'   -H 'x-xsrf-token: WRCraabpnEIjhhPUhP-XCJi86C-FdnWDDiFr4iFeMxk' -X POST --silent | jq .dockerRunCommand -r)

echo CMD
echo
echo $cmd

eval "$cmd"

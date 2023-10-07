ids=$(curl 'https://mlp.stable.caila-x-sls.test-ai.net/api/mlpgate/account/1023067/model/1183740/external'   -H 'cookie: CC-SESSION-ID=F67BZbA5-Gud_Tbhx2LnSTSfJlOCGyaLcLhoGTRkzJM'   -H 'x-xsrf-token: WRCraabpnEIjhhPUhP-XCJi86C-FdnWDDiFr4iFeMxk' --silent | jq .[].id.instanceId)

echo $ids
for i in $ids
do

	curl -H 'cookie: CC-SESSION-ID=F67BZbA5-Gud_Tbhx2LnSTSfJlOCGyaLcLhoGTRkzJM'   -H 'x-xsrf-token: WRCraabpnEIjhhPUhP-XCJi86C-FdnWDDiFr4iFeMxk' \
	"https://mlp.stable.caila-x-sls.test-ai.net/api/mlpgate/account/1023067/model/1183740/external/$i" -X DELETE --silent

done

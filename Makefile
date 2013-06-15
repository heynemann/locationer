run:
	@PYTHONPATH=.:$$PYTHONPATH python locationer/server.py -vvv -d -c ./locationer/local.conf

setup:
	@pip install -r requirements.txt

kill_redis:
	-redis-cli -p 7775 shutdown

redis: kill_redis
	redis-server redis.conf ; sleep 1
	redis-cli -p 7775 info

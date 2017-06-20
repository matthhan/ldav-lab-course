mysql --batch --quick --user=ldavlab_matthias --password=$MYSQL_PASSWORD --host=dolgi.informatik.rwth-aachen.de --database=ldavlab < query_tmg.sql | tr '\t' ',' > tmg_jn_accesses.sh 

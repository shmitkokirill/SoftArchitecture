#!/bin/bash

# $1 - start date
host='172.17.0.1'
start_d=$(date -d "$1" +%Y-%m-%d);

declare -a dates;

dates+=($start_d);
for (( j=1; j < 6; j++ ));
do
    dates+=($(date -d "${dates[(( $j-1 ))]} + 7 days" +%Y-%m-%d));
done

export PGPASSWORD='111'; psql -h $host -U 'kirill' \
            -d 'university' \
            -c "
create or replace function partition_for_visits() returns trigger as \$\$
BEGIN
    IF ( NEW.date >= '${dates[0]}'::DATE AND NEW.date < '${dates[1]}'::DATE ) THEN    
            INSERT INTO visit_0 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[1]}'::DATE AND NEW.date < '${dates[2]}'::DATE ) THEN  
            INSERT INTO visit_1 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[2]}'::DATE AND NEW.date < '${dates[3]}'::DATE ) THEN  
            INSERT INTO visit_2 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[3]}'::DATE AND NEW.date < '${dates[4]}'::DATE ) THEN  
            INSERT INTO visit_3 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[4]}'::DATE AND NEW.date < '${dates[5]}'::DATE ) THEN  
            INSERT INTO visit_4 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[5]}'::DATE AND NEW.date < '${dates[6]}'::DATE ) THEN  
            INSERT INTO visit_5 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[6]}'::DATE AND NEW.date < '${dates[7]}'::DATE ) THEN  
            INSERT INTO visit_6 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[7]}'::DATE AND NEW.date < '${dates[8]}'::DATE ) THEN  
            INSERT INTO visit_7 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[8]}'::DATE AND NEW.date < '${dates[9]}'::DATE ) THEN  
            INSERT INTO visit_8 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[9]}'::DATE AND NEW.date < '${dates[10]}'::DATE ) THEN  
            INSERT INTO visit_9 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[10]}'::DATE AND NEW.date < '${dates[11]}'::DATE ) THEN  
            INSERT INTO visit_10 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[11]}'::DATE AND NEW.date < '${dates[12]}'::DATE ) THEN  
            INSERT INTO visit_11 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[12]}'::DATE AND NEW.date < '${dates[13]}'::DATE ) THEN  
            INSERT INTO visit_12 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[13]}'::DATE AND NEW.date < '${dates[14]}'::DATE ) THEN  
            INSERT INTO visit_13 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[14]}'::DATE AND NEW.date < '${dates[15]}'::DATE ) THEN  
            INSERT INTO visit_14 VALUES (NEW.*);
    ELSIF ( NEW.date >= '${dates[15]}'::DATE) THEN  
            INSERT INTO visit_15 VALUES (NEW.*);
    END IF;
    return NULL;
END;
\$\$ language plpgsql;
";

export PGPASSWORD='111'; psql -h $host -U 'kirill' \
            -d 'university' \
            -c "create trigger partition_visits before insert on 
                    VISIT for each row execute 
                        procedure partition_for_visits();";
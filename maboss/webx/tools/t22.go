package main

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
	"log"
	"time"
)

func main() {
	db, err := sql.Open("postgres", "postgres://postgres:py03thon@localhost:5432/maboss?sslmode=disable")
	if err != nil {
		log.Fatal(err)
	}

	statement := "update test_station set lastupdatedby = 'abc' where pk_test_station_id = 9"

	db.Query(statement)

	// db.Query("commit")

	facility := "GCIC"

	rows, err := db.Query("select pk_test_station_id,  laststate, now(), createdby from test_station where facility=$1 order by 1", facility)

	if err != nil {
		log.Fatal(err)
	} else {
		fmt.Println("rows")

		for rows.Next() {

			var id int
			var laststate int
			var ctime time.Time //type time.Time
			var createdby string

			err = rows.Scan(&id, &laststate, &ctime, &createdby)

			if err != nil {
				fmt.Printf("rows.Scan error: %v\n", err)
				//return err
			}
			layout := "2006-01-02 15:04:05.999999999 -0700 MST"
			fmt.Printf("[%v] laststate: %v createdby: %v -- %v\n", id, laststate, createdby, ctime.Format(layout))

		}

	}
}

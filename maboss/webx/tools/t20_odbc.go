
package main;

import (
	"fmt"
	"database/sql"
	_"odbc/driver"
)

func main(){
	conn,err := sql.Open("odbc","driver={SQL Server};SERVER=192.168.0.7;UID=sa;PWD=sa123456;DATABASE=abdb1");
	if(err!=nil){
		fmt.Println("Connecting Error");
		return;
	}
	defer conn.Close();
	stmt,err := conn.Prepare("select top 5 id from ab_contents");
	if(err!=nil){
		fmt.Println("Query Error",err);
		return;
	}
	defer stmt.Close();
	row,err := stmt.Query();
	if err!=nil {
		fmt.Println("Query Error",err);
		return;
	}
	defer row.Close();
	for row.Next() {
		var id int;
		if err := row.Scan(&id);err==nil {
			fmt.Println(id);
		}
	}
	fmt.Printf("%s\n","finish");
	return;
}
package org;


import lombok.Data;

@Data
public class User {
    private String password="123";
    public String username="HIT";

    User(String username,String password){
        this.password=password;
        this.username=username;
    }
    User(){}

}

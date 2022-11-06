package org.spring1111;


import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component("jdbc")
@ConfigurationProperties("jdbc")
@Data
public class Jdbc {
    private String driverName="jdbc";
    private String url;
    private String username;
    private  String password;
}

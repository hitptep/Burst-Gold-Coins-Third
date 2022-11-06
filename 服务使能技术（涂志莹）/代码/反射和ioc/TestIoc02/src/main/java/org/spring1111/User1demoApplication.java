package org.spring1111;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.PropertySource;

@SpringBootApplication


/*@PropertySource("classpath:jdbc.properties")*/
@PropertySource(("classpath:jdbc.properties"))
public class User1demoApplication {
    public static void main(String[] args) {
        ConfigurableApplicationContext context= SpringApplication.run(User1demoApplication.class,args);
 /*       String strl=context.getEnvironment().getProperty("database.password");
        System.out.println(strl);*/

/*        DataBase db=(DataBase) context.getBean("database");
        System.out.println("driverName:" + db.getDriverName());*/

        Jdbc jdbc=(Jdbc) context.getBean("jdbc");
        System.out.println("drivername:"+jdbc.getDriverName());
    }
}

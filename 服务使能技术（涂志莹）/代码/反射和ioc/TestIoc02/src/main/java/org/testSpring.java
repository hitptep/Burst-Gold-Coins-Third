package org;

import org.wgr.service.CustomerService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class testSpring {
    public static void main(String[] args) {
        ApplicationContext ac= new AnnotationConfigApplicationContext(WgrSpringConfig.class);
        CustomerService ds = (CustomerService) ac.getBean("customerService");
        ds.save();
    }
}

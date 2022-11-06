package org;

import org.wgr.service.CustomerService;
import org.wgr.serviceimpl.CustomerServiceImpl;

public class ActionDemo {
    public static void main(String[] args) {
        CustomerService customerService=new CustomerServiceImpl();
        customerService.save();
    }
}

package org;

import org.wgr.dao.CustomerDao;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class DemoTest {
    public static void main(String[] args) {
        //初始化spring容器
        ApplicationContext ac = new ClassPathXmlApplicationContext("applicationContext.xml");


        CustomerDao customerDao=(CustomerDao) ac.getBean("customerDao");
        customerDao.save();
    }
}

package org.wgr.serviceimpl;

import org.springframework.beans.factory.annotation.Qualifier;
import org.wgr.dao.CustomerDao;
import org.wgr.service.CustomerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service(value = "customerService")
public class CustomerServiceImpl implements CustomerService {
    //private CustomerDao cd=new CustomerDaoImpl01();
    //private CustomerDao cd=(CustomerDao) BeanFactory.getBean("customerDao");
    @Autowired
    @Qualifier("customerDao")
    private CustomerDao cd;
    @Override
    public void save() {
        cd.save();
    }
}

package org.wgr.daoimpl;

import org.wgr.dao.CustomerDao;
import org.springframework.stereotype.Repository;


@Repository(value = "customerDao")
public class CustomerDaoImpl01 implements CustomerDao {
    @Override
    public void save(){
        System.out.println("存入数据库");
    }
}

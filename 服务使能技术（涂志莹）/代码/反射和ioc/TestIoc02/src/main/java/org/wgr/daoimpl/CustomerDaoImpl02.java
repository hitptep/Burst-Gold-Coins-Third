package org.wgr.daoimpl;

import org.wgr.dao.CustomerDao;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Repository;


@Primary
@Repository(value = "customerDao1")
public class CustomerDaoImpl02 implements CustomerDao {
    @Override
    public void save() {
        System.out.println("存入Oracle数据库");
    }
}

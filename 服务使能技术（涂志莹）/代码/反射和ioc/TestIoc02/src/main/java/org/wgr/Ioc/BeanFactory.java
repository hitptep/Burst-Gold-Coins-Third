package org.wgr.Ioc;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class BeanFactory {

    //加载配置文件
    private  static Properties properties=new Properties();
    static {
        InputStream in = BeanFactory.class.getResourceAsStream("/beans.properties"); //默认再main下面的resource里找
        try{
            properties.load(in);
        }catch (IOException e){
            e.printStackTrace();
            System.out.println("加载bean配置文件失败");
        }
    }

    public static Object getBean(String name){
        //根据名字在properties里找对应的类
        String className=properties.getProperty(name);
        try{
            return Class.forName(className).newInstance();
        }catch (Exception e){
            e.printStackTrace();
            System.out.println("获取实例失败");
        }
        return null;
    }
}

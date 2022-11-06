package org;

import java.lang.annotation.Annotation;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class GetClassIOC {
    public static void main(String[] args) throws ClassNotFoundException, InstantiationException, IllegalAccessException, NoSuchMethodException, InvocationTargetException, NoSuchFieldException {
        User u=new User("wgr","asd");
        Class u1=Class.forName("org.User");

/*        Annotation[] annotations=u1.getAnnotations();
        for(Annotation a : annotations){
            System.out.println("1");
        }*/

        //无参构造器
/*        User u2= (User) u1.newInstance();
        System.out.println(u2.getUsername());*/

        //用有参构造器
        //构造器传入对应属性的类
/*        Constructor c=u1.getDeclaredConstructor(java.lang.String.class,java.lang.String.class);
        User u2= (User) c.newInstance("asd","1123");
        System.out.println(u2.getUsername());
        System.out.println(u2.getPassword());*/
。
        //获取方法，方法名，参数类
/*        Method m1=u1.getMethod("setPassword", String.class);
        //在u这个实例中调用m1方法，参数为“bcd”
        m1.invoke(u,"bcd");
        Method m2=u1.getMethod("getPassword");
        //在u这个实例中调用m2方法
        System.out.println(m2.invoke(u));*/

        //获取参数
        Field[] fields=u1.getFields();
        for(Field field:fields){
            System.out.println(field);
        }
        Field field=u1.getDeclaredField("username");
        //获取u这个实例上上username的值,并把其改为密码
        System.out.println("获取的username的值"+field.get(u));
        System.out.println("原密码:"+u.getPassword());
        Method m3=u1.getMethod("setPassword", String.class);
        m3.invoke(u,field.get(u));
        System.out.println("修改后的密码:"+u.getPassword());


    }

}

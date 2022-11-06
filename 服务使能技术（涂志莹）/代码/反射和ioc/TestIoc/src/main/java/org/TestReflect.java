package org;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class TestReflect {
    public static void main(String[] args) throws ClassNotFoundException, InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        test1();
        test2();
        test3();
    }

    public static void test1(){
        User u=new User();
        long startTime = System.currentTimeMillis();
        for(int i=0;i<1000000000;i++){
            u.getUsername();
        }
        long endTime = System.currentTimeMillis();
        System.out.println("普通方法执行10亿次:"+(endTime - startTime)+"ms");
    }

    public static void test2() throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        User user=new User();
        Class u=Class.forName("org.User");
        Method method=u.getMethod("getUsername");
        long startTime = System.currentTimeMillis();
        for(int i=0;i<1000000000;i++){
            method.invoke(user);
        }
        long endTime = System.currentTimeMillis();
        System.out.println("反射方法执行10亿次:"+(endTime - startTime)+"ms");
    }

    public static void test3() throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        User user=new User();
        Class u=Class.forName("org.User");
        Method method=u.getMethod("getUsername");
        method.setAccessible(true);                             //关闭检测
        long startTime = System.currentTimeMillis();
        for(int i=0;i<1000000000;i++){
            method.invoke(user);
        }
        long endTime = System.currentTimeMillis();
        System.out.println("反射关闭检测执行10亿次:"+(endTime - startTime)+"ms");
    }
}

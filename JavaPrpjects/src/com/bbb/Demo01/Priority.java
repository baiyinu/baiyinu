package com.bbb.Demo01;

import java.util.Random;
import java.util.Scanner;

public class Priority {
    static int PSW,AX,BX,CX,DX,PC;                                                                                      // 模拟寄存器
    static int run;                                                                                                     // 运行进程块指针
    static int pfree;                                                                                                   // 空闲控制块指针
    static Pcbarea[] pcbareas = new Pcbarea[10];                                                                        // 创建进程数组
    static Ready ready = new Ready();                                                                                   // 创建就绪队列
//    进程调度
    public  static int sheduling() {
        int i;
//        空闲控制块为空，退出
        if(ready.head == -1){
            System.out.println("无就绪进程");
            return 0;

        }

        i = ready.head;                                                                                                 // 就绪队列头指针付给i
        ready.head = pcbareas[ready.head].next;                                                                         // 就绪队列头指针后移
        pcbareas[i].status = 1 ;                                                                                        // 修改进程控制块状态

//        恢复该进程现场信息
        run = i;
        AX = pcbareas[run].ax;
        BX = pcbareas[run].bx;
        CX = pcbareas[run].cx;
        DX = pcbareas[run].dx;
        PC = pcbareas[run].pc;
        PSW = pcbareas[run].psw;

        System.out.println("程序"+pcbareas[run].id+"执行完毕");
        pcbareas[run].name = 0;


        return 1;

    }
    //  创建进程
    public static int create(int name,int ax, int bx, int cx,int dx,int psw){
        int i;
//        判断进程控制块标记是否为空
        if (pfree == -1){
            System.out.println("无空闲进程控制块，创建进程失败");
            return 0;
        }
        i = pfree;                                                                                                      // 去空闲进程控制块队列的第一个

//        pfree 不为9时空闲控制块标记后移，否则为空赋值为-1
        if (pfree != 9) {
            pfree = pcbareas[i].next;
        }else {
            pfree = -1;
        }
//        填写该进程控制块的内容
        pcbareas[i].name = name;
        pcbareas[i].status = 1;
        pcbareas[i].ax = ax;
        pcbareas[i].bx = bx;
        pcbareas[i].cx = cx;
        pcbareas[i].dx = dx;
        pcbareas[i].pc = 0;
        pcbareas[i].psw = psw;

//        就绪队列不为空时，挂入就绪队列方式
        if (ready.head != -1){
            ready.tail = i;
        }
//        就绪队列空时，挂入就绪队列方式
        else {
            ready.head = i;
            ready.tail = i;
        }
        return 1;
    }

    public static void main(String[] args) {
//        初始化
        int num;
        ready.head = -1;
        ready.tail = -1;
        run = -1;
        pfree = 0;
        for (int i = 0; i <10; i++){
            pcbareas[i] = new Pcbarea();
            pcbareas[i].id = i;
            pcbareas[i].name = 0;
        }
        for (int j = 0; j < 9; j++) {
            pcbareas[j].next = j+1;
        }
        pcbareas[9].next = -1;

        Random random = new Random();                                                                                   // 创建生成随机数对象
        Scanner scanner = new Scanner(System.in);                                                                       // 创建输入对象
        System.out.println("请输入进程编号（编输入负数结束，最多十个进程）：");
        while(scanner.hasNextInt()) {
            try {

                num = scanner.nextInt();
                if (num < 0 ){
                    break;
                }
                create(num, random.nextInt(100), random.nextInt(100), random.nextInt(100), random.nextInt(100), random.nextInt(100));// 创建进程
                System.out.println("请输入进程编号（编输入负数结束，最多十个进程）：");
            } catch (Exception e) {
                System.out.println("输入错误，请重新输入数字");
            }

        }
        while (true) {
            //        获取最大优先级
            int id = pcbareas[0].id;                                                                                    // 存放最大优先级程序的id
            int max = pcbareas[0].name;                                                                                 // 存放最大优先级
            for (int i = 1; i < 10; i++) {
                if (max < pcbareas[i].name){
                    max = pcbareas[i].name;
                    id = pcbareas[i].id;
                }

            }

            ready.head = pcbareas[id].id;

            if (max == 0){
                run = -1;
                System.out.println("所有程序执行完毕");
                break;
            }

            sheduling();
            System.out.println("当前优先级最大的进程id为"+id+"，优先级是"+max);
            System.out.println("----------------------------------------------------");

        }
    }
}


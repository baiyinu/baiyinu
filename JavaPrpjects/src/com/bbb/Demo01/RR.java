package com.bbb.Demo01;

import java.util.Random;
import java.util.Scanner;
import static java.lang.Thread.sleep;

// 时间片轮转调度算法
public class RR {
    static int PSW,AX,BX,CX,DX,PC;                                                                                      // 模拟寄存器
    static int run;                                                                                                     // 运行进程块指针
    static int pfree;                                                                                                   // 空闲控制块指针
    static int time = 50;                                                                                               // 时间片大小
    static Pcbarea[] pcbareas = new Pcbarea[10];                                                                        // 创建进程数组
    static Ready ready = new Ready();                                                                                   // 创建就绪队列

// 进程调度函数
    public  static int sheduling() throws InterruptedException {
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
        //        判断程序是否运行完毕进行下一步操作
        if (pcbareas[run].pc < pcbareas[run].name){
            sleep(time);                                                                                                // 模拟程序运行
            pcbareas[run].pc +=5;


            pcbareas[ready.tail].next = i;
            ready.tail = i;                                                                                         // 进程送往就绪队列尾

            if (pcbareas[run].pc > pcbareas[run].name){

                pcbareas[run].pc = pcbareas[run].name;
                System.out.println("程序"+pcbareas[run].id+"执行完毕");

                if (ready.head == ready.tail){
                    System.out.println("所有程序执行完毕");
                    run = -1;
                }
            }
        }
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

    public static void main(String[] args) throws InterruptedException {

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
        for (int j = 0; j < 9; j++){
            pcbareas[j].next = j+1;
        }
        pcbareas[9].next = 0;
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
            sheduling();                                                                                                // 首次进程调度
        while (run != -1) {
            System.out.println("当前正在执行进程"+pcbareas[run].id);
            System.out.println("寄存器内容ax,bx,cx,dx,pc,psw:"+AX+"\t"+BX+"\t"+CX+"\t"+DX+"\t"+pcbareas[run].pc+"\t"+pcbareas[run].psw);
            System.out.println("进程状态"+pcbareas[run].status);
            pcbareas[run].status = 0;                                                                                   // 进程状态堵塞
            sheduling();                                                                                                // 进程调度
            System.out.println("------------------------------------------------");

        }
    }

}

class Pcbarea {
    int id;                                                                                                             // 标志符
    int name;                                                                                                           // 保存时间片大小，优先级
    int status;
    int ax, bx, cx, dx;
    int pc;
    int psw;
    int next;

}

class Ready {
    int head;
    int tail;
}